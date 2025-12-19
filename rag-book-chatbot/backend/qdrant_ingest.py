import os
import argparse
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_qdrant import Qdrant

# Load environment variables from .env file
load_dotenv()

def load_and_split_pdf(pdf_path):
    """
    Load PDF document and split it into chunks

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        list: List of document chunks
    """
    print(f"Loading PDF from: {pdf_path}")

    # Load the PDF document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages from PDF")

    # Split the document into smaller chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Each chunk will have max 1000 characters
        chunk_overlap=200,    # Overlap between chunks to maintain context
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} text chunks")

    return texts

def create_qdrant_vector_store(texts, collection_name, qdrant_url=None, qdrant_api_key=None, local_path=None):
    """
    Create a Qdrant vector store from the text chunks using embeddings

    Args:
        texts (list): List of document chunks
        collection_name (str): Name of the Qdrant collection
        qdrant_url (str): URL to Qdrant server (if using cloud)
        qdrant_api_key (str): API key for Qdrant (if using cloud)
        local_path (str): Local path to store Qdrant data (if using local)
    """
    print("Creating embeddings and Qdrant vector store...")

    # Initialize embeddings model (using a sentence transformer model)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Determine if using local or cloud Qdrant
    if local_path:
        print(f"Using local Qdrant at: {local_path}")
        client = QdrantClient(path=local_path)
    else:
        print(f"Connecting to Qdrant cloud: {qdrant_url}")
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=True  # Use gRPC for better performance
        )

    # Check if collection exists, if not create it
    try:
        client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists, clearing it...")
        client.delete_collection(collection_name)
    except:
        print(f"Collection '{collection_name}' does not exist, creating it...")

    # Create the collection with appropriate vector configuration
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384,  # Size of the embeddings from all-MiniLM-L6-v2
            distance=models.Distance.COSINE
        ),
    )

    # Create Qdrant vector store from documents and embeddings
    qdrant_store = Qdrant.from_documents(
        texts,
        embeddings,
        url=qdrant_url,
        api_key=qdrant_api_key,
        path=local_path,
        collection_name=collection_name,
        force_recreate=True  # Recreate the collection
    )

    print(f"Qdrant vector store created with collection: {collection_name}")
    return qdrant_store

def main():
    """
    Main function to run the ingestion process
    """
    # Get paths from environment variables
    book_path = os.getenv("BOOK_PATH", "./../data/book.pdf")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_collection")
    qdrant_url = os.getenv("QDRANT_URL")  # Optional - if None, will use local
    qdrant_api_key = os.getenv("QDRANT_API_KEY")  # Optional - if None, will use local
    local_path = os.getenv("LOCAL_QDRANT_PATH", "./qdrant_data")

    # Check if the book file exists
    if not os.path.exists(book_path):
        print(f"Error: Book file not found at {book_path}")
        print("Please place your book.pdf file in the data folder.")
        return

    # Determine if using local or cloud Qdrant
    if qdrant_url:
        print(f"Using Qdrant cloud: {qdrant_url}")
        persist_path = None
    else:
        print(f"Using local Qdrant: {local_path}")
        persist_path = local_path

    # Load and split the PDF
    texts = load_and_split_pdf(book_path)

    # Create the Qdrant vector store
    qdrant_store = create_qdrant_vector_store(
        texts,
        collection_name,
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key,
        local_path=persist_path
    )

    print("\nIngestion completed successfully!")
    print(f"Your book has been processed and stored in Qdrant collection: {collection_name}")
    print("You can now run the chatbot to ask questions about the book.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a PDF book into a Qdrant vector database")
    parser.add_argument("--book-path", help="Path to the PDF book file")
    parser.add_argument("--collection-name", help="Qdrant collection name")
    parser.add_argument("--qdrant-url", help="Qdrant server URL (for cloud)")
    parser.add_argument("--qdrant-api-key", help="Qdrant API key (for cloud)")
    parser.add_argument("--local-path", help="Local path for Qdrant data (for local)")

    args = parser.parse_args()

    # Override environment variables if command line arguments are provided
    if args.book_path:
        os.environ["BOOK_PATH"] = args.book_path
    if args.collection_name:
        os.environ["QDRANT_COLLECTION_NAME"] = args.collection_name
    if args.qdrant_url:
        os.environ["QDRANT_URL"] = args.qdrant_url
    if args.qdrant_api_key:
        os.environ["QDRANT_API_KEY"] = args.qdrant_api_key
    if args.local_path:
        os.environ["LOCAL_QDRANT_PATH"] = args.local_path

    main()