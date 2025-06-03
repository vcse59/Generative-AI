# Start from official Python base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app/mcp_client

# Copy only the poetry files to install dependencies
COPY ./ .

# Install system dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]