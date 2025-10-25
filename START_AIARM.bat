@echo off
title Nexus AI - Unified Launcher
color 0B

cls
echo ================================================================================
echo                           NEXUS AI SYSTEM
echo                        Unified Control Panel
echo ================================================================================
echo.
echo Starting all Nexus AI components...
echo.

REM Check if Ollama is running
echo [1/4] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   [!] WARNING: Ollama is not running
    echo   [!] Some AI features will be limited
) else (
    echo   [OK] Ollama is running
)
echo.

REM Start Flask API Server (Backend)
echo [2/3] Starting Nexus API Server (Backend)...
cd /d "D:\AIArm"
start "Nexus API Server" cmd /k "python nexus_api_server.py"
timeout /t 3 >nul
echo   [OK] API Server started on http://localhost:5000
echo.

REM Start Nexus UI (Frontend)
echo [3/3] Starting Nexus UI (Frontend)...
cd /d "D:\AIArm"
start "Nexus UI" cmd /k "python serve_ui.py"
timeout /t 3 >nul
echo   [OK] Nexus UI starting on http://localhost:3002
echo.

echo ================================================================================
echo                         NEXUS AI IS NOW RUNNING!
echo ================================================================================
echo.
echo   Frontend (React UI):  http://localhost:3002
echo   Backend (API):        http://localhost:5000
echo.
echo   The Nexus UI will open in your browser shortly...
echo.
echo   Press Ctrl+C in the server windows to stop individual components
echo   Or close this window to view status
echo.
echo ================================================================================
echo.

REM Wait a moment for servers to start, then open browser
timeout /t 5 >nul
start http://localhost:3002

echo.
echo System is running. You can minimize this window.
echo Press any key to exit (servers will continue running)...
pause >nul

exit
