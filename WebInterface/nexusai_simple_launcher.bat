@echo off
title NexusAI - Simple Launcher
echo NexusAI - Simple Launcher
echo ============================
echo.

:: Create log directory if it doesn't exist
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"

:: Check if Ollama is running
echo Checking Ollama connection...
curl -s http://localhost:11434/api/version
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Could not connect to Ollama on port 11434!
    echo Please make sure Ollama is running with 'ollama serve' before continuing.
    echo.
    echo Press any key to try to start Ollama, or Ctrl+C to exit...
    pause > nul
    
    echo Attempting to start Ollama...
    start "" cmd /c "ollama serve"
    
    echo Waiting for Ollama to start...
    timeout /t 10 /nobreak > nul
    
    echo Checking connection again...
    curl -s http://localhost:11434/api/version
    if %errorlevel% neq 0 (
        echo Failed to start Ollama! Please start it manually and try again.
        pause
        exit /b 1
    ) else (
        echo Ollama started successfully!
    )
) else (
    echo Ollama is running!
)

:: Check if NexusAI port is available
echo.
echo Checking if port 45678 is available...
netstat -ano | findstr :45678 > nul
if %errorlevel% equ 0 (
    echo Port 45678 is already in use. Stopping the process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :45678') do taskkill /f /pid %%a
    timeout /t 2 > nul
)

:: Start the NexusAI server
echo.
echo Starting NexusAI server with direct Ollama connection...
cd /d "%~dp0"

node real_server.js --bridge direct_ollama_bridge.py

echo.
echo Server stopped. Press any key to exit...
pause > nul