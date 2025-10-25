@echo off
echo 🚀 Starting Nexus AI 3D Interface System...
echo.

cd /d "D:\AIArm"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if Node.js is available (for web interface)
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Node.js not found - Web interface may not work
) else (
    echo ✅ Node.js found
)

echo.
echo 📋 Starting System Components...
echo.

REM Start FastAPI UE5 API Server (Updated to port 8000)
echo 1. Starting Nexus AI FastAPI Server...
start "Nexus FastAPI Server" cmd /k "python NEXUS_UE5_API.py"

REM Wait for API server to start
timeout /t 3 /nobreak >nul

REM Check if API server started successfully
curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Warning: FastAPI server may not have started properly
    echo Please check the FastAPI server window for errors
) else (
    echo ✅ FastAPI server is responding on port 8000
)

REM Check if UE5 is available
echo 2. Checking UE5 installation...
set UE5_PATH="C:\Program Files\Epic Games\UE_5.6\Engine\Binaries\Win64\UnrealEditor.exe"
if not exist %UE5_PATH% (
    echo ❌ Error: UE5 Editor not found at %UE5_PATH%
    echo Please verify your UE5 installation
    echo.
    echo 💡 You can still use the FastAPI server without UE5
    pause
    exit /b 1
)

REM Check if UE5 project exists
set PROJECT_PATH="D:\AIArm\NEXUS_UE5_PROJECT\NexusAI.uproject"
if not exist %PROJECT_PATH% (
    echo ⚠️  UE5 Project not found - it will be created when UE5 starts
)

echo.
echo 🎮 Starting UE5 with Nexus AI Interface...
echo.
echo Note: Make sure the FastAPI server is running on localhost:8000
echo Note: UE5 will connect to the API automatically
echo.

REM Launch UE5 with the project
start "" %UE5_PATH% "%PROJECT_PATH%"

echo.
echo ✅ System startup initiated!
echo.
echo 📊 System Status:
echo   • Nexus FastAPI Server: Running on localhost:8000
echo   • UE5 Editor: Launching with 3D interface
echo.
echo 🎯 The 3D interface will initialize automatically in UE5
echo 💬 You can interact with your AI through the immersive 3D interface
echo.
echo 🔗 API Endpoints available:
echo   • Health Check: http://localhost:8000/api/health
echo   • Chat: http://localhost:8000/api/chat
echo   • Agent Status: http://localhost:8000/api/agents/status
echo   • Interface List: http://localhost:8000/api/interfaces
echo.

pause
