# GenerativeAI

This repository contains components for a generative AI project, including a chat application, client, and server.

## Table of Contents

- [Overview](#overview)
- [Components](#components)
- [Getting Started](#getting-started)
- [Docker](#docker)
- [Usage](#usage)
- [Security](#security)
- [License](#license)

## Overview

This project demonstrates a generative AI system with a chat interface. It is divided into three main components:

- **chat-app**: The frontend chat application.
- **mcp-client**: The client that communicates with the server.
- **mcp-server**: The backend server handling AI generation.
- **ollama**: The backend service handling ollama models.

## Components

### [chat-app](chat-app)

A user-friendly web interface for interacting with the generative AI. Built with modern web technologies. Check out [README.md](chat-app/README.md)

### [mcp-client](mcp-client)

Handles communication between the chat-app and the mcp-server. Responsible for sending user messages and receiving AI responses. Check out [README.md](mcp-client/README.md)

### [mcp-server](mcp-server)

The backend service that processes requests and generates responses using AI models. Check out [README.md](mcp-server/README.md)

### [Ollama](ollama)

This is the docker service to use run ollama as a docker image. 
It it recommended to use docker to run ollama. Check out [README.md](ollama/README.md)

## Getting Started

### Pre-requisite

**Clone the repository:**

```bash
git clone https://github.com/vcse59/GenerativeAI.git
cd GenerativeAI
git checkout mcp-client-server-e2e
```
### Native:

#### Navigate to repository root directory:

- **Unix/Linux/macOS (bash/zsh/fish)**

```bash
cd "$(git rev-parse --show-toplevel)"
```

- **PowerShell (Windows)**

```bash
cd (git rev-parse --show-toplevel)
```

- **Command Prompt (cmd.exe on Windows)**
 
```bash
for /f "delims=" %i in ('git rev-parse --show-toplevel') do cd "%i"
```

#### Create, activate a Python virtual environment and install poetry using pip:

- **Windows (Command Prompt):**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install poetry
    ```

- **Windows (PowerShell):**
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install poetry
    ```

- **Unix/Linux/macOS (bash/zsh):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install poetry
    ```

1. **Install dependencies for each component:**
    ```bash
    cd chat-app
    npm install
    cd ../mcp-client
    poetry install
    cd ../mcp-client
    poetry install

2. **Navigate to mcp-server project and start the MCP server in new terminal with active virtual envrionment:**
    ```bash
    poetry run mcp-server
    ```

3. **Follow the instructions to start the ollama service in docker in new terminal:**

    [**Ollama**](ollama/README.md)

4. **Navigate to MCP client root directory in new terminal and configure following bash variables for mcp-client**

    ### Environment variables are:

    ```bash
    OLLAMA_LLM_MODEL_NAME=llama3.2 # Can be changed
    MCP_SERVER_ENDPOINT=http://127.0.0.1:8080/mcp
    OLLAMA_API_URL=http://127.0.0.1:11434
    ```

5. **Navigate to mcp-client project and start the MCP client in new terminal with active virtual envrionment:**
    ```bash
    poetry run uvicorn src.mcp_client.app:app --host 0.0.0.0 --port 8000 --reload
    ```

6. **Navigate to chat-app project and start the chat app in new terminal:**
    ```bash
    npm start
    ```

### Docker

You can run all components using Docker Compose for easier setup and deployment.

- Navigate to repoistory root directory


1. **Build and start all services:**
    ```bash
    docker-compose up --build
    ```

2. **Stop the services:**
    ```bash
    docker-compose down
    ```

Make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

The `docker-compose.yml` file defines services for `chat-app`, `mcp-client`, and `mcp-server`. Each service is built from its respective directory.

## Usage

- Open the chat-app in your browser(http://localhost:5000).
- Enter your message and interact with the AI.
- The mcp-client and mcp-server handle message routing and AI generation.

## Security

For information about security policies, reporting vulnerabilities, and best practices, please refer to the [SECURITY.md](./SECURITY.md) document.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

