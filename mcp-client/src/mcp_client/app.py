from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .model import MCPClientModelRequest, MCPClientModelResponse

from .client import handle_input, download_ollama_models, is_model_downloaded
from .client import ModelStatus

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MCP Client API!"}

@app.post("/process")
async def process_data(data : MCPClientModelRequest) -> MCPClientModelResponse:
    """
    Process the input data and return a response.
    """
    response_message = await handle_input(data.user_query)
    return MCPClientModelResponse(response=response_message)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Handles ModelStatus enum from is_model_downloaded().
    """

    try:
        status = await is_model_downloaded()
        if status == ModelStatus.DOWNLOADED:
            return {"status": "healthy", "message": "Services are up and ready to serve."}
        elif status == ModelStatus.NOT_FOUND:
            return {"status": "wait", "message": "Service is initializing, please wait."}
        elif status == ModelStatus.ERROR:
            return {"status": "error", "message": "Service is unavailable, please try again later."}
        else:
            return {"status": "unknown", "message": f"Unexpected status: {status}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Call the model download function on startup
def run_download_ollama_models():
    import asyncio
    asyncio.run(download_ollama_models())

@app.on_event("startup")
def startup_event():
    """
    Perform any startup tasks here.
    """
    print("MCP Client API is starting up...")
    import threading
    threading.Thread(target=run_download_ollama_models, daemon=True).start()
    print("Ollama models download started in background.")