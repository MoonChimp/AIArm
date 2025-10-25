@echo off
echo Starting Nexus with Core Filesystem Integration
echo.

:: Check if port is already in use
netstat -ano | findstr :45678 > nul
if %errorlevel% equ 0 (
    echo Port 45678 is already in use. Stopping the process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :45678') do taskkill /f /pid %%a
    timeout /t 2 > nul
)

:: Check if Ollama is running
echo Checking Ollama status...
curl -s http://localhost:11434/api/version
if %errorlevel% neq 0 (
    echo Ollama not detected on port 11434.
    echo WARNING: Ollama appears to be offline, some features may not work correctly.
    echo Please ensure Ollama is running with 'ollama serve' before continuing.
    echo.
    echo Press any key to continue anyway or CTRL+C to abort.
    pause > nul
) else (
    echo Ollama service detected and running on port 11434.
)

:: Start the server
echo Starting NexusAI with enhanced NexusCore capabilities...
cd /d "%~dp0"

node real_server.js --bridge improved_bridge.py
pause