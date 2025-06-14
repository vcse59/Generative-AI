# RAG (Retrieval-augmented generation) based Gen AI application

- [RAG (Retrieval-augmented generation) based Gen AI application](#rag-retrieval-augmented-generation-based-gen-ai-application)
- [Architecture](#rag-retrieval-augmented-generation-architecture)
- [Components](#components)
- [Set Up](#set-up)
- [Build the docker services](#build-the-docker-services)
- [Update the knowledge source](#update-the-knowledge-source)
- [Process the user query](#process-the-user-query)


## Overview
This project is a Generative AI application that leverages the RAG (Retrieval-augmented Generation) approach to provide intelligent responses based on custom knowledge sources. The application allows you to upload PDF documents, which are processed and converted into vector embeddings stored in a vector database. When a user submits a query through the chat interface, the system retrieves relevant information from the uploaded PDFs using semantic search, and then generates a context-aware answer using a Large Language Model (LLM) such as Ollama.

Key features include:
- Seamless PDF upload and ingestion as knowledge sources.
- Automated conversion of document content into vector embeddings for efficient retrieval.
- Integration with an LLM to generate accurate, context-rich responses.
- Modular architecture with separate services for frontend, backend, and model inference, orchestrated via Docker Compose.
- Easy-to-use chat interface for end users to interact with the knowledge base.

This setup enables organizations to build custom AI assistants that can answer questions based on their own documents, improving information accessibility and productivity.

---

## RAG (Retrieval-augmented generation) Architecture

![RAG (Retrieval-augmented generation) Architecture](RAG%20Architecture.png)

---

# Components

Here are the components used in this application:

- Frontend application (chatbot-app)
- Microservice application (chatbot-service)
- Ollama LLM and Embedding Model. 

---

## Set Up

Make sure following application is installed and running:

- PDF file is available to upload and use the PDF content as knowledge source.
- Docker is installed and running.

---

## Build the docker services

The Docker Compose file in the root folder manages all dependencies and services.

You can use the `--profile` option to choose which services to run. For example:

- To run only the ollama service:
    ```
    docker compose --profile ollama up
    ```

- To run only the chatbot-service:
    ```
    docker compose --profile chatbot up
    ```

- To run only the chatapp (frontend) service:
    ```
    docker compose --profile chatapp up
    ```

- To run multiple services (e.g., ollama, chatbot, and chatapp):
    ```
    docker compose --profile ollama --profile chatbot --profile chatapp up
    ```

If you omit `--profile`, all services will run by default.

---

## Update the knowledge source

- Open http://localhost:8000/docs and use /upload API endpoint to upload PDF file to convert the PDF content to vector embedding and save the embedding to vector DB(mounted in Docker).

---

## Process the user query

- open the chat application (http://localhost:8080) and click on chat icon in bottom right corner to open the chat dialog and enter the user query based on configured knowledge source.
