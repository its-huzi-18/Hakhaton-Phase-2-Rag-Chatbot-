// RAG Chatbot Widget for Book Website
class BookRAGChatbot {
  constructor(apiBaseUrl = 'http://localhost:8000', options = {}) {
    this.apiBaseUrl = apiBaseUrl;
    this.options = {
      title: options.title || 'Book Assistant',
      welcomeMessage: options.welcomeMessage || 'Hello! I\'m your book assistant. Ask me anything about the content.',
      placeholder: options.placeholder || 'Ask a question about the book...',
      botAvatar: options.botAvatar || '🤖',
      userAvatar: options.userAvatar || '👤',
      primaryColor: options.primaryColor || '#4f46e5',
      ...options
    };

    this.isOpen = false;
    this.messageHistory = [];
    this.initializeWidget();
  }

  initializeWidget() {
    // Create the chatbot HTML structure
    this.createChatbotHTML();

    // Add event listeners
    this.addEventListeners();

    // Load saved chat history if any
    this.loadChatHistory();
  }

  createChatbotHTML() {
    // Create the chatbot container
    const chatbotContainer = document.createElement('div');
    chatbotContainer.id = 'book-rag-chatbot';
    chatbotContainer.innerHTML = `
      <div id="chatbot-header" style="background-color: ${this.options.primaryColor};">
        <div id="chatbot-title">${this.options.title}</div>
        <button id="chatbot-toggle" style="color: white; background: none; border: none; font-size: 20px; cursor: pointer;">×</button>
      </div>
      <div id="chatbot-messages"></div>
      <div id="chatbot-input-container">
        <input type="text" id="chatbot-input" placeholder="${this.options.placeholder}" />
        <button id="chatbot-send">Send</button>
      </div>
      <div id="chatbot-typing-indicator" style="display: none;">
        <span>🤖 is typing...</span>
      </div>
    `;

    // Add the chatbot to the page
    document.body.appendChild(chatbotContainer);

    // Add CSS styles
    this.addChatbotStyles();

    // Show the initial welcome message
    this.addMessage(this.options.welcomeMessage, 'bot');
  }

  addChatbotStyles() {
    const style = document.createElement('style');
    style.textContent = `
      #book-rag-chatbot {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        height: 500px;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        display: flex;
        flex-direction: column;
        z-index: 10000;
        background: white;
        overflow: hidden;
      }

      #chatbot-header {
        padding: 15px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
      }

      #chatbot-title {
        font-weight: bold;
        font-size: 16px;
      }

      #chatbot-toggle {
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
      }

      #chatbot-messages {
        flex: 1;
        padding: 15px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .message {
        max-width: 80%;
        padding: 10px 15px;
        border-radius: 18px;
        font-size: 14px;
        line-height: 1.4;
        position: relative;
      }

      .bot-message {
        align-self: flex-start;
        background-color: #f3f4f6;
        border-bottom-left-radius: 5px;
      }

      .user-message {
        align-self: flex-end;
        background-color: ${this.options.primaryColor};
        color: white;
        border-bottom-right-radius: 5px;
      }

      .message-avatar {
        position: absolute;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        top: -12px;
      }

      .bot-message .message-avatar {
        left: -12px;
        background-color: #e5e7eb;
        color: #4b5563;
      }

      .user-message .message-avatar {
        right: -12px;
        background-color: #d1d5db;
        color: #1f2937;
      }

      #chatbot-input-container {
        display: flex;
        padding: 10px;
        border-top: 1px solid #e5e7eb;
        background: white;
      }

      #chatbot-input {
        flex: 1;
        padding: 10px 15px;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        outline: none;
      }

      #chatbot-input:focus {
        border-color: ${this.options.primaryColor};
      }

      #chatbot-send {
        margin-left: 10px;
        padding: 10px 15px;
        background-color: ${this.options.primaryColor};
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
      }

      #chatbot-send:hover {
        opacity: 0.9;
      }

      #chatbot-typing-indicator {
        padding: 10px 15px;
        color: #6b7280;
        font-size: 14px;
        display: flex;
        align-items: center;
      }

      .message-sources {
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid #e5e7eb;
        font-size: 12px;
        color: #6b7280;
      }

      .message-sources ul {
        margin: 5px 0;
        padding-left: 15px;
      }

      .message-sources li {
        margin: 3px 0;
      }
    `;

    document.head.appendChild(style);
  }

