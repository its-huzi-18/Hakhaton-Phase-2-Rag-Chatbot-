# Complete Deployment Steps for RAG Chatbot

## Step 1: Deploy Backend to Railway

1. **Go to Railway** - Visit [railway.app](https://railway.app)
2. **Sign up** - Use your GitHub account to sign up
3. **Create new project** - Click "New Project" → "Deploy from GitHub"
4. **Select your repository** - Choose the GitHub repo containing your code
5. **Railway will auto-detect** - It will see the Dockerfile and deploy automatically

## Step 2: Configure Environment Variables in Railway

1. **In your Railway project dashboard**, click on "Variables" in the left sidebar
2. **Add these variables** (click "New Variable" for each):
   - `OPENAI_API_KEY` = `your_openai_api_key_here` (optional)
   - `GOOGLE_API_KEY` = `your_google_api_key_here` (optional)
   - `QDRANT_COLLECTION_NAME` = `book_collection` (or your preferred name)

3. **If using cloud Qdrant, also add**:
   - `QDRANT_URL` = `your_qdrant_cloud_url`
   - `QDRANT_API_KEY` = `your_qdrant_api_key`

## Step 3: Get Your Railway Backend URL

1. **In your Railway project dashboard**, you'll see a URL like:
   - `https://your-project-name.up.railway.app`
   - Copy this URL (it will be different for your project)

## Step 4: Update Your Website Configuration

There's no need to update docusaurus.config.ts for the API URL anymore. The API URL will be configured as an environment variable in Vercel.

## Step 5: Deploy Frontend to Vercel

1. **Go to Vercel** - Visit [vercel.com](https://vercel.com)
2. **Sign in** with your GitHub account
3. **Click "New Project"** → "Import Git Repository"
4. **Select your repository** containing the `my-book` directory
5. **Set these build settings**:
   - Framework Preset: `Docusaurus`
   - Root Directory: `my-book`
   - Build Command: `npm run build`
   - Output Directory: `build`
6. **Add Environment Variables** (click "Environment Variables" section):
   - Key: `RAG_CHATBOT_API_URL`, Value: `https://your-railway-app.up.railway.app` (your actual Railway backend URL)
7. **Click "Deploy"**

**Note:** The environment variable will be available during the build process and passed to the Docusaurus config.

## Step 6: Process Your Book (One-time Setup)

1. **After Railway deployment**, you need to process your book PDF:
   - Make sure your book is in `rag-book-chatbot/data/book.pdf`
   - Send a POST request to your Railway URL to run the ingestion:
   - This step requires running the qdrant_ingest.py script on the deployed server or locally with the deployed database

## Step 7: Test Your Chatbot

1. **Visit your Vercel-deployed website**
2. **Look for the chatbot icon** in the bottom-right corner
3. **Ask a question** - it should now connect to your Railway backend and respond

## Important Notes:

- **Backend and frontend are separate**: The Python API runs on Railway, the website runs on Vercel
- **Processing time**: The first time someone asks a question, it might be slow as it loads the vector database
- **API keys**: Without API keys, the system will use local fallback models (slower but functional)
- **Qdrant**: For production, consider using Qdrant Cloud for better performance

## Troubleshooting:

- If the chatbot doesn't appear, check that your docusaurus.config.ts includes the plugin
- If it doesn't respond, verify the backend URL in your config is correct
- Check browser console for any error messages
- Ensure your backend is deployed and responding to requests