from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .model import MCPClientModelRequest, MCPClientModelResponse

from .client import handle_input, download_ollama_models

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


# Call the model download function on startup
@app.on_event("startup")
async def startup_event():
    """
    Perform any startup tasks here.
    """
    print("MCP Client API is starting up...")
    await download_ollama_models()
    print("Ollama models downloaded successfully.")