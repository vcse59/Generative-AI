# RAG (Retrieval-augmented generation) based application

This is a Generative AI application using RAG (Retrieval-augmented generation) approach to use PDF as a knowledge source and process user query.

Here are the components used in this application:

- Frontend application (chatbot-app)
- Microservice application (chatbot-service)
- Ollama LLM and Embedding Model. 

## Set Up

Make sure following application is installed and running:

- PDF file is available to upload and use the PDF content as knowledge source.
- Docker is installed and running.

## Build the docker service

Docker compose file in root folder takes care of downloading all the dependencies.

- docker compose up --build

## Run the docker service:

### Update the knowledge source

- Open http://localhost:8000/docs and use /upload API endpoint to upload PDF file to convert the PDF content to vector embedding and save the embedding to vector DB(mounted in Docker).

### Process the user query

- open the chat application (http://localhost:8080) and click on chat icon in bottom right corner to open the chat dialog and enter the user query based on configured knowledge source.
