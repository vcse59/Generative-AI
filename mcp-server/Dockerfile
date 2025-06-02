# Start from official Python base image
FROM python:3.12-slim

RUN pip install poetry

# Set work directory
WORKDIR /app/mcp_server

# Copy only the poetry files to install dependencies
COPY ./ .

# Configure Poetry to not create virtual environments
RUN poetry install

# Expose port
EXPOSE 8080

# Default command
CMD ["poetry", "run", "mcp-server"]
