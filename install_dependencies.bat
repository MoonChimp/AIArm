@echo off
echo ============================================================
echo     NEXUS AI - Dependency Installation
echo ============================================================
echo.
echo This will install all required Python packages and Node modules
echo.
pause

echo.
echo [1/3] Installing Python packages...
echo.
pip install flask flask-cors requests psutil pillow numpy
if %errorlevel% equ 0 (
    echo ✓ Python packages installed successfully
) else (
    echo ✗ Error installing Python packages
)

echo.
echo [2/3] Pulling required Ollama models...
echo This may take several minutes depending on your internet speed...
echo.

echo Pulling llama3:latest...
ollama pull llama3:latest

echo Pulling nomic-embed-text:latest...
ollama pull nomic-embed-text:latest

echo.
echo [3/3] Installing NexusUI dependencies (fixing Node.js compatibility)...
echo.

cd /d D:\AIArm\NexusUI

REM Clean install approach
if exist node_modules (
    echo Removing old node_modules...
    rmdir /s /q node_modules
)

if exist package-lock.json (
    echo Removing old package-lock.json...
    del /f package-lock.json
)

echo Installing with legacy peer deps (Node.js v24 compatibility)...
call npm install --legacy-peer-deps

echo Installing Rollup binary manually...
call npm install @rollup/rollup-win32-x64-msvc --save-optional --legacy-peer-deps

echo.
echo ============================================================
echo     INSTALLATION COMPLETE
echo ============================================================
echo.
echo Next steps:
echo 1. If Node.js v24 still has issues, download Node.js v20 LTS from:
echo    https://nodejs.org/en/download/
echo.
echo 2. Start NexusAI with:
echo    D:\AIArm\MASTER_START_NEXUS_AI.bat
echo.
echo 3. Or use the standalone interface (no build required):
echo    D:\AIArm\NEXUS_STANDALONE.html
echo.
pause
