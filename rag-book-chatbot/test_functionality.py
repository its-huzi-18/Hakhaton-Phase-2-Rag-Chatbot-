import os
import subprocess
import sys
import time
import requests
from pathlib import Path

def test_setup():
    """Test if the setup is correct"""
    print("Testing RAG Chatbot setup...")

    # Check if backend directory exists
    backend_path = Path("rag-book-chatbot/backend")
    if not backend_path.exists():
        print("[ERROR] Backend directory not found")
        return False

    # Check if required files exist
    required_files = [
        "qdrant_ingest.py",
        "qdrant_chat.py",
        "requirements.txt",
        ".env.example"
    ]

    for file in required_files:
        file_path = backend_path / file
        if not file_path.exists():
            print(f"[ERROR] Required file missing: {file}")
            return False

    print("[SUCCESS] All required files present")

    # Check if data directory exists and has a PDF
    data_path = Path("rag-book-chatbot/data")
    if not data_path.exists():
        print("[ERROR] Data directory not found")
        return False

    pdf_files = list(data_path.glob("*.pdf"))
    if not pdf_files:
        print("[WARNING] No PDF files found in data directory - this is required for ingestion")

    print("[SUCCESS] Data directory exists")
    return True

def test_dependencies():
    """Test if dependencies can be imported"""
    print("\nTesting dependencies...")

    try:
        import fastapi
        import uvicorn
        import langchain
        import qdrant_client
        import python_dotenv
        import pypdf
        print("[SUCCESS] Dependencies can be imported")
        return True
    except ImportError as e:
        print(f"[ERROR] Dependency import error: {e}")
        return False

def test_environment():
    """Test if environment is configured"""
    print("\nTesting environment...")

    env_path = Path("rag-book-chatbot/backend/.env")
    if not env_path.exists():
        print("[WARNING] .env file not found - creating from example")
        example_path = Path("rag-book-chatbot/backend/.env.example")
        if example_path.exists():
            import shutil
            shutil.copy(example_path, env_path)
            print("[SUCCESS] Created .env from example")
        else:
            print("[ERROR] .env.example not found")
            return False

    print("[SUCCESS] Environment file exists")
    return True

def run_ingestion_test():
    """Test the ingestion process (without actually running it to avoid long execution)"""
    print("\nTesting ingestion configuration...")

    # Check if book.pdf exists
    book_path = Path("rag-book-chatbot/data/book.pdf")
    if not book_path.exists():
        print("[WARNING] book.pdf not found in data directory")
        print("   Please place your book PDF in rag-book-chatbot/data/ as book.pdf")
        return False

    print("[SUCCESS] Book PDF found")
    return True

def test_api_connection():
    """Test if API is running"""
    print("\nTesting API connection...")

    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] API is running: {data}")
            return True
        else:
            print(f"[ERROR] API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] API is not running or not accessible at http://localhost:8000")
        return False
    except Exception as e:
        print(f"[ERROR] Error connecting to API: {e}")
        return False

def run_full_test():
    """Run a comprehensive test of the RAG chatbot functionality"""
    print("[INFO] Starting comprehensive RAG Chatbot functionality test...\n")

    tests = [
        ("Setup verification", test_setup),
        ("Dependency check", test_dependencies),
        ("Environment check", test_environment),
        ("Ingestion configuration", run_ingestion_test),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n[TEST] Running {test_name}...")
        result = test_func()
        results.append((test_name, result))

    print(f"\n[RESULTS] Test Results:")
    all_passed = True
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} - {test_name}")
        if not result:
            all_passed = False

    if all_passed:
        print(f"\n[SUCCESS] All tests passed! Your RAG Chatbot system is ready.")
        print("\nTo start using the system:")
        print("1. Make sure your book PDF is in rag-book-chatbot/data/")
        print("2. Run 'python qdrant_ingest.py' to process your book")
        print("3. Run 'python qdrant_chat.py' to start the API server")
        print("4. The chatbot will be available at http://localhost:8000")
    else:
        print(f"\n[ERROR] Some tests failed. Please address the issues above.")

    return all_passed

if __name__ == "__main__":
    run_full_test()