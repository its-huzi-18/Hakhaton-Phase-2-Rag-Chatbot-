import React, { useEffect } from 'react';
import RAGChatbot from '../components/RAGChatbot/RAGChatbot';

// Root component that wraps the entire app
export default function Root({ children }) {
  return (
    <>
      {children}
      <RAGChatbot />
    </>
  );
}