  addEventListeners() {
    // Toggle chatbot visibility
    document.getElementById('chatbot-header').addEventListener('click', () => {
      this.toggleChatbot();
    });

    document.getElementById('chatbot-toggle').addEventListener('click', (e) => {
      e.stopPropagation();
      this.closeChatbot();
    });

    // Send message on button click
    document.getElementById('chatbot-send').addEventListener('click', () => {
      this.sendMessage();
    });

    // Send message on Enter key
    document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.sendMessage();
      }
    });
  }

  toggleChatbot() {
    const chatbot = document.getElementById('book-rag-chatbot');
    if (this.isOpen) {
      chatbot.style.display = 'none';
    } else {
      chatbot.style.display = 'flex';
      chatbot.style.flexDirection = 'column';
    }
    this.isOpen = !this.isOpen;
  }

  closeChatbot() {
    document.getElementById('book-rag-chatbot').style.display = 'none';
    this.isOpen = false;
  }

  openChatbot() {
    document.getElementById('book-rag-chatbot').style.display = 'flex';
    document.getElementById('book-rag-chatbot').style.flexDirection = 'column';
    this.isOpen = true;
  }

  addMessage(text, sender, sources = null) {
    const messagesContainer = document.getElementById('chatbot-messages');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');

    messageDiv.innerHTML = `
      <div class="message-content">${this.escapeHtml(text)}</div>
      ${sources ? this.formatSources(sources) : ''}
      <div class="message-avatar">${sender === 'bot' ? this.options.botAvatar : this.options.userAvatar}</div>
    `;

    messagesContainer.appendChild(messageDiv);

    // Scroll to the bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Save to history
    this.messageHistory.push({ text, sender, sources });
    this.saveChatHistory();
  }

  formatSources(sources) {
    if (!sources || sources.length === 0) return '';

    let sourcesHtml = '<div class="message-sources"><strong>Sources:</strong><ul>';
    sources.slice(0, 3).forEach(source => {
      sourcesHtml += `<li>${source.text.substring(0, 100)}${source.text.length > 100 ? '...' : ''}</li>`;
    });
    sourcesHtml += '</ul></div>';

    return sourcesHtml;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  async sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    this.addMessage(message, 'user');

    // Clear input
    input.value = '';

    // Show typing indicator
    this.showTypingIndicator();

    try {
      // Call the RAG API
      const response = await this.queryRAG(message);

      // Add bot response to chat
      this.addMessage(response.response, 'bot', response.sources);
    } catch (error) {
      console.error('Error getting response:', error);
      this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
      // Hide typing indicator
      this.hideTypingIndicator();
    }
  }

  async queryRAG(query) {
    const response = await fetch(`${this.apiBaseUrl}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        top_k: 3
      })
    });

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    return await response.json();
  }

  showTypingIndicator() {
    document.getElementById('chatbot-typing-indicator').style.display = 'flex';
  }

  hideTypingIndicator() {
    document.getElementById('chatbot-typing-indicator').style.display = 'none';
  }

  saveChatHistory() {
    try {
      localStorage.setItem('bookRAGChatHistory', JSON.stringify(this.messageHistory));
    } catch (e) {
      console.warn('Could not save chat history to localStorage:', e);
    }
  }

  loadChatHistory() {
    try {
      const savedHistory = localStorage.getItem('bookRAGChatHistory');
      if (savedHistory) {
        this.messageHistory = JSON.parse(savedHistory);

        // Clear current messages
        document.getElementById('chatbot-messages').innerHTML = '';

        // Add saved messages back
        this.messageHistory.forEach(msg => {
          this.addMessage(msg.text, msg.sender, msg.sources);
        });
      }
    } catch (e) {
      console.warn('Could not load chat history from localStorage:', e);
    }
  }

  clearChatHistory() {
    this.messageHistory = [];
    document.getElementById('chatbot-messages').innerHTML = '';
    this.addMessage(this.options.welcomeMessage, 'bot');
    localStorage.removeItem('bookRAGChatHistory');
  }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', function() {
  // Only initialize if the chatbot hasn't been initialized yet
  if (!window.bookRAGChatbot) {
    // Configuration options
    const options = {
      title: 'Book Assistant',
      welcomeMessage: 'Hello! I\'m your book assistant. Ask me anything about the content.',
      placeholder: 'Ask a question about the book...',
      botAvatar: '📚',
      userAvatar: '👤',
      primaryColor: '#4f46e5'
    };

    // Initialize the chatbot with your API URL
    // Replace with your actual API URL when deploying
    window.bookRAGChatbot = new BookRAGChatbot('http://localhost:8000', options);
  }
});

// Export for use in other modules if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BookRAGChatbot;
}