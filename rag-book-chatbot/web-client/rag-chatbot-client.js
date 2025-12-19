// rag-chatbot-client.js
// Client-side JavaScript for integrating the RAG chatbot into the book website

class RAGChatbot {
  constructor(apiUrl = 'http://localhost:8000') {
    this.apiUrl = apiUrl;
    this.chatContainer = null;
    this.inputField = null;
    this.sendButton = null;
    this.initializeChatbot();
  }

  initializeChatbot() {
    // Create the chatbot UI elements
    this.createChatUI();

    // Set up event listeners
    this.sendButton = document.getElementById('rag-send-btn');
    this.inputField = document.getElementById('rag-question-input');
    this.chatContainer = document.getElementById('rag-chat-container');

    this.sendButton.addEventListener('click', () => this.sendMessage());
    this.inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.sendMessage();
      }
    });
  }

  createChatUI() {
    // Check if chatbot UI already exists
    if (document.getElementById('rag-chatbot-container')) {
      return;
    }

    // Create the chatbot container
    const chatbotContainer = document.createElement('div');
    chatbotContainer.id = 'rag-chatbot-container';
    chatbotContainer.innerHTML = `
      <div id="rag-chat-header">
        <h3>Book Assistant</h3>
        <button id="rag-toggle-btn">−</button>
      </div>
      <div id="rag-chat-body">
        <div id="rag-chat-container"></div>
        <div id="rag-input-area">
          <input type="text" id="rag-question-input" placeholder="Ask a question about the book..." />
          <button id="rag-send-btn">Send</button>
        </div>
      </div>
    `;

    // Add the chatbot to the page
    document.body.appendChild(chatbotContainer);

    // Add CSS styles
    this.addChatStyles();

    // Set up toggle functionality
    document.getElementById('rag-toggle-btn').addEventListener('click', () => {
      const chatBody = document.getElementById('rag-chat-body');
      const toggleBtn = document.getElementById('rag-toggle-btn');
      if (chatBody.style.display === 'none') {
        chatBody.style.display = 'block';
        toggleBtn.textContent = '−';
      } else {
        chatBody.style.display = 'none';
        toggleBtn.textContent = '+';
      }
    });

    // Add initial message
    this.addMessage('assistant', 'Hello! I\'m your book assistant. Ask me anything about the book content!');
  }

  addChatStyles() {
    // Create and add CSS styles
    const style = document.createElement('style');
    style.textContent = `
      #rag-chatbot-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        background: white;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        font-family: Arial, sans-serif;
      }

      #rag-chat-header {
        background: #4f5cf5;
        color: white;
        padding: 10px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      #rag-chat-header h3 {
        margin: 0;
        font-size: 16px;
      }

      #rag-toggle-btn {
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      #rag-chat-body {
        display: flex;
        flex-direction: column;
        height: 400px;
      }

      #rag-chat-container {
        flex: 1;
        overflow-y: auto;
        padding: 15px;
        background: #f9f9f9;
      }

      .rag-message {
        margin-bottom: 15px;
        padding: 8px 12px;
        border-radius: 8px;
        max-width: 80%;
      }

      .rag-user-message {
        background: #e3f2fd;
        margin-left: auto;
        text-align: right;
      }

      .rag-assistant-message {
        background: #f1f1f1;
        margin-right: auto;
      }

      #rag-input-area {
        display: flex;
        padding: 10px;
        border-top: 1px solid #eee;
        background: white;
      }

      #rag-question-input {
        flex: 1;
        padding: 8px 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        margin-right: 10px;
      }

      #rag-send-btn {
        padding: 8px 15px;
        background: #4f5cf5;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }

      #rag-send-btn:hover {
        background: #3a46c4;
      }

      .rag-typing-indicator {
        color: #888;
        font-style: italic;
        padding: 8px 12px;
      }
    `;

    document.head.appendChild(style);
  }

  addMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('rag-message');
    messageDiv.classList.add(sender === 'user' ? 'rag-user-message' : 'rag-assistant-message');
    messageDiv.textContent = text;

    this.chatContainer.appendChild(messageDiv);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
  }

  addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'rag-typing-indicator';
    typingDiv.classList.add('rag-typing-indicator');
    typingDiv.textContent = 'Thinking...';

    this.chatContainer.appendChild(typingDiv);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
  }

  removeTypingIndicator() {
    const typingIndicator = document.getElementById('rag-typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }

  async sendMessage() {
    const question = this.inputField.value.trim();
    if (!question) return;

    // Add user message to UI
    this.addMessage('user', question);
    this.inputField.value = '';

    // Show typing indicator
    this.addTypingIndicator();

    try {
      // Call the backend API
      const response = await fetch(`${this.apiUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      // Remove typing indicator
      this.removeTypingIndicator();

      // Add assistant response to UI
      this.addMessage('assistant', data.answer);

      // Optionally log source chunks to console for debugging
      console.log('Source chunks:', data.source_chunks);
    } catch (error) {
      // Remove typing indicator
      this.removeTypingIndicator();

      // Add error message to UI
      this.addMessage('assistant', 'Sorry, I encountered an error processing your question. Please try again.');
      console.error('Error sending message:', error);
    }
  }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
  // Initialize with your backend API URL
  // For development: http://localhost:8000
  // For production: your actual backend URL
  new RAGChatbot('http://localhost:8000');
});