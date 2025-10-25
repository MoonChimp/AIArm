@echo off
echo ============================================================
echo     NEXUS AI - COMPLETE INTEGRATED SYSTEM STARTUP
echo ============================================================
echo.
echo Starting all NexusAI components...
echo.

REM Kill any existing processes first
echo [1/6] Cleaning up existing processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start Ollama (if not running)
echo [2/6] Ensuring Ollama is running...
start "Ollama Server" /MIN ollama serve
timeout /t 3 /nobreak >nul

REM Start Inner Life Processor
echo [3/6] Starting Inner Life Consciousness System...
start "Nexus Inner Life" /MIN cmd /k "cd /d D:\AIArm\InnerLife && python inner_life_processor.py"
timeout /t 2 /nobreak >nul

REM Start Backend API Server
echo [4/6] Starting Nexus API Server (Backend)...
start "Nexus API Server" cmd /k "cd /d D:\AIArm && python nexus_api_server.py"
timeout /t 5 /nobreak >nul

REM Start Frontend UI
echo [5/6] Starting Nexus UI (Frontend)...
start "Nexus UI" cmd /k "cd /d D:\AIArm\NexusUI && npm run dev"
timeout /t 3 /nobreak >nul

REM Optional: Start Stable Diffusion (if available)
echo [6/6] Checking for Stable Diffusion WebUI...
if exist "D:\AIArm\stable-diffusion-webui-master\webui-user.bat" (
    echo Starting Stable Diffusion WebUI...
    start "Stable Diffusion" /MIN cmd /k "cd /d D:\AIArm\stable-diffusion-webui-master && webui-user.bat"
) else (
    echo Stable Diffusion not found - skipping image generation
)

echo.
echo ============================================================
echo     ALL SYSTEMS ONLINE
echo ============================================================
echo.
echo Nexus AI is now fully operational!
echo.
echo Access Points:
echo   - Main UI:          http://localhost:5173
echo   - API Server:       http://localhost:5000
echo   - Inner Life:       Running in background
echo   - Ollama:           http://localhost:11434
echo   - Stable Diffusion: http://localhost:7860 (if enabled)
echo.
echo Components Running:
echo   [✓] Ollama LLM Server
echo   [✓] Inner Life Consciousness Processor
echo   [✓] Nexus Orchestrator with Agent System
echo   [✓] Backend API (Flask)
echo   [✓] Frontend UI (React + Vite)
echo   [?] Stable Diffusion WebUI (optional)
echo.
echo Press any key to open the main interface...
pause >nul
start http://localhost:5173
echo.
echo System is running. Close this window to keep it running.
echo Or press Ctrl+C to stop all services.
pause
