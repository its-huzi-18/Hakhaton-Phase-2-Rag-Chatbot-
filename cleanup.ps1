# PowerShell script to clean up old RAGChatbot component files
Remove-Item -Path "D:\Vs Code-All-Things\Github Repo\GPT\my-book\src\components\RAGChatbot" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "D:\Vs Code-All-Things\Github Repo\GPT\my-book\src\pages\rag-chatbot-root.js" -Force -ErrorAction SilentlyContinue