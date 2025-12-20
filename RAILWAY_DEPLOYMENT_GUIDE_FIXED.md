# Deploying RAG Chatbot API to Railway

This guide will walk you through deploying your RAG chatbot API to Railway, which offers a free tier that's perfect for this application.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: Install the Railway CLI
3. **API Keys**: Have your Cohere API key and Qdrant credentials ready
4. **Processed Content**: Make sure you've already processed your book content

## Step 1: Install Railway CLI

### Windows:
```bash
npm install -g @railway/cli
# Or using Chocolatey:
choco install railway
```

### macOS:
```bash
brew install railwayapp/railway/railway
```

### Linux:
```bash
curl -fsSL https://railway.app/install.sh | bash
```

## Step 2: Login to Railway

```bash
railway login
```

## Step 3: Prepare Your Backend for Railway

Create a `Procfile` in your backend directory:

```bash
# In your backend directory
echo "web: uvicorn api:app --host=0.0.0.0 --port=\$PORT" > Procfile
```

Create a `runtime.txt` to specify Python version:

```bash
# In your backend directory
echo "python-3.11" > runtime.txt
```

## Step 4: Fix Dependencies for Railway

If you're getting dependency conflicts during deployment, you need to ensure you have the correct requirements file:

```bash
# In your backend directory, ensure you have the correct requirements
# The file should contain only the dependencies your API actually needs:
```

**backend/railway_requirements.txt** should contain:
```
requests
beautifulsoup4
cohere
qdrant-client
python-dotenv
typing-extensions
fastapi
uvicorn[standard]
pydantic
```

Make sure you're using the correct requirements file for Railway deployment.

## Step 5: Initialize Railway Project

```bash
# Navigate to your backend directory
cd backend

# Initialize Railway project
railway init
```

## Step 6: Set Environment Variables

```bash
# Set your environment variables
railway var set COHERE_API_KEY="your_cohere_api_key_here"
railway var set QDRANT_URL="your_qdrant_url_here"
railway var set QDRANT_API_KEY="your_qdrant_api_key_here"
railway var set TARGET_URL="https://your-book-website.com"

# Set port (Railway provides this automatically, but good to be explicit)
railway var set PORT="8000"
```

## Step 7: Deploy to Railway

```bash
# Deploy your API
railway up

# Or if you're in the backend directory
railway up --service <your-service-name>
```

## Step 8: Configure Railway Service

1. Go to your [Railway dashboard](https://railway.app/projects)
2. Select your project
3. Click on the API service
4. Go to "Settings" → "Environment Variables" and verify all variables are set
5. Go to "Deployments" to monitor the deployment process

## Step 9: Get Your API URL

After successful deployment, you'll have a URL like:
```
https://your-project-name-production.up.railway.app
```

## Step 10: Update Your Frontend

Update the API URL in your chatbot widget:

1. Edit the `chatbot_widget.js` file
2. Replace the API base URL:

```javascript
// Find this line in chatbot_widget.js
window.bookRAGChatbot = new BookRAGChatbot('https://your-railway-app-url.up.railway.app', options);
```

Or better yet, use an environment variable approach:

```html
<script>
  window.CHATBOT_API_URL = 'https://your-railway-app-url.up.railway.app';
</script>
<script src="chatbot_widget.js"></script>
```

And update the widget to use this variable:

```javascript
const apiBaseUrl = window.CHATBOT_API_URL || 'http://localhost:8000';
window.bookRAGChatbot = new BookRAGChatbot(apiBaseUrl, options);
```

## Step 11: Deploy Your Website to Vercel

1. In your Docusaurus project directory:

```bash
# Build your site
npm run build

# Deploy to Vercel
npm install -g vercel
vercel --prod
```

2. Make sure your `chatbot_widget.js` is included in your Vercel deployment

## Alternative: Railway Dashboard Method

Instead of CLI, you can also use the Railway dashboard:

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Connect to your GitHub repository (or upload your backend files)
4. Select "Python" environment
5. Set environment variables in the dashboard
6. Deploy!

## Railway Free Tier Limitations

- **512MB RAM** (sufficient for this application)
- **500 hours/month** (about 21 days of continuous operation)
- **1 CPU**
- **Environment variables** storage

## Monitoring and Logs

```bash
# View logs
railway logs

# Open dashboard for your project
railway dashboard
```

## Troubleshooting Common Issues

### Issue: Dependency conflicts during deployment
- This was the issue you encountered
- Make sure you're using the simplified requirements file I provided above
- Remove any conflicting packages like langchain, torch, etc. that aren't needed for your API

### Issue: Deployment fails
- Check that all environment variables are set
- Verify requirements.txt is in the backend directory
- Make sure Procfile is correctly formatted

### Issue: API returns 500 errors
- Check Railway logs: `railway logs`
- Verify your Qdrant connection
- Ensure your Cohere API key is valid

### Issue: Chatbot can't connect
- Verify the Railway API URL is correct
- Check CORS settings in your API
- Ensure your Vercel website URL is allowed in CORS

## Cost Considerations

- **Railway**: Free tier includes 500 hours/month
- **Qdrant**: Free tier for vector database
- **Cohere**: Free tier for API usage
- **Vercel**: Free for static hosting

This setup allows you to have a completely free RAG chatbot system!

## Testing Your Deployed System

1. Verify your Railway API is running
2. Test with the API documentation at `https://your-app.up.railway.app/docs`
3. Check that your Vercel site loads the chatbot
4. Test a few questions about your book content

Your RAG chatbot system is now ready for production use with your book website hosted on Vercel and API hosted on Railway!