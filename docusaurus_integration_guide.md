# Docusaurus Integration Guide for RAG Chatbot

This guide explains how to integrate the RAG chatbot widget into a Docusaurus-based book website.

## Overview

The RAG (Retrieval-Augmented Generation) chatbot allows users to ask questions about your book content and receive AI-powered answers based on the actual book text. This creates an interactive learning experience for your readers.

## Prerequisites

- A Docusaurus-based book website
- The RAG backend running (API server with processed content)
- Basic knowledge of Docusaurus customization

## Integration Steps

### 1. Prepare the Chatbot Widget

First, copy the `chatbot_widget.js` file to your Docusaurus static directory:

```bash
# Copy the chatbot widget to your static assets
cp chatbot_widget.js your-docusaurus-site/static/
```

### 2. Modify Docusaurus Configuration

To add the chatbot to all pages, you can modify your Docusaurus setup. There are two main approaches:

#### Approach A: Using a React Component (Recommended)

1. Create a new React component in `src/components/BookChatbot.js`:

```jsx
import React, { useEffect } from 'react';

const BookChatbot = () => {
  useEffect(() => {
    // Dynamically load the chatbot script
    const script = document.createElement('script');
    script.src = '/chatbot_widget.js';
    script.async = true;
    document.head.appendChild(script);

    return () => {
      // Clean up the script when component unmounts
      document.head.removeChild(script);
    };
  }, []);

  return null; // This component doesn't render anything itself
};

export default BookChatbot;
```

2. Create a layout wrapper in `src/theme/Layout/index.js`:

```jsx
import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import BookChatbot from '@site/src/components/BookChatbot';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
        <BookChatbot />
      </OriginalLayout>
    </>
  );
}
```

#### Approach B: Direct HTML Injection

If you prefer to add the script directly to all HTML pages:

1. Edit `static/index.html` or modify the `docusaurus.config.js` file:

In `docusaurus.config.js`, add the script to the `head` of all pages:

```js
module.exports = {
  // ... your existing config
  scripts: [
    {
      src: '/chatbot_widget.js',
      async: true,
    },
  ],
  // ... rest of config
};
```

### 3. Configure the Chatbot for Your API

The chatbot widget connects to the API server. You have several options:

#### Option 1: Update the Widget Directly

Modify the API URL in `chatbot_widget.js` to point to your deployed API:

```js
// In chatbot_widget.js, update the API base URL
const options = {
  // ... other options
};

// Initialize the chatbot with your API URL
window.bookRAGChatbot = new BookRAGChatbot('https://your-api-url.com', options);
```

#### Option 2: Environment Variable (Recommended)

For more flexibility, you can pass the API URL as a configuration option. Update the initialization in `chatbot_widget.js`:

```js
// Get API URL from environment or use default
const apiBaseUrl = window.CHATBOT_API_URL || 'http://localhost:8000';

window.bookRAGChatbot = new BookRAGChatbot(apiBaseUrl, options);
```

Then set the global variable before loading the script:

```html
<script>
  window.CHATBOT_API_URL = 'https://your-deployed-api.com';
</script>
<script src="/chatbot_widget.js"></script>
```

### 4. Customization Options

The chatbot widget can be customized with various options:

```js
const options = {
  title: 'Book Assistant',  // Chatbot window title
  welcomeMessage: 'Ask me anything about the book!',  // Initial message
  placeholder: 'Type your question...',  // Input placeholder
  botAvatar: '📚',  // Bot avatar emoji
  userAvatar: '👤',  // User avatar emoji
  primaryColor: '#4f46e5',  // Brand color
  top_k: 3,  // Number of sources to retrieve
};

window.bookRAGChatbot = new BookRAGChatbot(apiBaseUrl, options);
```

### 5. Styling Considerations

The chatbot widget comes with its own styles, but you can customize them to match your Docusaurus theme:

1. Add custom CSS in your Docusaurus site's global CSS file (`src/css/custom.css`):

```css
/* Custom chatbot styles to match your theme */
#book-rag-chatbot {
  font-family: var(--ifm-font-family-base);
}

#chatbot-header {
  background-color: var(--ifm-color-primary);
}
```

### 6. Deployment Considerations

#### For Local Development

During development, make sure your API server is running:

```bash
# In your backend directory
cd backend
python start_api.py
```

#### For Production Deployment

1. **API Server**: Deploy your FastAPI backend to a cloud provider (Heroku, Railway, etc.)
2. **Vector Database**: Use a hosted Qdrant service or secure your self-hosted instance
3. **Frontend**: The chatbot widget will be served with your Docusaurus site

### 7. Testing the Integration

1. Start your Docusaurus development server:
   ```bash
   npm run start
   ```

2. Open your browser to your site (usually `http://localhost:3000`)

3. You should see the chatbot widget in the bottom-right corner

4. Test by asking questions about your book content

## Troubleshooting

### Common Issues

1. **Chatbot doesn't appear**: Check that the script is loaded and there are no JavaScript errors in the console

2. **API connection errors**: Verify that your API server is running and accessible from the client

3. **CORS errors**: Make sure your API server allows requests from your website's domain

4. **No content in responses**: Ensure that you've processed your book content with `process_book.py`

### Debugging Steps

1. Open browser developer tools (F12)
2. Check the Console tab for JavaScript errors
3. Check the Network tab to see if API requests are being made
4. Verify that the chatbot script is loaded in the Sources tab

## Security Considerations

1. **API Keys**: Never expose your API keys in client-side code
2. **CORS**: In production, restrict CORS origins to your domain only
3. **Rate Limiting**: Consider implementing rate limiting on your API
4. **Content Validation**: The system processes publicly available content, but validate inputs

## Performance Tips

1. **Optimize Embeddings**: Adjust chunk size in `process_book.py` for better performance
2. **Caching**: Implement caching for frequent queries
3. **CDN**: Host the chatbot widget on a CDN for faster loading
4. **Lazy Loading**: Load the chatbot widget only when needed

## Customization Examples

### Adding to Specific Pages Only

If you want to add the chatbot to specific pages only, use the MDX approach:

Create a new MDX file `src/components/BookChatbot.mdx`:

```md
import BookChatbot from '@site/src/components/BookChatbot';

<BookChatbot />
```

Then include it in specific pages:

```mdx
---
title: Advanced Concepts
---

import BookChatbot from '@site/src/components/BookChatbot';

# Advanced Concepts

This chapter covers advanced topics...

<BookChatbot />
```

This integration guide provides everything you need to add the RAG chatbot to your Docusaurus-based book website, creating an interactive experience that allows readers to ask questions and get answers based on your book content.