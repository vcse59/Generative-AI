# Start from official Python base image
FROM python:3.12-slim

RUN pip install poetry

# Set work directory
WORKDIR /app/agent_server

# Copy only the poetry files to install dependencies
COPY ./ .

# Configure Poetry to not create virtual environments
RUN poetry install

# Remove the unnecessary files to reduce image size
RUN find . -type d -name "__pycache__" -exec rm -rf {} + \
    && find . -type f -name "*.pyc" -delete \
    && find . -type f -name "*.pyo" -delete \
    && find . -type f -name "*.pyd" -delete 
RUN rm -rf Dockerfile

# Default command
CMD ["poetry", "run", "agent-client"]