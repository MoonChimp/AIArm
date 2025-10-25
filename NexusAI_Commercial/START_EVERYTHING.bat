@echo off
echo ========================================
echo  NexusAI Complete Startup
echo ========================================
echo.
echo This will start:
echo   1. Ollama (AI Engine)
echo   2. NexusAI Backend (API Server - Port 5000)
echo   3. Web Server (File Server - Port 8080)
echo.
echo Access your webapp from ANY device:
echo   http://192.168.1.230:8080/html/chat.html
echo.
echo ========================================
echo.

REM Check if Ollama is already running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama is already running
) else (
    echo Starting Ollama...
    start "Ollama Server" ollama serve
    timeout /t 3 /nobreak >nul
)

REM Start NexusAI Backend
echo.
echo Starting NexusAI Backend API on port 5000...
start "NexusAI Backend" cmd /k "cd /d D:\AIArm\NexusAI_Commercial\backend && python nexus_functional_api.py"
timeout /t 3 /nobreak >nul

REM Start Web Server
echo.
echo Starting Web Server on port 8080...
start "NexusAI WebServer" cmd /k "cd /d D:\AIArm\NexusAI_Commercial && python -m http.server 8080"

echo.
echo ========================================
echo  All Services Started!
echo ========================================
echo.
echo Access your webapp:
echo   From this PC: http://localhost:8080/html/chat.html
echo   From other devices: http://192.168.1.230:8080/html/chat.html
echo.
echo API Status: http://192.168.1.230:5000/api/status
echo.
echo Three windows have opened:
echo   1. Ollama Server
echo   2. NexusAI Backend (Port 5000)
echo   3. Web Server (Port 8080)
echo.
echo Keep all windows running!
echo ========================================
echo.
pause
