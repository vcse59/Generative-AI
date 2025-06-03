import json
import re
import requests
import traceback
import os

import httpx
#from dotenv import load_dotenv

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


from typing import List
from enum import Enum, auto

# Load environment variables from .env file
# load_dotenv()

# Access .env variables if needed
OLLAMA_LLM_MODEL_NAME = os.environ.get("OLLAMA_LLM_MODEL_NAME") # Default model name, can be overridden by setting shell variable

# MCP Server Endpoint
MCP_SERVER_ENDPOINT = os.environ.get("MCP_SERVER_ENDPOINT")  # MCP server endpoint, can be overridden by setting shell variable

# Ollama API URL
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL")  # Ollama API URL, can be overridden by setting shell variable

class ModelStatus(Enum):
    DOWNLOADED = auto()
    NOT_FOUND = auto()
    ERROR = auto()

async def is_model_downloaded() -> ModelStatus:
    """
    Checks if the specified Ollama model is downloaded locally.

    Returns:
        ModelStatus: Enum indicating the model status.
    """
    try:
        print(f"🔄 Checking Ollama model: {OLLAMA_LLM_MODEL_NAME}...")
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        response.raise_for_status()
        models = response.json().get("models", [])

        if len(models) == 0:
            print("No models found in Ollama.")
            return ModelStatus.NOT_FOUND

        if any(model["name"] == OLLAMA_LLM_MODEL_NAME for model in models):
            return ModelStatus.DOWNLOADED
        else:
            return ModelStatus.NOT_FOUND

    except requests.exceptions.RequestException as e:
        print(f"Error checking model availability: {e}")
        return ModelStatus.ERROR

# Function to Download Ollama Models
def download_ollama_models():
    """Downloads necessary models using Ollama API."""
    try:
        print(f"🔄 Downloading Ollama model: {OLLAMA_LLM_MODEL_NAME}...")
        model_names = [OLLAMA_LLM_MODEL_NAME]  # List of models
        for model_name in model_names:
            response = httpx.post(f"{OLLAMA_API_URL}/api/pull", json={"model": model_name})

            if response.status_code == 200:
                print(f"Model {model_name} downloaded successfully.")
            else:
                print(f"Failed to download model {model_name}: {response.text}")
    except Exception as e:
        print(f"Error downloading models: {e}")
        raise

def build_system_prompt(tools: List[list], user_prompt: str) -> str:
    """
    Construct a system prompt from available tools and user input.
    `tools` is expected to be a list where the first element is a list of Tool objects.
    """
    if not tools or not tools[0]:
        return "No tools are available to select from."

    tool_descriptions = ""
    for tool in tools[0]:
        name = getattr(tool, "name", "unknown_tool")
        description = getattr(tool, "description", "No description provided")
        input_schema = getattr(tool, "inputSchema", {})
        params = input_schema.get("properties", {})

        if params:
            param_str = ", ".join(
                f"{param}: {info.get('type', 'unknown')}" for param, info in params.items()
            )
        else:
            param_str = "no parameters"

        tool_descriptions += f"- {name}({param_str}): {description}\n"

    system_prompt = f"""You are a helpful assistant that selects the correct tool and parameters based on user input.

Available Tools:
{tool_descriptions}

User Query: {user_prompt}

Respond ONLY in this JSON format (no explanation or extra text) and give error description if any:

{{
    "tool_name": "tool_name",
    "parameters": {{
      "param1": "value",
      "param2": "value"
    }}
}}

"""
    return system_prompt.strip()

async def build_generative_response_prompt(output_response: str, user_prompt: str) -> str:
    """
    Build a prompt for the LLM to generate a response based on the tool call output.
    """
    if not output_response:
        return "No valid response from the tool call."

    generative_prompt = f"""You are a helpful assistant that generates a response based on the tool call output.
Output to User Query {user_prompt} is as follows:
{output_response}
Respond ONLY in string format, no JSON or extra text.
"""
    return generative_prompt.strip()

async def regenerate_user_prompt(user_prompt: str) -> str:
    """
    Regenerate the user prompt based on intent.
    """
    if not user_prompt:
        return "No user prompt provided."
    
    prompt = f"""You are a helpful assistant that regenerates user prompts based on intent.
User Query: {user_prompt}
Regenerate the user prompt to be more specific and clear, focusing on the intent of the user.
Respond ONLY in string format, no JSON or extra text.
"""
    output_response = await call_ollama(prompt=prompt, model=OLLAMA_LLM_MODEL_NAME)
    if isinstance(output_response, dict):
        output_response = output_response.get("response", "")
    
    return output_response.strip()

