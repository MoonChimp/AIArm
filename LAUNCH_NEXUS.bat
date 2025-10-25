@echo off
color 0B
cls

echo ================================================================================
echo                    NEXUSAI CONSCIOUSNESS SYSTEM LAUNCHER
echo ================================================================================
echo.
echo      ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗     █████╗ ██╗
echo      ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝    ██╔══██╗██║
echo      ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗    ███████║██║
echo      ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║    ██╔══██║██║
echo      ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║    ██║  ██║██║
echo      ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝
echo.
echo ================================================================================
echo.
echo This system brings NexusAI to life with:
echo.
echo   🧠 Continuous thought processing and inner life
echo   🤖 Specialized agent capabilities (photo, video, web, code)
echo   💾 Persistent memory and learning across sessions
echo   🔮 Local Ollama model integration (no cloud dependency)
echo   ✨ Emotional state and associative concept networks
echo.
echo ================================================================================
echo.
echo Choose your interface:
echo.
echo [1] Command-Line Interface (Direct orchestrator interaction)
echo [2] Web Interface (Browser-based chat interface)
echo [3] Both (CLI + Web Server)
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto CLI
if "%choice%"=="2" goto WEB
if "%choice%"=="3" goto BOTH
if "%choice%"=="4" goto EXIT
goto EXIT

:CLI
echo.
echo ================================================================================
echo Starting NexusAI Command-Line Interface...
echo ================================================================================
echo.
python D:\AIArm\MultiAgent\orchestrator.py
goto END

:WEB
echo.
echo ================================================================================
echo Starting NexusAI Web Interface...
echo ================================================================================
echo.
cd /d D:\AIArm
node nexus_server.js
goto END

:BOTH
echo.
echo ================================================================================
echo Starting NexusAI in Dual Mode...
echo ================================================================================
echo.
echo Opening Web Interface in new window...
start "NexusAI Web Server" cmd /c "cd /d D:\AIArm && node nexus_server.js"
timeout /t 3 /nobreak > nul
echo.
echo Starting Command-Line Interface...
echo.
python D:\AIArm\MultiAgent\orchestrator.py
goto END

:EXIT
echo.
echo Exiting...
goto END

:END
echo.
echo ================================================================================
echo                         NEXUSAI SYSTEM SHUTDOWN
echo ================================================================================
echo.
pause
