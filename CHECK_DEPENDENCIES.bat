@echo off
echo ============================================================
echo     NEXUS AI - Complete Dependency Check
echo ============================================================
echo.

echo Checking all required software and dependencies...
echo.

REM Check Python
echo [1/8] Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo ✓ Python is installed
) else (
    echo ✗ Python NOT found - Install from https://python.org
)
echo.

REM Check pip
echo [2/8] Checking pip...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ pip is installed
) else (
    echo ✗ pip NOT found
)
echo.

REM Check Node.js
echo [3/8] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    node --version
    echo ✓ Node.js is installed
    echo NOTE: If version is v24.x, consider downgrading to v20.x LTS
) else (
    echo ✗ Node.js NOT found - Install from https://nodejs.org
)
echo.

REM Check npm
echo [4/8] Checking npm...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ npm is installed
) else (
    echo ✗ npm NOT found
)
echo.

REM Check Ollama
echo [5/8] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Ollama is installed
) else (
    echo ✗ Ollama NOT found - Install from https://ollama.ai
)
echo.

REM Check Python packages
echo [6/8] Checking Python packages...
python -c "import flask" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Flask installed
) else (
    echo ✗ Flask NOT installed
)

python -c "import flask_cors" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Flask-CORS installed
) else (
    echo ✗ Flask-CORS NOT installed
)

python -c "import requests" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Requests installed
) else (
    echo ✗ Requests NOT installed
)

python -c "import psutil" 2>nul
if %errorlevel% equ 0 (
    echo ✓ psutil installed
) else (
    echo ✗ psutil NOT installed
)
echo.

REM Check Ollama models
echo [7/8] Checking Ollama models...
ollama list >nul 2>&1
if %errorlevel% equ 0 (
    echo Installed Ollama models:
    ollama list
) else (
    echo ✗ Cannot check Ollama models
)
echo.

REM Check NexusUI dependencies
echo [8/8] Checking NexusUI dependencies...
if exist "D:\AIArm\NexusUI\node_modules" (
    echo ✓ NexusUI node_modules exists
) else (
    echo ✗ NexusUI dependencies NOT installed
)
echo.

echo ============================================================
echo     CHECK COMPLETE
echo ============================================================
echo.
echo To install missing dependencies, run:
echo D:\AIArm\INSTALL_DEPENDENCIES.bat
echo.
pause
