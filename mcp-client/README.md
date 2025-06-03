# MCP Client
MCP Client for interacting with the MCP Server and utilizing available tools (e.g., arithmetic operations).

## Features

- Connects to MCP Server to perform tasks using available tools.
- Supports operations such as addition, subtraction, multiplication, and division.

## Usage

### Locally

**Pre-requisites**

- Ensure Python 3.12 is installed.
- Ensure the MCP Server is running and accessible.
- Ensure the ollama is installed and running.
- Ensure the server URL is configured (e.g., via environment variable or config file).

1. Navigate to the project directory:

    ```bash
    cd mcp-client
    ```

2. Create a Python virtual environment:

    ```bash
    python -m venv .venv
    ```

3. Install Poetry in the virtual environment:

    ```bash
    pip install poetry
    ```

4. Install dependencies defined in `pyproject.toml`:

    ```bash
    poetry install
    ```
5. Navigate to MCP client root directory in new terminal and configure following bash variables for mcp-client:

    ```bash
    cd mcp-client
    ```
    ### Environment variables are:

    ```bash
        OLLAMA_LLM_MODEL_NAME=llama3.2:latest
        MCP_SERVER_ENDPOINT=http://127.0.0.1:8080/mcp
        OLLAMA_API_URL=http://127.0.0.1:11434
    ```

6. Run the MCP client:

    ```bash
    poetry run uvicorn src.mcp_client.app:app --host 0.0.0.0 --port 8000 --reload
    ```

### Docker

**Pre-requisite**

- Ensure Docker is installed and running

1. Navigate to the project directory:

    ```bash
    cd $(git rev-parse --show-toplevel)/mcp-client
    ```

2. Build the Docker image:

    ```bash
    docker build -t mcp_client .
    ```

3. Run the Docker image (ensure MCP Server is accessible):

    ```bash
    docker run --rm -it mcp_client
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Security

Please report any security vulnerabilities or concerns by opening an issue or contacting the maintainers directly. We encourage responsible disclosure and will address issues promptly.  
For more information, see the [SECURITY](SECURITY.md) document.
