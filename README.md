<!--
  Documentation:
  This README provides an overview of the GenerativeAI project repository.
  The repository hosts multiple Generative AI applications, each organized in its own branch.
  For setup and usage details, refer to the README within the respective branch.
-->

# Generative AI Applications Repository

Welcome to the GenerativeAI repository! Here you'll find a collection of practical Generative AI applications built using the Ollama framework. Ollama enables local experimentation with large language models, making it easy to prototype and deploy AI-powered solutions.

## Repository Structure

Each application is maintained in a dedicated branch, allowing you to explore various Generative AI use cases independently. The main categories include:

- **Chatbots**: Conversational agents utilizing large language models.
- **Retrieval-Augmented Generation (RAG)**: Applications that combine external data sources (such as web content, PDFs, or images) with language models for context-aware outputs.
- **Client-Server Architectures**: Examples of distributed systems integrating AI models.

## Getting Started

To try out any application:

1. **Clone the repository** to your machine:
   ```bash
   git clone https://github.com/vcse59/GenerativeAI.git
   ```
2. **Checkout the branch** for the desired application:
   ```bash
   git checkout <branch-name>
   ```
3. **Follow the branch-specific README** for setup, dependencies, and usage instructions.

## Available Applications

Currently, the repository includes the following main applications:

- [Web Search-Based RAG Pipeline with Chat Application](https://github.com/vcse59/GenerativeAI/tree/feature-chatapp-websearch-rag-pipeline):  
  Handles user queries by incorporating web search results into a Retrieval-Augmented Generation pipeline.

- [RAG Application Using PDF as Knowledge Source](https://github.com/vcse59/GenerativeAI/tree/feature-rag-pdf-based-application):  
  Enables chat-based interactions using information extracted from PDF documents via a RAG pipeline.

- [RAG Application with Redis and Image Parsing](https://github.com/vcse59/GenerativeAI/tree/feature-redis_image_based_rag_pipeline):  
  Utilizes Redis for fast data retrieval and supports image-to-text parsing to enhance chatbot responses in the RAG pipeline.

- [End-to-End MCP Client-Server Chat Application](https://github.com/vcse59/GenerativeAI/tree/feature-mcp-client-server-e2e):  
  Demonstrates a complete client-server chat architecture, showcasing AI model integration in distributed systems.

- [End-to-End A2A (Agent2Agent) Client-Server Application](https://github.com/vcse59/GenerativeAI/blob/feature-a2a-full-implementation):  
  Presents a full A2A (Agent2Agent) client-server setup, highlighting AI model integration over the A2A protocol.

## Prerequisites

- [Docker](https://www.docker.com/) (for running Ollama models locally)
- [Ollama](https://ollama.com/) (refer to the official documentation for installation and supported models)
- Python 3.10+ (required for most applications)
- Additional dependencies listed in each branch's README

## Additional Resources

- [LICENSE](/LICENSE): Repository distribution terms.
- [SECURITY](/SECURITY.md): Instructions for reporting vulnerabilities and security concerns.

## Learn More

For detailed documentation, setup guides, and advanced usage, see the README in each application branch.

To learn more about Ollama and its capabilities, visit the [official Ollama website](https://ollama.com/).

---

Contributions and feedback are encouraged! Please open issues or submit pull requests to help improve this repository.
