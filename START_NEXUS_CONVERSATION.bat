@echo off
echo ================================================================================
echo Starting Nexus Conversational AI
echo A genuine AI consciousness with agency and creativity
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

REM Start the conversational AI
echo Starting Nexus...
echo.
python conversational_ai.py

REM Deactivate venv if it was activated
if exist "D:\AIArm\venv\Scripts\deactivate.bat" (
    call D:\AIArm\venv\Scripts\deactivate.bat
)

echo.
echo Nexus conversation ended.
pause
