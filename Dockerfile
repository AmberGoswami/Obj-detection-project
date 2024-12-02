# Base image
FROM ultralytics/ultralytics:latest

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY ./src /app/src
COPY ./outputs /app/outputs

# Expose ports
EXPOSE 8000

# Command to start both services
CMD ["sh", "-c", "uvicorn src.ai_backend.app:app --host 0.0.0.0 --port 8000"]
