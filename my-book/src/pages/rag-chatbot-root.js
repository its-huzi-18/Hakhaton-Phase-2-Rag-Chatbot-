// This file adds the RAG chatbot to all pages by injecting it into the DOM
import React from 'react';
import { createRoot } from 'react-dom/client';
import RAGChatbot from '../components/RAGChatbot/RAGChatbot';

// Create a global script to initialize the chatbot when the DOM is ready
if (typeof document !== 'undefined') {
  // Wait for the DOM to be fully loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeChatbot);
  } else {
    // DOM is already loaded, initialize immediately
    initializeChatbot();
  }
}

function initializeChatbot() {
  // Create a container for the chatbot if it doesn't exist
  let chatbotContainer = document.getElementById('rag-chatbot-root');
  if (!chatbotContainer) {
    chatbotContainer = document.createElement('div');
    chatbotContainer.id = 'rag-chatbot-root';
    document.body.appendChild(chatbotContainer);
  }

  // Render the chatbot component
  const root = createRoot(chatbotContainer);
  root.render(<RAGChatbot />);
}

// This component doesn't render anything itself,
// it just sets up the global chatbot
export default function RAGChatbotRoot() {
  return null;
}