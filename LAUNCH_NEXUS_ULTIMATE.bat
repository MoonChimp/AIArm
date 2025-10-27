@echo off
title NEXUS AI Ultimate Interface Launcher
color 0A

echo.
echo ========================================
echo  NEXUS AI ULTIMATE INTERFACE LAUNCHER
echo ========================================
echo.
echo The most stunning AI interface ever created!
echo.
echo Features:
echo - Real-time holographic panels
echo - Multi-agent AI system
echo - Advanced visual effects
echo - Voice input processing
echo - 3D spatial interface
echo - Particle systems
echo - Dynamic animations
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

echo Python is available. Starting Nexus AI Ultimate Interface...
echo.

REM Check if we're in the right directory
if not exist "NEXUS_ULTIMATE_INTERFACE.py" (
    echo ERROR: NEXUS_ULTIMATE_INTERFACE.py not found in current directory
    echo Please run this script from the D:\AIArm directory
    pause
    exit /b 1
)

echo Starting the Ultimate API Server...
echo Server will be available at: http://127.0.0.1:8001
echo.

REM Start the ultimate interface server
start "Nexus AI Ultimate Server" cmd /k "python NEXUS_ULTIMATE_INTERFACE.py"

echo.
echo Server is starting up...
echo.
echo ========================================
echo  UE5 SETUP INSTRUCTIONS
echo ========================================
echo.
echo 1. Open your NexusAI UE5 project
echo 2. Copy NEXUS_ULTIMATE_PANEL_SYSTEM.py to:
echo    Content/Python/
echo 3. In UE5 Python console, run:
echo    import NEXUS_ULTIMATE_PANEL_SYSTEM
echo    NEXUS_ULTIMATE_PANEL_SYSTEM.initialize_ultimate_interface()
echo.
echo 4. Create widgets in UE5:
echo    - CentralPanel_Widget (400x300)
echo    - SatellitePanel_Widget (200x150)
echo    - AgentAvatar Blueprint
echo    - Particle system Blueprints
echo.
echo 5. In Level Blueprint, add:
echo    Event BeginPlay -> initialize_ultimate_interface()
echo.
echo ========================================
echo  API ENDPOINTS TO TEST
echo ========================================
echo.
echo Chat with AI:
echo curl -X POST http://127.0.0.1:8001/chat -H "Content-Type: application/json" -d "{\"message\":\"Hello NexusAI\"}"
echo.
echo Execute commands:
echo curl -X POST http://127.0.0.1:8001/command -H "Content-Type: application/json" -d "{\"command\":\"/generate\",\"parameters\":{\"prompt\":\"a beautiful sunset\"}}"
echo.
echo Get agents:
echo curl http://127.0.0.1:8001/agents
echo.
echo ========================================
echo  VISUAL EFFECTS TO TRY
echo ========================================
echo.
echo - Type messages to see holographic responses
echo - Use /generate for image generation effects
echo - Use /code for programming animations
echo - Use /music for audio visualizations
echo - Use /analyze for data processing effects
echo.
echo ========================================
echo  TROUBLESHOOTING
echo ========================================
echo.
echo If panels don't appear:
echo - Check UE5 Output Log for errors
echo - Verify widget paths are correct
echo - Ensure Python script loaded successfully
echo.
echo If API doesn't respond:
echo - Check if port 8001 is available
echo - Verify Python path and dependencies
echo - Check Windows Firewall settings
echo.
echo ========================================
echo  SUCCESS CRITERIA
echo ========================================
echo.
echo When working, you should see:
echo - Central holographic panel in UE5
echo - 4 satellite panels around it
echo - AI agent avatars with colors
echo - Particle effects and animations
echo - Real-time text updates
echo - Stunning visual effects
echo.
echo ========================================
echo.

echo Press any key to open UE5 project...
pause >nul

REM Try to open UE5 project
if exist "NEXUS_UE5_PROJECT\NexusAI.uproject" (
    start "Unreal Engine 5" "NEXUS_UE5_PROJECT\NexusAI.uproject"
    echo UE5 project opened!
) else (
    echo UE5 project not found at expected location
    echo Please open your UE5 project manually
)

echo.
echo ========================================
echo  READY FOR THE ULTIMATE EXPERIENCE!
echo ========================================
echo.
echo Server running at: http://127.0.0.1:8001
echo UE5 interface ready for setup
echo.
echo Happy building! 🚀
echo.

pause
