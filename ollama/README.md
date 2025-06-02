# Ollama Docker Setup

This guide provides instructions to build and run the Ollama Docker image using a Dockerfile, exposing the service on port `11434`.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running

## Build the Docker Image

1. Clone the Ollama repository or ensure you have a Dockerfile for Ollama.
2. Open a terminal and build the Docker image:

    ```bash
    docker build -t ollama .
    ```

## Run the Docker Container

Start the Ollama container and map port `11434`:

```bash
docker run --rm -it -p 11434:11434 ollama
```

The Ollama service will now be accessible on `localhost:11434`.

## Notes

- Adjust the Dockerfile or run command as needed for your specific Ollama configuration.
- For more information, refer to the [Ollama documentation](https://github.com/ollama/ollama).
