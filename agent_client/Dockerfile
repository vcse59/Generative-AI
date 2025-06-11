# Start from official Python base image
FROM python:3.12-slim

RUN pip install poetry

# Set work directory
WORKDIR /app/agent_server

# Copy only the poetry files to install dependencies
COPY ./ .

# Configure Poetry to not create virtual environments
RUN poetry install

# Default command
CMD ["poetry", "run", "agent-client"]