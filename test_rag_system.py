#!/usr/bin/env python3
"""
Complete RAG Chatbot System Test
This script tests the entire RAG chatbot pipeline from content processing to API response.
"""

import os
import sys
import time
import subprocess
import requests
import threading
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def check_environment():
    """Check if required environment variables are set"""
    print("Checking environment variables...")

    required_vars = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "TARGET_URL"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment")
        return False

    print("✅ All required environment variables are set")
    return True

def test_api_connection():
    """Test if the API server is running and accessible"""
    print("\nTesting API connection...")

    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API server is running")
            print(f"   Status: {health_data['status']}")
            print(f"   Collections: {health_data['collections']}")
            return True
        else:
            print(f"❌ API server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server at http://localhost:8000")
        print("   Make sure the API server is running with: python start_api.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return False

def test_content_processing():
    """Test the content processing pipeline"""
    print("\nTesting content processing pipeline...")

    try:
        # Import and run the process_book function
        sys.path.append(str(backend_dir))
        from process_book import process_book

        print("   Running content processing (this may take a few minutes)...")
        print("   This will crawl your book website and store content in the vector database")

        # Run the processing function
        process_book()

        print("✅ Content processing completed successfully")
        return True
    except ImportError as e:
        print(f"❌ Could not import process_book: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error during content processing: {e}")
        return False

def test_query_functionality():
    """Test the query functionality of the API"""
    print("\nTesting query functionality...")

    try:
        query_data = {
            "query": "What is this book about?",
            "top_k": 3
        }

        response = requests.post(
            "http://localhost:8000/query",
            json=query_data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Query successful")
            print(f"   Query: {result['query']}")
            print(f"   Response length: {len(result['response'])} characters")
            print(f"   Sources found: {result['total_chunks']}")

            if result['total_chunks'] > 0:
                print("✅ Content was found and returned")
                return True
            else:
                print("⚠️  Query successful but no content was found in the database")
                print("   This might be because the content hasn't been processed yet")
                return False
        else:
            print(f"❌ Query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during query test: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive tests on the RAG system"""
    print("="*60)
    print("RAG CHATBOT SYSTEM TEST")
    print("="*60)

    # Check environment first
    if not check_environment():
        print("\n❌ Environment check failed. Please set up your environment variables.")
        return False

    # Test API connection
    api_connected = test_api_connection()

    if not api_connected:
        print("\n❌ API connection failed. Please start the API server.")
        print("   Start with: python backend/start_api.py")
        return False

    # Test content processing
    print("\n" + "="*60)
    print("CONTENT PROCESSING TEST")
    print("="*60)
    content_processed = test_content_processing()

    if content_processed:
        print("\n" + "="*60)
        print("QUERY FUNCTIONALITY TEST")
        print("="*60)
        query_works = test_query_functionality()

        if query_works:
            print("\n" + "="*60)
            print("🎉 ALL TESTS PASSED!")
            print("✅ Your RAG chatbot system is working correctly")
            print("✅ Content is processed and stored in the vector database")
            print("✅ API is responding to queries with relevant information")
            print("="*60)
            return True
        else:
            print("\n❌ Query functionality test failed")
            return False
    else:
        print("\n❌ Content processing test failed")
        print("   Make sure your TARGET_URL is accessible and contains text content")
        return False

def show_setup_instructions():
    """Show setup instructions if tests fail"""
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    print("1. Install dependencies:")
    print("   cd backend && pip install -r requirements.txt")
    print("\n2. Set up environment variables in a .env file:")
    print("   COHERE_API_KEY=your_cohere_api_key")
    print("   QDRANT_URL=your_qdrant_url")
    print("   QDRANT_API_KEY=your_qdrant_api_key")
    print("   TARGET_URL=https://your-book-website.com")
    print("\n3. Process your book content:")
    print("   python backend/process_book.py")
    print("\n4. Start the API server:")
    print("   python backend/start_api.py")
    print("\n5. Add the chatbot to your website:")
    print("   Include chatbot_widget.js in your HTML")
    print("="*60)

if __name__ == "__main__":
    success = run_comprehensive_test()

    if not success:
        show_setup_instructions()
        sys.exit(1)
    else:
        print("\n🚀 Your RAG chatbot is ready to use!")
        print("Add the chatbot widget to your website and start answering questions about your book!")