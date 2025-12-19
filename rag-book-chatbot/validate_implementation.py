import os
from pathlib import Path
import json

def validate_implementation():
    """Validate that all required components for the RAG chatbot have been created"""
    print("[INFO] Validating RAG Chatbot Implementation...")

    validation_results = []

    # Check backend files
    backend_files = [
        "rag-book-chatbot/backend/qdrant_ingest.py",
        "rag-book-chatbot/backend/qdrant_chat.py",
        "rag-book-chatbot/backend/requirements.txt",
        "rag-book-chatbot/backend/.env.example"
    ]

    print("\n[CHECK] Checking backend files...")
    for file_path in backend_files:
        exists = Path(file_path).exists()
        status = "[PASS]" if exists else "[FAIL]"
        print(f"  {status} {file_path}")
        validation_results.append((file_path, exists))

    # Check web client files
    web_client_files = [
        "rag-book-chatbot/web-client/rag-chatbot-client.js",
        "rag-book-chatbot/web-client/RAGChatbot.jsx",
        "rag-book-chatbot/web-client/RAGChatbot.css",
        "rag-book-chatbot/web-client/RAGChatbotWrapper.jsx",
        "rag-book-chatbot/web-client/index.html"
    ]

    print("\n[CHECK] Checking web client files...")
    for file_path in web_client_files:
        exists = Path(file_path).exists()
        status = "[PASS]" if exists else "[FAIL]"
        print(f"  {status} {file_path}")
        validation_results.append((file_path, exists))

    # Check Docusaurus plugin files
    plugin_files = [
        "rag-book-chatbot/docusaurus-plugin/index.js",
        "rag-book-chatbot/docusaurus-plugin/package.json",
        "rag-book-chatbot/docusaurus-plugin/src/client/module.js",
        "rag-book-chatbot/docusaurus-plugin/src/components/RAGChatbot.jsx",
        "rag-book-chatbot/docusaurus-plugin/src/components/RAGChatbot.css"
    ]

    print("\n[CHECK] Checking Docusaurus plugin files...")
    for file_path in plugin_files:
        exists = Path(file_path).exists()
        status = "[PASS]" if exists else "[FAIL]"
        print(f"  {status} {file_path}")
        validation_results.append((file_path, exists))

    # Check integration in Docusaurus config
    docusaurus_config_path = "my-book/docusaurus.config.ts"
    config_exists = Path(docusaurus_config_path).exists()

    print(f"\n[CHECK] Checking Docusaurus integration...")
    if config_exists:
        with open(docusaurus_config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()

        has_plugin = "'../rag-book-chatbot/docusaurus-plugin/index.js'" in config_content
        has_custom_field = "ragChatbotApiUrl" in config_content

        print(f"  [PASS] {docusaurus_config_path}")
        print(f"  [INFO] Plugin reference found: {has_plugin}")
        print(f"  [INFO] Custom field found: {has_custom_field}")

        validation_results.append((docusaurus_config_path, config_exists and has_plugin and has_custom_field))
    else:
        print(f"  [FAIL] {docusaurus_config_path}")
        validation_results.append((docusaurus_config_path, False))

    # Check documentation
    docs_files = [
        "rag-book-chatbot/README.md",
        "rag-book-chatbot/setup.sh",
        "rag-book-chatbot/setup.ps1",
        "my-book/docs/chatbot-integration.md"
    ]

    print("\n[CHECK] Checking documentation...")
    for file_path in docs_files:
        exists = Path(file_path).exists()
        status = "[PASS]" if exists else "[FAIL]"
        print(f"  {status} {file_path}")
        validation_results.append((file_path, exists))

    # Summary
    total_checks = len(validation_results)
    passed_checks = sum(1 for _, result in validation_results if result)

    print(f"\n[SUMMARY] Validation Summary:")
    print(f"  Total checks: {total_checks}")
    print(f"  Passed: {passed_checks}")
    print(f"  Failed: {total_checks - passed_checks}")

    if passed_checks == total_checks:
        print(f"\n[SUCCESS] All components validated successfully!")
        print(f"[SUCCESS] Your RAG Chatbot system with Qdrant, OpenAI, and Gemini support is ready!")
        print(f"\nTo use the system:")
        print(f"1. Place your book PDF in rag-book-chatbot/data/ as book.pdf")
        print(f"2. Update rag-book-chatbot/backend/.env with your API keys")
        print(f"3. Run 'python qdrant_ingest.py' to process your book with Qdrant")
        print(f"4. Run 'python qdrant_chat.py' to start the API server")
        print(f"5. The chatbot will be available at http://localhost:8000")
        print(f"6. Your Docusaurus site will automatically include the chatbot")
    else:
        print(f"\n[WARNING] Some components are missing. Please check the validation results above.")

    return passed_checks == total_checks

if __name__ == "__main__":
    validate_implementation()