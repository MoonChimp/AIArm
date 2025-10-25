@echo off
echo ========================================
echo  Starting NexusAI WebApp
echo ========================================
echo.
echo This will start the web server on port 8080
echo.
echo Access from any device on your network:
echo   http://192.168.1.230:8080/html/chat.html
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d D:\AIArm\NexusAI_Commercial
python -m http.server 8080
