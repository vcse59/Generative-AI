# Start from official Python base image
FROM python:3.12-slim

RUN pip install poetry

# Set work directory
WORKDIR /app/mcp_client

# Copy only the poetry files to install dependencies
COPY ./ .

# Configure Poetry to not create virtual environments
RUN poetry install

# Expose port
EXPOSE 8000

# Default command
CMD ["poetry", "run", "uvicorn", "src.mcp_client.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]