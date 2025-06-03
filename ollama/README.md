# Ollama Docker Setup

This repository contains a `Dockerfile` for running [Ollama](https://ollama.com/) in a containerized environment.

## Getting Started

### Build the Docker Image

```sh
docker build -t ollama .
```

### Run the Container

```sh
docker run -d --name ollama -p 11434:11434 ollama
```

- The Ollama API will be available at `http://localhost:11434`.

## Customization

- Modify the `Dockerfile` to change Ollama versions or add dependencies as needed.

## Resources

- [Ollama Documentation](https://github.com/jmorganca/ollama)
- [Docker Documentation](https://docs.docker.com/)

---

**Note:** Ensure you have Docker installed and running on your system.