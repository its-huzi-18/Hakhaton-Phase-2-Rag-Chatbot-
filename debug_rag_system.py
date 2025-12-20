#!/usr/bin/env python3
"""
Debug script for RAG Chatbot System
This script helps diagnose issues with the RAG system and verify it's working properly.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")

    required_vars = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "TARGET_URL"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("   Please set these variables in your .env file or environment")
        return False

    print("✅ All required environment variables are set")
    return True

def check_api_connection():
    """Check if the API server is running and accessible"""
    print("\n🔍 Checking API connection...")

    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API server is running")
            print(f"   Status: {health_data['status']}")
            print(f"   Collections: {health_data['collections']}")
            return True, health_data['collections']
        else:
            print(f"❌ API server returned status {response.status_code}")
            return False, []
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server at http://localhost:8000")
        print("   Make sure the API server is running with: python backend/start_api.py")
        return False, []
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return False, []

def check_collections():
    """Check what collections exist in the vector database"""
    print("\n🔍 Checking collections in vector database...")

    try:
        response = requests.get("http://localhost:8000/collections", timeout=10)
        if response.status_code == 200:
            collections_data = response.json()
            print(f"✅ Collections found: {collections_data['collections']}")

            if not collections_data['collections']:
                print("⚠️  No collections found. You need to process your book content first.")
                print("   Run: python backend/process_book.py")
                return False, collections_data['collections']

            return True, collections_data['collections']
        else:
            print(f"❌ Collections endpoint failed with status {response.status_code}")
            return False, []
    except Exception as e:
        print(f"❌ Error checking collections: {e}")
        return False, []

def test_query():
    """Test a sample query to see if the RAG system works"""
    print("\n🔍 Testing sample query...")

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
            print(f"   Response: {result['response'][:200]}...")
            print(f"   Sources found: {result['total_chunks']}")

            if result['total_chunks'] > 0:
                print("✅ Content was found and used for response")
                print("\nFull response preview:")
                print("-" * 50)
                print(result['response'])
                print("-" * 50)
                return True
            else:
                print("⚠️  Query successful but no content was found in the database")
                print("   This means the book content hasn't been processed yet")
                return False
        else:
            print(f"❌ Query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during query test: {e}")
        return False

def check_target_url():
    """Check if the target URL is accessible"""
    print("\n🔍 Checking if target URL is accessible...")

    target_url = os.getenv("TARGET_URL")
    if not target_url:
        print("❌ TARGET_URL not set in environment variables")
        return False

    print(f"   Checking: {target_url}")

    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code == 200:
            print("✅ Target URL is accessible")
            # Check if it contains text content
            content_type = response.headers.get('content-type', '')
            if 'text' in content_type or 'html' in content_type:
                print("✅ Target URL contains text/HTML content")
                return True
            else:
                print(f"⚠️  Target URL content type is {content_type}, might not be text-based")
                return True  # Still accessible, just different content type
        else:
            print(f"❌ Target URL returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing target URL: {e}")
        print("   Make sure your book website is publicly accessible")
        return False

def run_debugging():
    """Run comprehensive debugging of the RAG system"""
    print("="*60)
    print("RAG CHATBOT SYSTEM DEBUGGING")
    print("="*60)

    # Check environment
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ Environment check failed. Please set up your environment variables.")
        return False

    # Check target URL
    url_ok = check_target_url()
    if not url_ok:
        print("\n❌ Target URL check failed. Make sure your book website is accessible.")
        return False

    # Check API connection
    api_ok, collections = check_api_connection()
    if not api_ok:
        print("\n❌ API connection failed. Please start the API server.")
        print("   Start with: python backend/start_api.py")
        return False

    # Check collections
    collections_ok, collections = check_collections()

    if collections_ok and collections:
        # If collections exist, test a query
        query_ok = test_query()
        if query_ok:
            print("\n" + "="*60)
            print("🎉 DEBUGGING COMPLETE!")
            print("✅ Your RAG system appears to be working correctly")
            print("✅ You should be able to ask questions about your book")
            print("="*60)
            return True
        else:
            print("\n❌ Query test failed. There might be an issue with content retrieval.")
            return False
    else:
        print("\n" + "="*60)
        print("📚 CONTENT PROCESSING NEEDED")
        print("Your API is running but no content has been processed yet.")
        print("\nTo fix this:")
        print("1. Run: python backend/process_book.py")
        print("   This will crawl your book website and store content in the vector database")
        print("2. After processing, test again with this script")
        print("="*60)
        return False

def show_setup_steps():
    """Show the complete setup steps"""
    print("\n" + "="*60)
    print("COMPLETE SETUP STEPS")
    print("="*60)
    print("1. Install dependencies:")
    print("   cd backend && pip install -r requirements.txt")
    print("\n2. Set up environment variables in a .env file:")
    print("   COHERE_API_KEY=your_cohere_api_key")
    print("   QDRANT_URL=your_qdrant_url")
    print("   QDRANT_API_KEY=your_qdrant_api_key")
    print("   TARGET_URL=https://your-book-website.com")
    print("\n3. Process your book content (this is the crucial step!):")
    print("   python backend/process_book.py")
    print("   This will crawl your book website and store content in the vector database")
    print("\n4. Start the API server:")
    print("   python backend/start_api.py")
    print("\n5. Test the system:")
    print("   python debug_rag_system.py")
    print("="*60)

if __name__ == "__main__":
    success = run_debugging()

    if not success:
        show_setup_steps()
        sys.exit(1)
    else:
        print("\n🚀 Your RAG chatbot system is ready to use!")
        print("The chatbot should now be able to answer questions about your book content!")