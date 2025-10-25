@echo off
echo =====================================================================
echo             AIArm Real Agent Connection
echo =====================================================================
echo.

echo First, killing any existing Node.js processes...
taskkill /F /IM node.exe >nul 2>&1

cd /D "D:\AIArm\WebInterface"

echo Installing required packages...
call npm install express body-parser child_process

echo Starting real agent server...
echo.
echo This server connects directly to your AI orchestrator at:
echo D:\AIArm\MultiAgent\enhanced_orchestrator.py
echo.
echo Once the server is running, it will show you the URL to access
echo the interface in your browser.
echo.

node real_server.js

pause
