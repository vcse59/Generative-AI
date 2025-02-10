from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import httpx
from fastapi.middleware.cors import CORSMiddleware
import requests
from urllib.parse import quote_plus

app = FastAPI()

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

# Define search function (using a simple search engine API)
def search_web(query: str):
    try:
        # Properly encode the query to handle UTF-8 characters
        encoded_query = quote_plus(query)
        print(f"Encoded Query: {encoded_query}")  # Debug: check encoded query
        
        # Use DuckDuckGo API for demo purposes
        search_url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json"
        print(f"Search URL: {search_url}")  # Debug: check the full URL
        
        response = requests.get(search_url)
        
        # Raise an error for bad status codes
        response.raise_for_status()
        
        search_data = response.json()

        # Debugging: Print the entire response for inspection
        #print(f"Response: {search_data}")  # Debug: check the raw response

        # Check if 'RelatedTopics' exists in the response
        if 'RelatedTopics' in search_data:
            # Extract relevant snippets (example: first 3 results)
            results = [result['Text'] for result in search_data.get('RelatedTopics', [])[:3]]
            return "\n".join(results)
        else:
            print("No 'RelatedTopics' found in the response.")  # Debug: No results found
            return "No relevant results found."

    except requests.exceptions.RequestException as e:
        print(f"Error with the request: {e}")  # Debug: Request issues
        return f"Request failed: {str(e)}"
    except Exception as e:
        print(f"Error occurred: {e}")  # Debug: Other errors
        return f"An error occurred: {str(e)}"

async def get_response(prompt: str, model_name: str, context: str):

    if len(context) > 0:
        # Construct the prompt by combining the query and context
        prompt = f"Question: {prompt}\nContext: {context}\nAnswer:"

    # Ollama API URL for local deployment
    ollama_url = "http://localhost:11434/api/generate"

    # Prepare the request payload
    payload = {
        "model": model_name,  # Adjust model name if needed
        "prompt": prompt
    }

    try:
        async with httpx.AsyncClient() as client:
            print("Sending request to Ollama API...")  # Debug: check request
            response = await client.post(ollama_url, json=payload)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"HTTP error! Status: {response.status_code}")

            combined_response = ""

            async for line in response.aiter_lines():
                line = line.strip()
                if not line:
                    continue
                try:
                    parsed_response = json.loads(line)
                    if "response" in parsed_response:
                        response_text = parsed_response["response"]
                        combined_response += response_text
                        if parsed_response.get("done", False):
                            break
                except json.JSONDecodeError:
                    print("Failed to parse line as JSON:", line)
                    continue
            return combined_response
    except Exception as e:
        print("Error fetching response:", e)
        raise HTTPException(status_code=500, detail="Error fetching response")

@app.post("/generate", response_model=ResponseModel)
async def generate_text(request: RequestModel):
    try:
        # 1. Perform web search to fetch context
        context = search_web(request.prompt)
        
        # 2. Generate a response using Ollama (RAG approach)
        response = await get_response(request.prompt, request.model_name, context)
        
        response = response.strip()

        if len(response) == 0:
            print("No response... Trying again")
            response = await get_response(request.prompt, request.model_name, context)

        # 3. Return the generated response
        return ResponseModel(response=response, request=request.prompt)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
