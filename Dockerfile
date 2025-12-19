FROM python:3.11-slim

WORKDIR /app

COPY rag-book-chatbot/backend/railway_requirements.txt .
RUN pip install --no-cache-dir -r railway_requirements.txt

COPY rag-book-chatbot/backend/ .

# Create a default .env file if it doesn't exist
RUN touch .env

EXPOSE 8000

CMD ["uvicorn", "qdrant_chat.py:app", "--host", "0.0.0.0", "--port", "8000"]