## Overview

This project provides a FastAPI-based microservice for powering a chatbot application. It processes user queries using Ollama models specified in the request.

## Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Service

### Option 1: Local Development

Set the environment variable:

```bash
OLLAMA_API_URL=http://127.0.0.1:11434
```
Start the FastAPI server locally:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Option 2: Using Docker

Build and run the service with Docker:

```bash
docker build -t backend-service .
docker run -p 8000:8000 backend-service
```

## Project Structure

- `main.py`: Main FastAPI application.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Containerization instructions.

## Usage

Send POST requests to `/generate` with your query and model details. Refer to the API documentation at `http://localhost:8000/docs` when the server is running.

