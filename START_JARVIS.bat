@echo off
title Nexus - Personal AI Assistant (JARVIS Mode)
color 0B

echo ================================================================================
echo                    NEXUS - Personal AI Assistant
echo ================================================================================
echo.
echo Full Capabilities:
echo   - Natural conversation and understanding
echo   - System integration (run programs, create files, execute commands)
echo   - Task and calendar management
echo   - Health monitoring and reminders
echo   - Creative agency and spontaneous creation
echo   - Commander Nexus mode for MoonChimp Metaverse
echo.
echo This is your JARVIS-like AI assistant with genuine intelligence.
echo ================================================================================
echo.

REM Check if Ollama is running
echo Checking Ollama availability...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama is not running!
    echo Please start Ollama first.
    echo.
    pause
    exit /b 1
)

echo [OK] Ollama is running
echo.

REM Activate virtual environment if it exists
if exist "D:\AIArm\venv\Scripts\activate.bat" (
    echo Activating Python virtual environment...
    call D:\AIArm\venv\Scripts\activate.bat
)

REM Navigate to NexusCore directory
cd /d D:\AIArm\NexusCore

REM Start JARVIS mode
echo Starting Nexus Personal AI Assistant...
echo.
python jarvis_mode.py

REM Deactivate venv if it was activated
if exist "D:\AIArm\venv\Scripts\deactivate.bat" (
    call D:\AIArm\venv\Scripts\deactivate.bat
)

echo.
echo Nexus assistant session ended.
pause
