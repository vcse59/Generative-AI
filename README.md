<!--
    Documentation:
    This README offers a detailed overview of the GenerativeAI project repository.
    The repository contains several Generative AI applications, each maintained in its own branch.
    For setup and usage instructions, please refer to the README file within the relevant branch.
-->

# Generative AI Applications Repository

Welcome to the GenerativeAI repository! This project features a variety of practical Generative AI applications developed using the Ollama framework. Ollama allows you to experiment with large language models locally, making it straightforward to prototype and deploy AI-driven solutions.

## Repository Structure

Each application resides in a separate branch, enabling you to explore different Generative AI use cases independently. The primary categories of applications include:

- **Chatbots**: Conversational agents powered by large language models.
- **Retrieval-Augmented Generation (RAG)**: Solutions that integrate external data sources (such as web content, PDFs, or images) with language models to deliver context-aware responses.
- **Client-Server Architectures**: Examples of end-to-end systems utilizing AI models in distributed setups.

## Getting Started

To explore and run any application:

1. **Clone the repository** to your local system:
   ```bash
   git clone https://github.com/vcse59/GenerativeAI.git
   ```
2. **Switch to the branch** for the application you wish to use:
   ```bash
   git checkout <branch-name>
   ```
3. **Follow the instructions** in the README file specific to that branch for setup, dependencies, and usage.

## Available Applications

The main applications currently available in this repository are:

- [Web Search-Based RAG Pipeline with Chat Application](https://github.com/vcse59/GenerativeAI/tree/Ollama_Chatbot):  
  Processes user queries using web search results within a Retrieval-Augmented Generation pipeline.

- [RAG Application Using PDF as Knowledge Source](https://github.com/vcse59/GenerativeAI/tree/rag-based-application):  
  Supports chat-based interactions with information extracted from PDF documents via a RAG pipeline.

- [RAG Application with Redis and Image Parsing](https://github.com/vcse59/GenerativeAI/tree/redis_image_based_rag_pipeline):  
  Leverages Redis for rapid data retrieval and includes image-to-text parsing to enhance chatbot responses in the RAG pipeline.

- [End-to-End MCP Client-Server Chat Application](https://github.com/vcse59/GenerativeAI/tree/mcp-client-server-e2e):  
  Showcases a complete client-server architecture for chat applications, highlighting the integration of AI models in distributed environments.

## Prerequisites

- [Docker](https://www.docker.com/) (for running Ollama models locally)
- [Ollama](https://ollama.com/) (see the official documentation for installation and supported models)
- Python 3.10+ (required for most applications)
- Additional dependencies as listed in each branch's README

## Learn More

For comprehensive documentation, setup instructions, and advanced usage, please consult the README file in each application branch.

To discover more about Ollama and its features, visit the [official Ollama website](https://ollama.com/).

---

Contributions and suggestions are welcome! Please open issues or submit pull requests for improvements.