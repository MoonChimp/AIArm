@echo off
echo ============================================================
echo      NexusAI - EASY START (Use Your Working System)
echo ============================================================
echo.
echo This uses your EXISTING working Nexus API server
echo that already runs perfectly!
echo.
echo ============================================================
pause

echo.
echo [1/2] Starting YOUR working Nexus API server...
start "NexusAI Backend" cmd /k "cd /d D:\AIArm && python nexus_api_server.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo [2/2] Opening chat interface...
start "" "D:\AIArm\NexusAI_Commercial\html\chat.html"

echo.
echo ============================================================
echo      DONE! Chat interface opened!
echo ============================================================
echo.
echo Your WORKING backend: http://localhost:5000
echo Ollama must be running: ollama serve
echo.
echo The chat should work now using YOUR existing API!
echo.
pause
