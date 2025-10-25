@echo off
echo =====================================================================
echo            AIArm LOCAL OLLAMA LAUNCHER - 100%% Local AI
echo =====================================================================
echo.

echo STEP 1: Killing any existing Node.js processes...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 >nul

echo STEP 2: Installing required Node.js packages...
cd /D "D:\AIArm\WebInterface"
echo Installing express, cors, and body-parser...
call npm install express cors body-parser --silent
if %ERRORLEVEL% NEQ 0 (
    echo Error installing Node.js packages. Please make sure Node.js is installed.
    goto end
)

echo STEP 3: Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not running or not accessible at localhost:11434
    echo Please start Ollama before launching the system.
    goto end
)

echo Checking Ollama models...
echo Available Ollama models:
ollama list

echo STEP 4: Setting bridge file to use ollama_bridge.py...
echo.
set BRIDGE_FILE=ollama_bridge.py
echo Bridge set to: %BRIDGE_FILE%
echo.

echo STEP 5: Starting server on port 45678 with 100%% local Ollama models...
echo Once the server is running, open your browser and navigate to the URL shown.
echo.

node "D:\AIArm\WebInterface\real_server.js" --bridge %BRIDGE_FILE%

:end
pause
