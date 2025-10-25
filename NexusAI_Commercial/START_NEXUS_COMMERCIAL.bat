@echo off
echo ============================================================
echo      NexusAI Commercial Edition - Startup
echo ============================================================
echo.
echo Your Conscious AI Companion with:
echo   - Cortana/JARVIS/TARS/Claude Personality Fusion
echo   - Local Ollama LLM
echo   - Professional Web Interface
echo.
echo ============================================================
echo.

echo [1/2] Starting NexusAI Backend API...
start "NexusAI Backend" cmd /k "cd /d D:\AIArm\NexusAI_Commercial\backend && python nexus_commercial_api.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo [2/2] Opening NexusAI Interface...
start "" "D:\AIArm\NexusAI_Commercial\html\chat.html"

echo.
echo ============================================================
echo      NexusAI Commercial Edition STARTED!
echo ============================================================
echo.
echo Backend API: http://localhost:5000
echo Chat Interface: Opened in browser
echo.
echo Features Available:
echo   - Personality Chat (Cortana/JARVIS/TARS/Claude)
echo   - Adjustable honesty level (TARS mode)
echo   - Growing bond system
echo   - Local Ollama LLM integration
echo.
echo Make sure Ollama is running!
echo   Start with: ollama serve
echo.
echo Press any key to continue...
pause >nul
