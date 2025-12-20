#!/usr/bin/env python3
"""
RAG Chatbot API Implementation
This script provides API endpoints for querying the RAG knowledge base.
"""

import os
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest
from qdrant_client.http import models
import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY not found in environment variables")
co = cohere.Client(cohere_api_key)

# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL or QDRANT_API_KEY not found in environment variables")

client = QdrantClient(
    url=qdrant_url.replace("https://", "").replace(":6333", ""),
    api_key=qdrant_api_key,
    port=6333,
    https=True
)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for querying the RAG knowledge base",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    collection_name: str = "book_knowledge_base"

class QueryResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict[str, Any]]
    total_chunks: int

class HealthResponse(BaseModel):
    status: str
    collections: List[str]

def embed_query(query: str) -> List[float]:
    """
    Generate embedding for a query string using Cohere

    Args:
        query (str): Query text to embed

    Returns:
        List[float]: Embedding vector
    """
    logger.info(f"Generating embedding for query: {query[:50]}...")

    try:
        response = co.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query"
        )

        embedding = response.embeddings[0]  # Get the first (and only) embedding
        logger.info(f"Generated embedding with {len(embedding)} dimensions")
        return embedding

    except Exception as e:
        logger.error(f"Error generating query embedding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating query embedding: {str(e)}")

def search_similar_chunks(query_embedding: List[float], collection_name: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar text chunks in Qdrant

    Args:
        query_embedding (List[float]): Query embedding vector
        collection_name (str): Name of the collection to search in
        top_k (int): Number of results to return

    Returns:
        List[Dict[str, Any]]: List of similar chunks with metadata
    """
    logger.info(f"Searching for similar chunks in collection '{collection_name}', top_k={top_k}")

    try:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        results = []
        for point in search_result:
            results.append({
                "text": point.payload.get("text", ""),
                "metadata": point.payload.get("metadata", {}),
                "score": point.score
            })

        logger.info(f"Found {len(results)} similar chunks")
        return results

    except Exception as e:
        logger.error(f"Error searching in Qdrant: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching in Qdrant: {str(e)}")

def generate_response(query: str, context_chunks: List[Dict[str, Any]]) -> str:
    """
    Generate a response using Cohere Chat API based on the query and context

    Args:
        query (str): User query
        context_chunks (List[Dict[str, Any]]): Context chunks to use for response generation

    Returns:
        str: Generated response
    """
    logger.info(f"Generating response for query: {query[:50]}...")

    # Check if we have any context chunks
    if not context_chunks or all(len(chunk["text"].strip()) == 0 for chunk in context_chunks):
        logger.warning("No context chunks available for the query")
        return ("I couldn't find any relevant information in the book for your question. "
                "Please try rephrasing your question or ask about a different topic from the book. "
                "Make sure the book content has been processed and indexed in the vector database.")

    # Combine context chunks into a single context string
    context = "\n\n".join([chunk["text"] for chunk in context_chunks if chunk["text"].strip()])

    # Create a message for the chat model
    message = f"""
    You are an AI assistant for the 'Advanced Robotics & AI' book.
    Answer the user's question based on the context provided below.

    Context information is below:
    ---------------------
    {context}
    ---------------------

    User Query: {query}

    Provide a comprehensive, helpful, and accurate answer based on the context.
    If the context contains specific examples, definitions, or explanations, include them in your response.
    If the context doesn't contain the information needed to answer the question, say so clearly.
    Structure your response with clear explanations and use book content directly when possible.
    """

    try:
        response = co.chat(
            message=message,
            max_tokens=1000,  # Increased to allow more comprehensive answers
            temperature=0.4   # Slightly increased for more engaging responses
        )

        generated_text = response.text.strip()
        logger.info(f"Generated response with {len(generated_text)} characters")
        return generated_text

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/")
def root():
    """Root endpoint for health check"""
    return {"message": "RAG Chatbot API is running"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    try:
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]
        return HealthResponse(status="healthy", collections=collection_names)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    """
    Query the RAG knowledge base

    Args:
        request (QueryRequest): Query request with query text and parameters

    Returns:
        QueryResponse: Response with answer and sources
    """
    logger.info(f"Received query: {request.query[:50]}...")

    # Generate embedding for the query
    query_embedding = embed_query(request.query)

    # Search for similar chunks in the vector database
    similar_chunks = search_similar_chunks(
        query_embedding,
        request.collection_name,
        request.top_k
    )

    # Generate a response using the context
    response_text = generate_response(request.query, similar_chunks)

    # Prepare the response
    response = QueryResponse(
        query=request.query,
        response=response_text,
        sources=[{
            "text": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],  # Truncate for response
            "source_url": chunk["metadata"].get("source_url", ""),
            "score": chunk["score"]
        } for chunk in similar_chunks],
        total_chunks=len(similar_chunks)
    )

    logger.info(f"Query processed successfully, returning {len(similar_chunks)} sources")
    return response

@app.get("/collections")
def get_collections():
    """Get list of available collections"""
    try:
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]
        return {"collections": collection_names}
    except Exception as e:
        logger.error(f"Error getting collections: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting collections")

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)