async def call_ollama(prompt: str, model="llama3.2") -> dict:
    url = f"{OLLAMA_API_URL}/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        raw_output = response.json().get("response", "")

        # Remove Markdown-style code block
        cleaned = re.sub(r'^```json\n|```$|\\\"', '', raw_output.strip(), flags=re.MULTILINE)

        # Remove "quotes at the start and end if they exist
        if cleaned.startswith('"') and cleaned.endswith('"'):
            # Remove only if the string is not empty
            if len(cleaned) > 1:
                # Strip the quotes
                cleaned = cleaned[1:-1]

        return cleaned
    except Exception as e:
        print(f"\n❌ Failed to call Ollama or parse output: {e}")
        print(f"Raw output: {response.text if response else 'No response'}")
        return None

async def connect():
    async with streamablehttp_client(MCP_SERVER_ENDPOINT) as (
        read_stream,
        write_stream,
        _
    ):


        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Get available tools
            mcp_tools_raw = await session.list_tools()

            # mcp_tools_raw is a list of tuples: (tool_name, tool_info_dict)
            mcp_tools = []
            for tool_name, tool_info in mcp_tools_raw:

                if not isinstance(tool_info, list):
                    continue
                mcp_tools.append(tool_info)

            return mcp_tools

async def run(available_tools: list, user_query: str):
    async with streamablehttp_client(MCP_SERVER_ENDPOINT) as (
        read_stream,
        write_stream,
        _
    ):
        
        user_input = user_query.strip()
        if not user_input:
            print("❌ No user input provided. Exiting.")
            return None
        
        user_input = await regenerate_user_prompt(user_input)
        if not user_input:
            print("❌ Failed to regenerate user prompt. Exiting.")
            return None

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # mcp_tools_raw is a list of tuples: (tool_name, tool_info_dict)
            mcp_tools = available_tools

            # Generate system prompt for LLM
            system_prompt = build_system_prompt(mcp_tools, user_input)

            # Call Ollama model
            tool_call = await call_ollama(prompt=system_prompt, model=OLLAMA_LLM_MODEL_NAME)
            tool_call = json.loads(tool_call)
            print(f"\n🔍 LLM tool call suggestion: {tool_call}")
            if not tool_call:
                print("❌ Tool call generation failed.")
                return
                
            tool_name = tool_call.get("tool_name")
            parameters = tool_call.get("parameters", {})

            # Validate tool name
            available_tool_names = [tool.name for tool in mcp_tools[0]]
            
            if tool_name not in available_tool_names:
                print(f"\n❌ Tool '{tool_name}' is not available. Choose from: {available_tool_names}")
                return

            print(f"\n🛠️ Using Tool: {tool_name}")
            print(f"📦 With Parameters: {parameters}")

            try:
                result = await session.call_tool(tool_name, parameters)
                print(f"\n✅ Result: {result}")
                if hasattr(result, 'content') and result.content:
                    text_content = result.content[0].text if isinstance(result.content, list) else result.content.text
                    print(f"\n📄 Result Text: {text_content}")
                    result = text_content
                else:
                    print("\n❌ No content returned from the tool call.")
                    result = None

                # Generate a response from the LLM based on the tool call output
                generative_prompt = await build_generative_response_prompt(result, user_query)
                result = await call_ollama(prompt=generative_prompt, model=OLLAMA_LLM_MODEL_NAME)
                result = result.strip('"')  # Remove quotes if they exist
                print(f"\n🔄 Final Result : {result}")
                return result
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    print(f"\n❌ Tool '{tool_name}' not found on the MCP server.")
                else:
                    print(f"\n❌ HTTP error occurred: {e}")
            except Exception as e:
                print(f"\n❌ MCP tool execution failed: {e}")


async def handle_input(user_input: str) -> str:
    """
    Handle user input and run the main logic.
    """
    try:
        available_tools = await connect()
        result = await run(available_tools, user_input)
        if result:
            print(f"\n✅ Final Result: {result}")
        else:
            print("\n❌ No result returned from the tool call.")
        return result
    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP error occurred: {e}")
    except Exception as eg:  # Python 3.11+
        print("\n❌ ExceptionGroup occurred:")
        for e in eg.exceptions:
            traceback.print_exception(type(e), e, e.__traceback__)

if __name__ == "__main__":
    handle_input()
