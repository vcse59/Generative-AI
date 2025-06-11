# Basic Implementation Using Google A2A (Agent to Agent) in Python

Google's A2A (Agent-to-Agent) framework enables secure, scalable, and seamless communication between autonomous agents or services. In generative AI scenarios, A2A supports agent interactions for message exchange, task delegation, and coordinated actions without direct human involvement. This methodology is widely adopted in distributed systems, microservices, and AI-driven workflows.

Key features of Google A2A include:
- **Standardized Protocols:** Facilitates interoperability among diverse agents through well-defined APIs and message formats.
- **Authentication & Authorization:** Ensures secure agent identification and access control, typically using OAuth or service accounts.
- **Scalability:** Handles large-scale deployments with concurrent agent communications.
- **Observability:** Integrates with monitoring and logging tools to track agent interactions and troubleshoot issues.

This repository presents a simplified A2A model inspired by these principles, emphasizing agent communication, message routing, and extensibility for AI-powered applications.

## Table of Contents

- [Overview](#overview)
- [Components](#components)
- [Getting Started](#getting-started)
- [Docker](#docker)
- [Usage](#usage)
- [Security](#security)
- [License](#license)

## Overview

This project showcases a generative AI system with a complete implementation of both A2A client and server. It consists of two primary components:

- **agent-client:** The A2A client application.
- **agent-server:** The A2A server responsible for processing queries from the **agent-client**.

## Components

### [agent-server](agent_server)

The A2A server processes requests received from the A2A client.

### [agent-client](agent_client)

The A2A client application connects to the A2A server and manages responses.

## Getting Started

### Prerequisites

**Clone the repository:**

```bash
git clone https://github.com/vcse59/GenerativeAI.git
cd GenerativeAI
git checkout feature-a2a-full-implementation
```

### Native Setup

#### Navigate to the repository root directory:

- **Unix/Linux/macOS (bash/zsh/fish):**
  ```bash
  cd "$(git rev-parse --show-toplevel)"
  ```

- **PowerShell (Windows):**
  ```bash
  cd (git rev-parse --show-toplevel)
  ```

- **Command Prompt (cmd.exe on Windows):**
  ```bash
  for /f "delims=" %i in ('git rev-parse --show-toplevel') do cd "%i"
  ```

#### Create and activate a Python virtual environment, then install Poetry using pip:

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
  ```

2. **Start the A2A server in a new terminal with the virtual environment activated:**
  ```bash
  poetry run agent-server
  ```

3. **Start the agent client in a new terminal with the virtual environment activated:**
  ```bash
  poetry run agent-client
  ```

### Docker

You can use Docker Compose to run all components for simplified setup and deployment.

- Navigate to the repository root directory.

1. **Build and launch all services:**
  ```bash
  docker-compose up --build
  ```

2. **Stop all services:**
  ```bash
  docker-compose down
  ```

Ensure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

The `docker-compose.yml` file defines services for both `agent-client` and `agent-server`, with each service built from its respective directory.

## Usage

- The agent-client and agent-server communicate using the A2A protocol.

## Security

For details on security policies, reporting vulnerabilities, and best practices, refer to the [SECURITY.md](./SECURITY.md) document.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more information.
