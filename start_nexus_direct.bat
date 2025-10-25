@echo off
echo ===================================================================== 
echo NEXUS AI DIRECT - START
echo ===================================================================== 

REM Check if Ollama is running
echo Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama is not running! Please start Ollama before running this script.
    echo Visit http://localhost:11434 to verify Ollama is running.
    pause
    exit /b 1
)
echo [SUCCESS] Ollama is running

REM Check if the enhanced model exists
echo Checking for enhanced Nexus AI model...
curl -s http://localhost:11434/api/tags | findstr "nexusai-enhanced" > nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Enhanced Nexus AI model not found!
    echo Please run setup_nexus_direct.bat first to create the model.
    pause
    exit /b 1
)
echo [SUCCESS] Found nexusai-enhanced:latest model

REM Start the server
echo Starting Nexus AI Direct server...
cd D:\AIArm\WebInterface
start "Nexus AI Direct" python nexus_direct_server.py

echo ===================================================================== 
echo NEXUS AI DIRECT - STARTED
echo ===================================================================== 
echo.
echo The server is now running and your browser should open automatically.
echo If not, visit: http://localhost:8000/nexus_direct.html
echo.
echo To stop the server, close the command prompt window that opened.
echo.
echo Press any key to exit this window...
pause > nul
