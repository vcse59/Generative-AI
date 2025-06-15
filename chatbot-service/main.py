import pypdf
import httpx
import chromadb
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
import os
import asyncio
from dotenv import load_dotenv
import socket
import platform
from contextlib import asynccontextmanager

# Load environment variables from .env file
load_dotenv()

# download ollama models at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Download models at startup."""
    await download_ollama_models()
    yield

# Initialize FastAPI app
app = FastAPI(
    title="RAG API with PDF Citations",
    description="Retrieval-Augmented Generation (RAG) API using PDFs as a knowledge source.",
    version="1.0.0",
    lifespan=lifespan
)

# Specify the absolute or relative path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../config/.env')

# Load the .env file from the given path
load_dotenv(dotenv_path=dotenv_path)

# Access variables
OLLAMA_EMBED_MODEL_NAME =   os.getenv("OLLAMA_EMBED_MODEL_NAME")
OLLAMA_LLM_MODEL_NAME   =   os.getenv("OLLAMA_LLM_MODEL_NAME")
IS_HOST_DOCKER          =   os.getenv("IS_HOST_DOCKER")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for storing PDFs in Docker volume
PDF_STORAGE_DIR = "./pdf_storage"

# Ensure the storage directory exists
os.makedirs(PDF_STORAGE_DIR, exist_ok=True)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./vector_db")
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

# Input Schema for Queries
class RequestModel(BaseModel):
    prompt: str

# Response Schema
class ResponseModel(BaseModel):
    response: str
    citation_links: list  # Stores citation URLs

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to chunk text
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to generate embedding
async def generate_embedding(text):
    try:
        response = httpx.post(f"http://{get_host_ip()}:11434/api/embeddings", json={"model": OLLAMA_EMBED_MODEL_NAME, "prompt": text})
        response_data = response.json()
        return response_data['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Combined Upload and Read PDF API
@app.post("/upload/")
async def upload_and_read_pdf(file: UploadFile = File(...)):
    """Uploads a PDF file, stores it, extracts text, and provides a link to download."""
    
    file_path = os.path.join(PDF_STORAGE_DIR, file.filename)

    # Save the file to the Docker volume
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text and chunk it
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text, chunk_size=500)

    # Store chunks in vector database
    for idx, chunk in enumerate(chunks):
        embedding = await generate_embedding(chunk)
        collection.add(
            ids=[f"{file.filename}-{idx}"], 
            embeddings=embedding, 
            metadatas=[{"text": chunk, "source": file.filename}],  # Store file info
            documents=[chunk]
        )

    # Return the file download link
    file_download_link = f"http://{get_host_ip()}:8000/pdf/{file.filename}"
    
    return {
        "message": f"Processed {len(chunks)} chunks from {file.filename}",
        "download_link": file_download_link
    }

def get_host_ip():
    """
    Returns the host machine's IP address as seen from inside a Docker container.
    Handles Linux (Docker), Windows, and macOS environments.
    """
    try:
        if IS_HOST_DOCKER.lower() == "true":
            # If running inside Docker, use the default gateway IP
            return "host.docker.internal"

        # For non-Docker environments, use the local IP address
        system = platform.system()
        if system == "Linux":
            # Try to detect the host IP from inside Docker (default gateway)
            try:
                with open("/proc/net/route") as f:
                    for line in f.readlines():
                        fields = line.strip().split()
                        if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                            continue
                        gateway_hex = fields[2]
                        gateway = socket.inet_ntoa(bytes.fromhex(gateway_hex)[::-1])
                        return gateway
            except Exception:
                pass
        elif system == "Windows":
            # Use the local IP address
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        elif system == "Darwin":
            # macOS: Use the local IP address
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
    except Exception:
        pass
    # Fallback to localhost if detection fails
    return "localhost"

# Retrieve relevant chunks from vector database
async def retrieve_relevant_chunks(query, top_k=3):
    """Retrieves relevant chunks from the vector database."""
    query_embedding = await generate_embedding(query)
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)

    relevant_chunks = []
    citation_links = []
    
    for item in results["metadatas"][0]:
        chunk_text = item["text"]
        source_file = item["source"]
        citation_url = f"http://{get_host_ip()}:8000/pdf/{source_file}"
        
        relevant_chunks.append(chunk_text)
        citation_links.append({"url" : citation_url, "title" : source_file})

    return relevant_chunks, citation_links

# Query Ollama with retrieved context
async def query_ollama_with_context(context_chunks, user_query):
    """Queries Ollama with retrieved context and returns response."""
    context = "\n\n".join(context_chunks)
    prompt = f"Context: {context}\n\nUser Query: {user_query}\n\nAnswer:"
    
    async with httpx.AsyncClient(timeout=900) as client:
        response = await client.post(
            f"http://{get_host_ip()}:11434/api/generate",
            json={"model": OLLAMA_LLM_MODEL_NAME, "prompt": prompt, "stream": False}
        )
        response_data = response.json()
        return response_data["response"]

# Serve stored PDFs via FastAPI
@app.get("/pdf/{filename}")
async def serve_pdf(filename: str):
    """Serves stored PDFs via API"""
    file_path = os.path.join(PDF_STORAGE_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf")
    return {"error": "File not found"}

# API Endpoint to Process User Query
@app.post("/generate", response_model=ResponseModel)
async def generate_text(request: RequestModel):
    """Processes the user query using RAG and provides citations."""
    relevant_chunks, citation_links = await retrieve_relevant_chunks(request.prompt)

    if not relevant_chunks:
        return {"response": "No relevant information found in the documents.", "citation_links": []}

    # Query Ollama using retrieved context
    response = await query_ollama_with_context(relevant_chunks, request.prompt)

    return ResponseModel(response=response, citation_links=citation_links)

# Function to Download Ollama Models
async def download_ollama_models():
    """Downloads necessary models using Ollama API."""
    try:
        model_names = [OLLAMA_EMBED_MODEL_NAME, OLLAMA_LLM_MODEL_NAME]  # List of models
        for model_name in model_names:
            response = httpx.post(f"http://{get_host_ip()}:11434/api/pull", json={"model": model_name})
            if response.status_code != 200:
                print(f"Failed to download model {model_name}: {response.text}")
    except Exception as e:
        print(f"Error downloading models: {e}")
        raise

# Call the model download function on startup
'''
@app.on_event("startup")
async def startup_event():
    """Download models at startup."""
    await download_ollama_models()
'''

# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=get_host_ip(), port=8000, log_level="info")