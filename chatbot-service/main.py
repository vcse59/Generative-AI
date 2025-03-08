import pypdf
import httpx  # Import httpx for making REST API calls
import chromadb
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os

# Initialize the FastAPI application
app = FastAPI(
    title="RAG Based API Microservice",
    description="API Microservice to process query using RAG (Retrieval-augmented generation) approach and PDF as knowledge source",
    version="1.0.0"
)

# Define CORS configuration
origins = [
    "*",  # To allow all origins (use with caution in production)
]

# Add CORSMiddleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins or specify a list
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Input Schema
class RequestModel(BaseModel):
    prompt: str
    model_name: str

# Response Schema
class ResponseModel(BaseModel):
    response: str
    request: str

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./vector_db")
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

# Ollama API URL (assuming it's running on localhost:11434 in Docker)
OLLAMA_API_URL = "http://ollama:11434"  # Change to your Ollama API URL

# Read PDF file and extract text
def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(file_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Convert the text into chunks
def chunk_text(text, chunk_size=500):
    """Splits text into smaller chunks."""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

async def generate_embedding(text):
    """Generates an embedding using Ollama."""
    try:
        response = httpx.post(f"{OLLAMA_API_URL}/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
        response_data = response.json()
        return response_data['embedding']
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# Retrieve the chunks from vector_db
async def retrieve_relevant_chunks(query, top_k=3):
    """Retrieves relevant chunks from the vector database."""
    query_embedding = await generate_embedding(query)
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    print(f"retrieve_relevant_chunks : {results}")
    return [item['text'] for item in results['metadatas'][0]]

# Create prompt and query Ollama model via REST API
async def query_ollama_with_context(context_chunks, model_name, user_query):
    """Queries Ollama with retrieved context."""
    context = "\n\n".join(context_chunks)
    prompt = f"Context: {context}\n\nUser Query: {user_query}\n\nAnswer:"
    async with httpx.AsyncClient(timeout=900) as client:
        response = await client.post(
            f"{OLLAMA_API_URL}/api/generate",  # Endpoint for querying Ollama with context
            json={"model": model_name, "prompt": prompt, "stream": False}
        )
        response_data = response.json()
        return response_data['response']

# Download models using the Ollama REST API with /api/pull
async def download_ollama_models():
    """Downloads models from Ollama using API keys and the /api/pull endpoint."""
    try:
        model_names = ["nomic-embed-text", "phi3"]  # List of models you want to download
        for model_name in model_names:
            print(f"Downloading model: {model_name}")
            response = httpx.post(f"{OLLAMA_API_URL}/api/pull", json={"model": model_name})
            if response.status_code == 200:
                print(f"Model {model_name} downloaded successfully.")
            else:
                print(f"Failed to download model {model_name}: {response.text}")
    except Exception as e:
        print(f"Error downloading models: {e}")
        raise  # Re-raise the exception to stop the app startup if download fails

# Upload the PDF file to save the embeddings to vector db
@app.post("/upload/")  # Endpoint for uploading PDF
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads a PDF file, extracts text, and stores embeddings."""
    file_path = f"./{file.filename}"
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text, chunk_size=500)

    print(f"chunks : {chunks}")
    for idx, chunk in enumerate(chunks):
        embedding = await generate_embedding(chunk)
        collection.add(
            ids=[str(idx)], 
            embeddings=embedding, 
            metadatas=[{"text": chunk}],
            documents=[chunk]
        )

    return {"message": f"Processed {len(chunks)} chunks from {file.filename}"}

# Process the user query using RAG(Retrieval-augmented generation) approach
@app.post("/generate", response_model=ResponseModel)
async def generate_text(request: RequestModel):
    """Queries the processed PDF content."""
    relevant_chunks = await retrieve_relevant_chunks(request.prompt)

    if not relevant_chunks:
        return {"message": "No relevant information found in the document."}

    # Query Ollama using context found in vector_db
    response = await query_ollama_with_context(relevant_chunks, request.model_name, request.prompt)
    
    # Return the generated response
    return ResponseModel(response=response, request=request.prompt)

# Call the model download function when the application starts
@app.on_event("startup")
async def startup_event():
    """Download models during app startup and block access until it's done."""
    await download_ollama_models()  # Blocks access until models are downloaded
