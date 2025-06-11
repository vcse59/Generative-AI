# Basic implementation using Google A2A (Agent to Agent) in python

Google's A2A (Agent-to-Agent) framework is designed to enable seamless, secure, and scalable communication between autonomous agents or services. In the context of generative AI, A2A facilitates interactions where agents can exchange messages, delegate tasks, and coordinate actions without direct human intervention. This approach is commonly used in distributed systems, microservices architectures, and AI-driven workflows.

Key aspects of Google A2A include:
- **Standardized Protocols:** Ensures interoperability between heterogeneous agents using well-defined APIs and message formats.
- **Authentication & Authorization:** Provides secure agent identification and access control, often leveraging OAuth or service accounts.
- **Scalability:** Supports large-scale deployments where multiple agents communicate concurrently.
- **Observability:** Integrates with monitoring and logging tools for tracking agent interactions and diagnosing issues.

This repository demonstrates a simplified A2A model inspired by these principles, focusing on agent communication, message routing, and extensibility for AI-driven applications.


## Table of Contents

- [Overview](#overview)
- [Components](#components)
- [Getting Started](#getting-started)
- [Docker](#docker)
- [Security](#security)
- [License](#license)

## Overview

This project demonstrates a generative AI system with end to end implementation of A2A client and server. It is divided into two main components:

- **agent-client**: The A2A client application.
- **agent-server**: The A2A server that processes the query coming from **agent-client**.

## Components

### [agent-server](agent_server)

A2A server to process request coming from A2A client.

### [agent-client](agent_client)

A2A client application to connect to A2A server and handle the response.

## Getting Started

### Pre-requisite

**Clone the repository:**

```bash
git clone https://github.com/vcse59/GenerativeAI.git
cd GenerativeAI
git checkout feature-a2a-full-implementation
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
    cd ../agent_server
    poetry install
    cd ../agent_client
    poetry install

2. **Navigate to agent-server project and start the A2A server in new terminal with active virtual envrionment:**
    ```bash
    poetry run agent-server
    ```

3. **Navigate to agent-client project and start the agent client in new terminal with active virtual envrionment:**
    ```bash
    poetry run agent-client
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

The `docker-compose.yml` file defines services for `agent-client`, and `agent-server`. Each service is built from its respective directory.

## Usage

- The agent-client and agent-server communicate the message over A2A protocol.

## Security

For information about security policies, reporting vulnerabilities, and best practices, please refer to the [SECURITY.md](./SECURITY.md) document.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

