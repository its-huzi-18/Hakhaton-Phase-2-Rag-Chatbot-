#!/bin/bash
# setup.sh - Setup script for RAG Book Chatbot with Qdrant

echo "Setting up RAG Book Chatbot with Qdrant, OpenAI and Gemini support..."

# Navigate to the rag-book-chatbot backend directory
cd rag-book-chatbot/backend

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate the virtual environment
source .venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Check if the .env file exists, if not create it from the example
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please update the .env file with your API keys and configuration"
fi

echo "Setup complete! You can now:"
echo "1. Update the .env file with your API keys"
echo "2. Place your book PDF in the data/ folder"
echo "3. Run 'python qdrant_ingest.py' to process your book"
echo "4. Run 'python qdrant_chat.py' to start the chatbot API server"