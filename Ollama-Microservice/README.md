## Overview

This project utilizes FastAPI to build a microservice that powers a chatbot application. It processes user queries using Ollama models specified in the request.

### Step 1: Install Dependencies

Run the following command to install the required packages:

$ pip install -r requirements.txt

### Step 2: Start the FastAPI Server

Launch the server using:

$ uvicorn ollama:app --host 0.0.0.0 --port 8000
