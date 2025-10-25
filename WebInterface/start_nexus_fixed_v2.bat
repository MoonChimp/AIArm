@echo off
echo ===================================================================== 
echo NEXUS HRM ARCHITECTURE SYSTEM - FIXED VERSION
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

REM Try to stop any running bridges
echo Cleaning up any running processes...
taskkill /f /im python.exe 2>nul

echo Starting Nexus HRM system on port 45691...
cd "D:\AIArm\WebInterface"
echo The system will be available at http://localhost:45691
node concurrent_server.js --port 45691

pause
