# RAG Book Chatbot with Qdrant, OpenAI & Gemini

This is a Retrieval-Augmented Generation (RAG) chatbot that answers questions based only on the content of a specific book. It supports both OpenAI and Google Gemini models with Qdrant vector database.

## Features

- **Qdrant Vector Database**: Fast and efficient similarity search
- **Multiple LLM Support**: OpenAI GPT and Google Gemini models
- **Docusaurus Integration**: Seamless integration with your book website
- **PDF Processing**: Automatic extraction and chunking of book content
- **Context-Aware Responses**: Answers based only on book content

## Project Structure

```
rag-book-chatbot/
  backend/
    qdrant_ingest.py     # Script to process the PDF and create Qdrant vector database
    qdrant_chat.py       # FastAPI application for the chatbot with Qdrant
    chat.py             # Legacy script using ChromaDB (for reference)
    ingest.py           # Legacy script using ChromaDB (for reference)
    requirements.txt    # Dependencies
    .env.example        # Example environment variables
  data/
    book.pdf            # Your book file goes here
  web-client/
    rag-chatbot-client.js  # Standalone JavaScript client
    RAGChatbot.jsx         # React component
    RAGChatbot.css         # Component styles
    RAGChatbotWrapper.jsx  # Docusaurus wrapper
    index.html            # Example HTML integration
  docusaurus-plugin/
    index.js              # Docusaurus plugin
    package.json          # Plugin package file
    src/
      client/
        module.js         # Client-side initialization
      components/
        RAGChatbot.jsx    # React component
        RAGChatbot.css    # Component styles
  setup.sh              # Linux/Mac setup script
  setup.ps1             # Windows setup script
```

## Setup Instructions

### 1. Install dependencies:
   ```bash
   cd rag-book-chatbot/backend
   pip install -r requirements.txt
   ```

### 2. Set up environment:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env to add your API keys (optional, fallback to local models available)
   ```

### 3. Place your book:
   - Put your PDF book in the `data/` folder as `book.pdf`
   - Or update the `BOOK_PATH` in `.env` to point to your book

### 4. Process your book (create Qdrant vector database):
   ```bash
   python qdrant_ingest.py
   ```
   This will convert your PDF into searchable chunks and store them in a Qdrant database.

### 5. Start the chatbot:
   ```bash
   python qdrant_chat.py
   ```
   The chatbot will be available at `http://localhost:8000`

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `GOOGLE_API_KEY`: Your Google Gemini API key (optional)
- `QDRANT_URL`: Qdrant database URL (for cloud deployment)
- `QDRANT_API_KEY`: Qdrant API key (for cloud deployment)
- `QDRANT_COLLECTION_NAME`: Name of the collection in Qdrant (default: book_collection)
- `LOCAL_QDRANT_PATH`: Local path for Qdrant data (default: ./qdrant_data)
- `BOOK_PATH`: Path to your book PDF (default: ./../data/book.pdf)

## API Endpoints

- `GET /` - Health check
- `POST /ask` - Ask a question about the book
  - Request body: `{"question": "Your question here"}`
  - Response: `{"answer": "Answer from book", "source_chunks": ["relevant text chunks"]}`
- `GET /health` - Health check with Qdrant status

## Example Usage

After starting the server, you can test with curl:

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is RAG?"}'
```

Or use the browser at `http://localhost:8000/docs` to access the interactive API documentation.

## Web Integration

### For Docusaurus Websites
1. Update your `docusaurus.config.ts` to include the plugin (as shown in this repo)
2. The chatbot will automatically appear on all pages

### For Other Websites
Include the JavaScript client:
```html
<script src="rag-chatbot-client.js"></script>
```

## Important Notes

- If the answer is not in the book, the bot will respond with: "Is book me ye information nahi hai"
- Make sure your book is in the data folder before running qdrant_ingest.py
- The first run will take some time as it processes the PDF and creates embeddings
- If no API keys are provided, the system will use local models as fallback
- Qdrant can run locally or in the cloud - configure in .env