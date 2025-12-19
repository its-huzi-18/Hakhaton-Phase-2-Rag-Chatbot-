# setup.ps1 - Setup script for RAG Book Chatbot with Qdrant

Write-Host "Setting up RAG Book Chatbot with Qdrant, OpenAI and Gemini support..." -ForegroundColor Green

# Navigate to the rag-book-chatbot backend directory
Set-Location -Path "rag-book-chatbot/backend"

# Create a virtual environment if it doesn't exist
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
pip install --upgrade pip

# Install the required packages
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if the .env file exists, if not create it from the example
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file from example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "Please update the .env file with your API keys and configuration" -ForegroundColor Red
}

Write-Host "Setup complete! You can now:" -ForegroundColor Green
Write-Host "1. Update the .env file with your API keys" -ForegroundColor Green
Write-Host "2. Place your book PDF in the data/ folder" -ForegroundColor Green
Write-Host "3. Run 'python qdrant_ingest.py' to process your book" -ForegroundColor Green
Write-Host "4. Run 'python qdrant_chat.py' to start the chatbot API server" -ForegroundColor Green