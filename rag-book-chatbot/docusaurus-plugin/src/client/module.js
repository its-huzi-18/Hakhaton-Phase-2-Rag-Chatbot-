// This file is loaded by Docusaurus to initialize the chatbot
import React from 'react';
import ReactDOM from 'react-dom';
import RAGChatbot from '../components/RAGChatbot';

// Initialize the chatbot when the DOM is ready
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    const chatbotRoot = document.getElementById('rag-chatbot-root');
    if (chatbotRoot) {
      ReactDOM.render(<RAGChatbot />, chatbotRoot);
    }
  });
}