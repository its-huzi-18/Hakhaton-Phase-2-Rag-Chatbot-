FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a default .env file if it doesn't exist
RUN touch .env

EXPOSE $PORT 8000

# Correct ASGI startup command - module name without .py extension
CMD ["sh", "-c", "uvicorn qdrant_chat:app --host=0.0.0.0 --port=${PORT:-8000}"]