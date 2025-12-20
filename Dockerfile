FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy the rag-book-chatbot/backend directory with the app and requirements
COPY rag-book-chatbot/backend/ ./backend/

# Install dependencies from the backend directory (using the lighter requirements)
WORKDIR /app/backend
RUN pip install --no-cache-dir -r railway_requirements.txt

# Change to backend directory for running the app
WORKDIR /app/backend

# Expose port
EXPOSE $PORT 8000

# Start the application using the final version
CMD ["sh", "-c", "uvicorn qdrant_chat_final:app --host=0.0.0.0 --port=${PORT:-8000}"]