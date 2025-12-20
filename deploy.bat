@echo off
REM RAG Chatbot Deployment Script for Windows
REM This script helps automate the deployment process

echo =========================================
echo RAG Chatbot Deployment Script for Windows
echo =========================================

REM Function to check if a command exists
where railway >nul 2>&1
if errorlevel 1 (
    echo ❌ Railway CLI not found. Please install it:
    echo    npm install -g @railway/cli
    exit /b 1
)

where git >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found. Please install Git.
    exit /b 1
)

echo ✅ Prerequisites check passed

:menu
echo.
echo What would you like to do?
echo 1) Process book content only
echo 2) Deploy API to Railway only
echo 3) Process content and deploy API
echo 4) Show deployment summary
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto process_content
if "%choice%"=="2" goto deploy_api
if "%choice%"=="3" goto process_and_deploy
if "%choice%"=="4" goto show_summary
echo Invalid choice. Please enter 1, 2, 3, or 4.
goto menu

:process_content
echo Processing book content...
cd backend
if not exist ".env" (
    echo ❌ .env file not found in backend directory
    echo Please create backend/.env with your API keys
    cd ..
    pause
    exit /b 1
)

python process_book.py
cd ..
echo ✅ Book content processed
goto show_summary

:deploy_api
echo Deploying API to Railway...
cd backend

REM Check if Railway project is initialized
if not exist ".railway" (
    echo Initializing Railway project...
    railway init
)

echo Deploying to Railway...
railway up
cd ..
echo ✅ API deployed to Railway
goto show_summary

:process_and_deploy
call :process_content
call :deploy_api
goto show_summary

:show_summary
echo.
echo =========================================
echo DEPLOYMENT SUMMARY
echo =========================================
echo.
echo 1. API Deployment:
echo    - Check your Railway dashboard for the API URL
echo    - It should look like: https://your-project.up.railway.app
echo.
echo 2. Frontend Integration:
echo    - Update chatbot_widget.js with your Railway API URL
echo    - Deploy your Docusaurus site to Vercel
echo.
echo 3. Test the system:
echo    - Visit your Vercel website
echo    - Use the chatbot to ask questions about your book
echo.
echo For detailed instructions, see: DEPLOYMENT_COMPLETE_GUIDE.md
echo =========================================
pause