#!/bin/bash

# RAG Chatbot Deployment Script
# This script helps automate the deployment process

set -e  # Exit on any error

echo "========================================="
echo "RAG Chatbot Deployment Script"
echo "========================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists railway; then
    echo "❌ Railway CLI not found. Please install it:"
    echo "   npm install -g @railway/cli"
    exit 1
fi

if ! command_exists git; then
    echo "❌ Git not found. Please install Git."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Function to process book content
process_content() {
    echo "Processing book content..."
    cd backend
    if [ ! -f ".env" ]; then
        echo "❌ .env file not found in backend directory"
        echo "Please create backend/.env with your API keys"
        exit 1
    fi

    python process_book.py
    cd ..
    echo "✅ Book content processed"
}

# Function to deploy API to Railway
deploy_api() {
    echo "Deploying API to Railway..."
    cd backend

    # Check if Railway project is initialized
    if [ ! -f ".railway" ]; then
        echo "Initializing Railway project..."
        railway init
    fi

    echo "Deploying to Railway..."
    railway up
    cd ..
    echo "✅ API deployed to Railway"
}

# Function to show deployment summary
show_summary() {
    echo ""
    echo "========================================="
    echo "DEPLOYMENT SUMMARY"
    echo "========================================="
    echo ""
    echo "1. API Deployment:"
    echo "   - Check your Railway dashboard for the API URL"
    echo "   - It should look like: https://your-project.up.railway.app"
    echo ""
    echo "2. Frontend Integration:"
    echo "   - Update chatbot_widget.js with your Railway API URL"
    echo "   - Deploy your Docusaurus site to Vercel"
    echo ""
    echo "3. Test the system:"
    echo "   - Visit your Vercel website"
    echo "   - Use the chatbot to ask questions about your book"
    echo ""
    echo "For detailed instructions, see: DEPLOYMENT_COMPLETE_GUIDE.md"
    echo "========================================="
}

# Main deployment flow
main() {
    echo ""
    echo "What would you like to do?"
    echo "1) Process book content only"
    echo "2) Deploy API to Railway only"
    echo "3) Process content and deploy API"
    echo "4) Show deployment summary"
    echo ""
    read -p "Enter your choice (1-4): " choice

    case $choice in
        1)
            process_content
            ;;
        2)
            deploy_api
            ;;
        3)
            process_content
            deploy_api
            ;;
        4)
            show_summary
            ;;
        *)
            echo "Invalid choice. Please enter 1, 2, 3, or 4."
            exit 1
            ;;
    esac

    if [ "$choice" != "4" ]; then
        show_summary
    fi
}

# Run the main function
main "$@"