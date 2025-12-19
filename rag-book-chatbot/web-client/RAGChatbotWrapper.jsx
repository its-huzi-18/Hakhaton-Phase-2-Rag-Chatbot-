import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import RAGChatbot from './RAGChatbot';
import './RAGChatbot.css';

const RAGChatbotWrapper = () => {
  const { siteConfig } = useDocusaurusContext();

  // You can get the API URL from site config or environment
  const apiUrl = siteConfig.customFields?.ragChatbotApiUrl || 'http://localhost:8000';

  return <RAGChatbot apiUrl={apiUrl} />;
};

export default RAGChatbotWrapper;