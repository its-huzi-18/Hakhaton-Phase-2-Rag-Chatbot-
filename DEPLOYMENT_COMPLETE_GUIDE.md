# Complete Deployment Guide: RAG Chatbot for Book Website

This guide provides comprehensive instructions for deploying your RAG chatbot system with your book website on Vercel and the API on Railway.

## System Overview

- **Frontend**: Your book website (Docusaurus) → Deployed on Vercel
- **Backend API**: RAG system → Deployed on Railway
- **Database**: Qdrant vector database → Hosted service
- **AI**: Cohere for embeddings and generation

## Prerequisites

1. **Accounts**:
   - [Railway](https://railway.app) account
   - [Vercel](https://vercel.com) account
   - [Cohere](https://cohere.ai) account (API key)

2. **Qdrant Database**:
   - Either Qdrant Cloud account or self-hosted instance

3. **Book Content**:
   - Your book website must be publicly accessible

## Step 1: Prepare Your Environment

### Create .env file in backend directory:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
TARGET_URL=https://your-book-website.com
PORT=8000
```

## Step 2: Process Your Book Content (Critical!)

Before deploying, you must process your book content locally:

```bash
cd backend
python process_book.py
```

This will crawl your book website and store the content in your Qdrant database.

## Step 3: Deploy API to Railway

### Option A: Using Railway CLI

1. **Install Railway CLI**:
   ```bash
   # Windows
   npm install -g @railway/cli

   # Or use the direct installer
   curl -fsSL https://railway.app/install.sh | bash
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Navigate to backend directory and initialize**:
   ```bash
   cd backend
   railway init
   ```

4. **Set environment variables**:
   ```bash
   railway var set COHERE_API_KEY="your_cohere_api_key_here"
   railway var set QDRANT_URL="your_qdrant_url_here"
   railway var set QDRANT_API_KEY="your_qdrant_api_key_here"
   railway var set TARGET_URL="https://your-book-website.com"
   ```

5. **Deploy**:
   ```bash
   railway up
   ```

### Option B: Using Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Connect your repository
4. Select the `backend` directory
5. Add the Dockerfile I provided
6. Set environment variables in the dashboard
7. Deploy!

## Step 4: Get Your Railway API URL

After deployment, you'll have a URL like:
```
https://your-project-name-production.up.railway.app
```

## Step 5: Update Your Frontend

### For Docusaurus sites:

1. **Copy the chatbot widget** to your static assets:
   ```bash
   cp chatbot_widget.js your-docusaurus-site/static/
   ```

2. **Update the API URL in chatbot_widget.js**:
   ```javascript
   // Replace the API URL with your Railway deployment
   window.bookRAGChatbot = new BookRAGChatbot('https://your-railway-app.up.railway.app', options);
   ```

3. **Or use a more flexible approach** by adding this to your HTML before the script:
   ```html
   <script>
     window.CHATBOT_API_URL = 'https://your-railway-app.up.railway.app';
   </script>
   <script src="/chatbot_widget.js"></script>
   ```

4. **And update the widget to use this**:
   ```javascript
   const apiBaseUrl = window.CHATBOT_API_URL || 'http://localhost:8000';
   window.bookRAGChatbot = new BookRAGChatbot(apiBaseUrl, options);
   ```

## Step 6: Deploy Your Book Website to Vercel

### For Docusaurus:

1. **Build your site**:
   ```bash
   npm run build
   ```

2. **Deploy to Vercel**:
   ```bash
   npm install -g vercel
   vercel --prod
   ```

### Alternative: Git Integration
1. Push your Docusaurus code to GitHub
2. Connect Vercel to your GitHub repo
3. Vercel will auto-deploy on pushes

## Step 7: Test Your Complete System

1. **Verify API is working**: Visit `https://your-railway-app.up.railway.app/docs` for API documentation
2. **Test your website**: Visit your Vercel-deployed website
3. **Test the chatbot**: Ask questions about your book content
4. **Check browser console** for any errors

## Docker Deployment Alternative

If you prefer to use Docker, the backend directory now includes a Dockerfile:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ /app/

# Expose port (Railway will set PORT environment variable)
EXPOSE $PORT 8000

# Run the application
CMD ["sh", "-c", "uvicorn api:app --host=0.0.0.0 --port=${PORT:-8000}"]
```

## Troubleshooting

### Common Issues:

1. **"No content found" responses**:
   - Make sure you ran `python process_book.py` before deployment
   - Verify your TARGET_URL is accessible and contains book content

2. **API connection errors**:
   - Check that your Railway API is running
   - Verify the API URL in your frontend

3. **CORS errors**:
   - The API allows all origins by default, but check browser console

4. **Environment variable issues**:
   - Verify all environment variables are set in Railway

### Debugging Commands:

```bash
# Check Railway logs
railway logs

# Test API locally first
cd backend
python start_api.py
# Then visit http://localhost:8000/docs

# Test with debug script
python debug_rag_system.py
```

## Free Tier Considerations

- **Railway**: 500 hours/month free (about 21 days)
- **Vercel**: Free for static sites
- **Qdrant Cloud**: Free tier available
- **Cohere**: Free API tier (limited requests)

## Performance Tips

1. **Optimize content processing**: Adjust chunk size in `process_book.py` if needed
2. **Monitor API usage**: Check your Cohere and Qdrant usage
3. **Caching**: Consider implementing response caching for frequent queries

## Security Considerations

1. **API Keys**: Never expose in frontend code
2. **CORS**: Restrict to your domain in production
3. **Rate Limiting**: Consider implementing on the API
4. **HTTPS**: Ensure all connections use HTTPS

## Maintenance

1. **Content Updates**: If you update your book content, re-run `process_book.py`
2. **Monitoring**: Check Railway logs regularly
3. **Backups**: Regularly backup your Qdrant data
4. **Updates**: Keep dependencies updated

Your RAG chatbot system is now ready for production deployment! The chatbot will provide specific, detailed answers about your book content to users visiting your Vercel-hosted website.