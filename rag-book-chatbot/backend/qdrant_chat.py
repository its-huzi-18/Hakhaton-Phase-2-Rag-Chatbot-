import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from langchain_community.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Book RAG Chatbot with Qdrant",
    description="A chatbot that answers questions based only on the content of a specific book using Qdrant vector database",
    version="2.0.0"
)

# Define request/response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    source_chunks: List[str] = []

# Global variable to store the Qdrant vector store
qdrant_store = None

def initialize_qdrant_store():
    """
    Initialize the Qdrant vector store when the application starts
    """
    global qdrant_store

    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_collection")
    qdrant_url = os.getenv("QDRANT_URL")  # Optional - if None, will use local
    qdrant_api_key = os.getenv("QDRANT_API_KEY")  # Optional - if None, will use local
    local_path = os.getenv("LOCAL_QDRANT_PATH", "./qdrant_data")

    # Initialize embeddings model
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Determine if using local or cloud Qdrant
    if qdrant_url:
        print(f"Connecting to Qdrant cloud: {qdrant_url}")
        # Connect to cloud Qdrant
        qdrant_store = Qdrant(
            url=qdrant_url,
            api_key=qdrant_api_key,
            collection_name=collection_name,
            embedding_function=embeddings
        )
    else:
        print(f"Using local Qdrant: {local_path}")
        # Connect to local Qdrant
        qdrant_store = Qdrant.from_params(
            path=local_path,
            collection_name=collection_name,
            embedding_function=embeddings
        )

    print(f"Qdrant vector store loaded from collection: {collection_name}")

def format_docs(docs):
    """
    Format retrieved documents into a string
    """
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    """
    Create the RAG (Retrieval-Augmented Generation) chain
    This connects the document retriever with the LLM (either OpenAI or Gemini)
    """
    # Determine which LLM to use based on available API keys
    llm = None

    # Check for OpenAI API key first
    if os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI GPT model")
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    # Check for Google API key next
    elif os.getenv("GOOGLE_API_KEY"):
        print("Using Google Gemini model")
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.1,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    else:
        # Fallback to a local model if no API keys are provided
        print("No API keys found, using local model as fallback")
        from langchain_community.llms import HuggingFaceEndpoint
        llm = HuggingFaceEndpoint(
            repo_id="google/flan-t5-small",
            temperature=0.1,
            max_new_tokens=512
        )

    # Create the prompt template for the LLM
    template = """You are a helpful assistant that answers questions based only on the provided context from a book.
    If the answer is not available in the provided context, respond with exactly: "Is book me ye information nahi hai".

    Context: {context}

    Question: {question}

    Answer:"""

    prompt = PromptTemplate.from_template(template)

    # Set up the retriever to get relevant documents from the Qdrant vector store
    retriever = qdrant_store.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 most relevant chunks

    # Create the RAG chain
    # This chain: takes question -> retrieves relevant docs -> formats them -> sends to LLM -> gets answer
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs when the application starts
    """
    global qdrant_store
    try:
        initialize_qdrant_store()

        # Test that we can create the RAG chain
        _ = create_rag_chain()

        print("Application started successfully!")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise

@app.get("/")
async def root():
    """
    Root endpoint to check if the service is running
    """
    return {"message": "Book RAG Chatbot with Qdrant is running!", "status": "ok"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Endpoint to ask a question and get an answer based on the book content

    Args:
        request (QuestionRequest): Request containing the question

    Returns:
        AnswerResponse: Response containing the answer and source chunks
    """
    global qdrant_store

    if qdrant_store is None:
        raise HTTPException(status_code=500, detail="Qdrant vector store not initialized")

    try:
        # Create the RAG chain
        rag_chain = create_rag_chain()

        # Get the answer from the RAG chain
        answer = rag_chain.invoke(request.question)

        # Also retrieve the source documents to show where the answer came from
        retriever = qdrant_store.as_retriever(search_kwargs={"k": 3})
        source_docs = retriever.get_relevant_documents(request.question)
        source_chunks = [doc.page_content for doc in source_docs]

        return AnswerResponse(answer=answer, source_chunks=source_chunks)

    except Exception as e:
        print(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "qdrant_store_loaded": qdrant_store is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)