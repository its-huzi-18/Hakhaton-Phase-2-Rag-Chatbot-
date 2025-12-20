# RAG Chatbot for Book Website

This project provides a complete Retrieval-Augmented Generation (RAG) chatbot system that allows users to ask questions about your book content and receive accurate answers based on the book's text.

## Features

- **Content Crawling**: Automatically extracts content from your book website
- **Vector Storage**: Stores content in a vector database for semantic search
- **AI-Powered Responses**: Generates contextual answers using AI
- **Frontend Widget**: Easy-to-integrate chatbot widget for your website
- **Persistent Chat History**: Remembers conversations using localStorage

## Prerequisites

Before setting up the RAG chatbot, you'll need:

1. **Cohere API Key**: Get one from [Cohere](https://cohere.ai/)
2. **Qdrant Vector Database**: Either hosted or local instance
3. **Python 3.8+**: For the backend services
4. **Your Book Website URL**: The deployed website containing your book content

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   TARGET_URL=https://your-book-website-url.com
   ```

### 2. Process Your Book Content

Run the content processing script to crawl your book website and store content in the vector database:

```bash
python process_book.py
```

This will:
- Crawl all pages on your book website
- Extract text content from each page
- Create embeddings using Cohere
- Store content in the Qdrant vector database

### 3. Start the API Server

Start the RAG chatbot API server:

```bash
python start_api.py
```

The API will be available at `http://localhost:8000`

### 4. Frontend Integration

To add the chatbot to your book website:

1. Copy the `chatbot_widget.js` file to your website's static assets
2. Add the following script tag to your HTML pages:
   ```html
   <script src="path/to/chatbot_widget.js"></script>
   ```
3. The chatbot will appear as a floating widget on the bottom-right of your pages

### 5. Complete Workflow

Alternatively, you can run the complete workflow with a single command:

```bash
python run_all.py
```

This will guide you through processing content and starting the API server.

## Configuration

### Backend Configuration

- `TARGET_URL`: URL of your book website to crawl
- `PORT`: Port for the API server (default: 8000)
- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL` and `QDRANT_API_KEY`: Qdrant database credentials

### Frontend Configuration

The chatbot widget can be customized by modifying these options in `chatbot_widget.js`:

- `title`: Chatbot window title
- `welcomeMessage`: Initial message when chat opens
- `placeholder`: Input field placeholder text
- `botAvatar` and `userAvatar`: Emoji or text for avatars
- `primaryColor`: Brand color for the chatbot

## API Endpoints

- `GET /`: Health check
- `GET /health`: System health status
- `GET /collections`: List available collections
- `POST /query`: Query the RAG system

Example query request:
```json
{
  "query": "What is the main concept of robotics?",
  "top_k": 3
}
```

## Testing

Test the API functionality:
```bash
python test_api.py
```

## Deployment

### For Production

1. **Environment Variables**: Use secure methods to store API keys
2. **Qdrant Database**: Use a hosted Qdrant service or secure your self-hosted instance
3. **API Server**: Deploy using a WSGI server like Gunicorn
4. **Frontend**: Host the chatbot widget on your website's CDN

### Docker (Optional)

A Dockerfile is included for containerized deployment:

```bash
docker build -t rag-chatbot .
docker run -p 8000:8000 rag-chatbot
```

## Troubleshooting

- **No content in responses**: Make sure you ran `process_book.py` after setting up your API keys
- **API connection errors**: Verify your Qdrant and Cohere API keys are correct
- **CORS issues**: The API allows all origins by default, but you may want to restrict this in production
- **Crawling issues**: Ensure your book website is publicly accessible

## Free Options

For completely free setup:

1. **Cohere API**: Cohere offers a free tier with limited requests
2. **Qdrant**: Can run locally for free or use Qdrant Cloud free tier
3. **Hosting**: Deploy to platforms like Vercel, Netlify, or Heroku (with some limitations)

## Architecture

```
[User] ↔ [Frontend Widget] ↔ [API Server] ↔ [Qdrant Vector DB]
                    ↓
             [Cohere AI Services]
```

The system works by:
1. Crawling your book website content
2. Creating embeddings of text chunks using Cohere
3. Storing embeddings in Qdrant vector database
4. On query, finding relevant content using vector similarity
5. Generating responses using Cohere's language model with retrieved context