import React, { useState, useRef, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './RAGChatbot.css';

const RAGChatbot = () => {
  const { siteConfig } = useDocusaurusContext();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, sender: 'assistant', text: 'Hello! I\'m your book assistant. Ask me anything about the book content!' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Get API URL from site config or use default
  const apiUrl = siteConfig.customFields?.ragChatbotApiUrl || 'http://localhost:8000';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), sender: 'user', text: inputValue.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userMessage.text })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage = { id: Date.now() + 1, sender: 'assistant', text: data.answer };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: 'Sorry, I encountered an error processing your question. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={`rag-chatbot-container ${isOpen ? 'open' : 'closed'}`}>
      <div className="rag-chat-header" onClick={() => setIsOpen(!isOpen)}>
        <h3>Book Assistant</h3>
        <button className="rag-toggle-btn">
          {isOpen ? '−' : '+'}
        </button>
      </div>

      {isOpen && (
        <div className="rag-chat-body">
          <div className="rag-chat-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`rag-message ${message.sender}-message`}
              >
                {message.text}
              </div>
            ))}
            {isLoading && (
              <div className="rag-message assistant-message">
                <div className="rag-typing-indicator">Thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="rag-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the book..."
              className="rag-question-input"
              rows="1"
            />
            <button
              onClick={sendMessage}
              className="rag-send-btn"
              disabled={isLoading || !inputValue.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGChatbot;