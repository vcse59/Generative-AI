# Use an official Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the application files
COPY requirements.txt .
COPY main.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
