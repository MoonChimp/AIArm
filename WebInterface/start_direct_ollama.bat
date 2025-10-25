@echo off
echo Starting Nexus with Direct Ollama Connection
echo =============================================
echo.

:: Check if port is already in use
echo Checking if port 45678 is available...
netstat -ano | findstr :45678 > nul
if %errorlevel% equ 0 (
    echo Port 45678 is already in use. Stopping the process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :45678') do taskkill /f /pid %%a
    timeout /t 2 > nul
)

:: Check if Ollama is running
echo Checking Ollama connection...
curl -s http://localhost:11434/api/version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Could not connect to Ollama on port 11434!
    echo.
    echo Please ensure Ollama is running with 'ollama serve' before continuing.
    echo.
    set /p CONTINUE="Do you want to continue anyway? (y/n): "
    if /i "%CONTINUE%" neq "y" exit /b 1
) else (
    echo.
    echo SUCCESS: Connected to Ollama successfully!
)

:: Start the server
echo.
echo Starting NexusAI with direct Ollama connection...
cd /d "%~dp0"

node real_server.js --bridge direct_ollama_bridge.py

echo.
echo Server stopped. Press any key to exit...
pause > nul