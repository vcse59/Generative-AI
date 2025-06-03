# Generative AI Chatbot with Ollama, Docker Compose, and Web Search Integration

This repository contains a chatbot application powered by Generative AI models using Ollama. The chatbot is enhanced with real-time context fetching from the internet via the DuckDuckGo Web Search API, allowing it to provide up-to-date and relevant responses based on user queries. The project features a containerized setup with Docker Compose for easy deployment and management of multiple services.

---

## Services Overview

This project uses the following services, each with its own README and specific functionality:

- **Ollama Service**  
    - **Location:** [`/ollama/README.md`](/ollama/README.md)  
    - **Details:** Hosts and serves generative AI models for chatbot responses. Handles model inference and communication with the main application.

- **Chatbot Application Service**  
    - **Location:** [`/frontend-chat/README.md`](/frontend-chat/README.md)  
    - **Details:** Main application logic for handling user queries, orchestrating requests to Ollama and Web Search services, and serving the frontend or API endpoints.

- **(Optional) Frontend Service**  
    - **Location:** [`/backend-service/README.md`](/backend-service/README.md)  
    - **Details:** Provides a user interface for interacting with the chatbot. (Include if your project has a separate frontend.)

---

## Project Structure

- **Docker Compose Setup**:  
        The repository includes a `docker-compose.yml` file to orchestrate multiple services for the chatbot application.

- **Dockerfiles**:  
        Each service/component has its own `Dockerfile` for containerization, enabling easy deployment and scalability.

- **Web Search Integration**:  
        The chatbot leverages the DuckDuckGo Web Search API to retrieve contextual information from the internet, enriching its responses.

---

## Build and Run Instructions

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system.
- [Docker Compose](https://docs.docker.com/compose/install/) (if not included with Docker Desktop).
- DuckDuckGo Web Search API key (if required).

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/vcse59/GenerativeAI.git
    cd GenerativeAI
    ```

2. **Build Docker Images**

    ```bash
    docker compose build
    ```

3. **Start the Services**

    ```bash
    docker compose up
    ```
    This will start all services defined in the `docker-compose.yml` file.

4. **Access the Application**
    - Follow the logs or documentation for the specific service endpoints (e.g., `http://localhost:5000`).

5. **Stop the Services**
    ```bash
    docker compose down
    ```

---

## Resources

- **YouTube Video**:  
        https://www.youtube.com/watch?v=V40wit53nXg

- **Dev.to Blog**:  
        https://dev.to/vivekyadav200988/chatbot-application-using-models-available-in-ollama-17n9

---

## Security

For information about security policies, reporting vulnerabilities, and best practices, see [SECURITY.md](./SECURITY.md).

---

## License

This project is licensed. For details, see the [LICENSE](./LICENSE) file.
