@echo off
echo Starting Nexus AI Unified Application...
echo.

cd /d "D:\AIArm"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required modules are installed
echo Checking dependencies...
python -c "import tkinter, requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required modules...
    pip install requests
)

echo.
echo Starting Nexus Unified Application...
echo.
echo Note: Make sure Ollama is running on localhost:11434
echo Note: Make sure Stable Diffusion is running on localhost:7860 (optional)
echo.

python NEXUS_UNIFIED_APP.py

pause
