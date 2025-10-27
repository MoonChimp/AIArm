@echo off
REM NexusAI Quick Setup Script
REM Run this in D:\AIArm directory

echo ============================================
echo NexusAI Enhanced Setup
echo ============================================
echo.

REM Check if we're in the right directory
if not exist "NEXUS_UE5_PROJECT" (
    echo ERROR: Please run this script from D:\AIArm directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [1/5] Installing Python dependencies...
pip install fastapi uvicorn websockets python-multipart --upgrade
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
    echo Continue anyway? Press any key...
    pause >nul
)

echo.
echo [2/5] Backing up old API server...
if exist "NEXUS_UE5_API_SIMPLIFIED.py" (
    copy /Y "NEXUS_UE5_API_SIMPLIFIED.py" "NEXUS_UE5_API_SIMPLIFIED.py.backup"
    echo Backup created: NEXUS_UE5_API_SIMPLIFIED.py.backup
)

echo.
echo [3/5] Installing enhanced API server...
if exist "NEXUS_ENHANCED_API.py" (
    echo Enhanced API already present
) else (
    echo ERROR: NEXUS_ENHANCED_API.py not found!
    echo Please copy it to this directory first
    pause
    exit /b 1
)

echo.
echo [4/5] Installing UE5 Python scripts...
if not exist "NEXUS_UE5_PROJECT\Content\Python" (
    mkdir "NEXUS_UE5_PROJECT\Content\Python"
)

if exist "NexusAI_Panel_System.py" (
    copy /Y "NexusAI_Panel_System.py" "NEXUS_UE5_PROJECT\Content\Python\"
    echo Panel system installed
)

echo.
echo [5/5] Creating startup script...
(
echo @echo off
echo echo Starting NexusAI Enhanced API Server...
echo python NEXUS_ENHANCED_API.py
) > start_nexusai_server.bat

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Run: start_nexusai_server.bat
echo 2. Open UE5 project
echo 3. Follow NEXUS_BUILD_INSTRUCTIONS.md
echo.
echo Press any key to start the API server now...
pause >nul

start_nexusai_server.bat

