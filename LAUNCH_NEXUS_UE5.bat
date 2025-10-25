@echo off
echo 🚀 Starting Nexus AI UE5 3D Interface...
echo.

REM Set UE5 installation path
set UE5_PATH="C:\Program Files\Epic Games\UE_5.6\Engine\Binaries\Win64\UnrealEditor.exe"
set PROJECT_PATH="D:\AIArm\NEXUS_UE5_PROJECT\NexusAI.uproject"

REM Check if UE5 exists
if not exist %UE5_PATH% (
    echo ❌ Error: UE5 Editor not found at %UE5_PATH%
    echo Please verify your UE5 installation path
    pause
    exit /b 1
)

REM Check if project exists
if not exist %PROJECT_PATH% (
    echo ⚠️  UE5 Project not found at %PROJECT_PATH%
    echo The project will be created when UE5 starts
)

echo.
echo 🎮 Starting UE5 with Nexus AI Interface...
echo.
echo Note: Make sure the FastAPI server is running on localhost:8000
echo Note: The 3D interface will connect to the API automatically
echo.

REM Launch UE5 with the project
start "" %UE5_PATH% "%PROJECT_PATH%"

echo.
echo ✅ UE5 is starting...
echo 🎯 The 3D interface will initialize automatically
echo 🔗 UE5 will connect to: http://localhost:8000/api/chat
echo.

pause
