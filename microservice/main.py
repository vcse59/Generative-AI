from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import redis.asyncio as redis
import faiss
import numpy as np
import chromadb
import pytesseract
import json
import logging
import hashlib
import requests
import os
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Specify the absolute or relative path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../config/.env')

# Load the .env file from the given path
load_dotenv(dotenv_path=dotenv_path)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Access variables
OLLAMA_EMBED_MODEL_NAME =   os.getenv("OLLAMA_EMBED_MODEL_NAME")
OLLAMA_LLM_MODEL_NAME   =   os.getenv("OLLAMA_LLM_MODEL_NAME")

# Connect to Redis
cache = redis.Redis(host="redis", port=6379, decode_responses=True)

# Ollama API URL
OLLAMA_API_URL = "http://ollama:11434"

# FAISS setup
dimension = 768
index = faiss.IndexFlatL2(dimension)

# ChromaDB setup
chroma_client = chromadb.PersistentClient(path="/chroma_db")
collection = chroma_client.get_or_create_collection(name="image_contexts")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_text(prompt: str) -> str:
    url = f"{OLLAMA_API_URL}/api/generate"
    data = {"model": OLLAMA_LLM_MODEL_NAME, "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return json.loads(response.text)["response"]
    except Exception as e:
        logger.error(f"Failed to get text from Ollama: {e} | Raw: {response.text}")
        raise

def generate_embeddings(prompt: str) -> np.ndarray:
    url = f"{OLLAMA_API_URL}/api/embeddings"
    data = {"model": OLLAMA_EMBED_MODEL_NAME, "prompt": prompt}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        embedding = response.json()["embedding"]
        vec = np.asarray(embedding, dtype=np.float32).reshape(1, -1)
        if vec.shape[1] != dimension:
            raise ValueError(f"Expected embedding of shape (1, {dimension}), got {vec.shape}")
        return vec
    except Exception as e:
        logger.error(f"Failed to get embedding: {e}")
        raise

def extract_text(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return pytesseract.image_to_string(image)
    except Exception as e:
        logger.error(f"Failed to extract text from image: {e}")
        return ""

def hash_content(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()

async def process_image_with_rag(image_bytes: bytes):
    extracted_text = extract_text(image_bytes).strip()
    if not extracted_text:
        return {"response": "No text could be extracted from the image."}

    logger.info(f"Extracted Text: {extracted_text}")

    # Generate embeddings
    embedding = generate_embeddings(extracted_text)

    # FAISS vector search (optional safety if index is empty)
    if index.ntotal == 0:
        logger.warning("FAISS index is empty; skipping FAISS search.")
    else:
        try:
            _, idxs = index.search(embedding, k=2)
            logger.info(f"FAISS returned indices: {idxs}")
        except Exception as e:
            logger.error(f"FAISS search failed: {e}")

    # ChromaDB search
    retrieved_contexts = []
    try:
        results = collection.query(query_embeddings=embedding.tolist(), n_results=2)
        for doc_text in results["documents"][0]:
            retrieved_contexts.append(doc_text)
    except Exception as e:
        logger.error(f"ChromaDB query failed: {e}")

    context = "\n".join(retrieved_contexts)
    prompt = f"Extracted Text: {extracted_text}\n\nContext: {context}\n\nDescribe the image."

    # Cache check
    cache_key = f"rag:{hash_content(prompt)}"
    cached_response = await cache.get(cache_key)
    if cached_response:
        logger.info("Cache hit")
        return json.loads(cached_response)

    # Generate text using Ollama
    response_text = generate_text(prompt)
    result = {"response": response_text}

    await cache.set(cache_key, json.dumps(result), ex=3600)
    logger.info("Cache miss: storing new response")

    return result

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = await process_image_with_rag(image_bytes)
    return {"description": result["response"]}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connected")
    try:
        while True:
            image_bytes = await websocket.receive_bytes()
            result = await process_image_with_rag(image_bytes)
            await websocket.send_text(result["response"])
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
        logger.info("WebSocket disconnected")

# Function to Download Ollama Models
async def download_ollama_models():
    """Downloads necessary models using Ollama API."""
    try:
        model_names = [OLLAMA_EMBED_MODEL_NAME, OLLAMA_LLM_MODEL_NAME]  # List of models
        for model_name in model_names:
            response = httpx.post(f"{OLLAMA_API_URL}/api/pull", json={"model": model_name})
            if response.status_code == 200:
                print(f"Model {model_name} downloaded successfully.")
            else:
                print(f"Failed to download model {model_name}: {response.text}")
    except Exception as e:
        print(f"Error downloading models: {e}")
        raise

# Call the model download function on startup
@app.on_event("startup")
async def startup_event():
    """Download models at startup."""
    await download_ollama_models()