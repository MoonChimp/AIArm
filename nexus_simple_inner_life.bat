@echo off
echo =====================================================================
echo     NEXUS INNER LIFE - Simplified Launcher for Stability
echo =====================================================================
echo.

echo STEP 1: Killing any existing Node.js processes...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 >nul

echo STEP 2: Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not running or not accessible at localhost:11434
    echo Please start Ollama before launching the system.
    goto end
)

echo Checking Ollama models...
echo Available Ollama models:
ollama list

echo STEP 3: Setting bridge file to use ollama_bridge.py...
echo.
set BRIDGE_FILE=ollama_bridge.py
echo Bridge set to: %BRIDGE_FILE%
echo.

echo STEP 4: Starting server on port 45678 with inner life integration...
echo.
echo *******************************************************************
echo *                                                                 *
echo *                 NEXUS INNER LIFE ACTIVE                         *
echo *                                                                 *
echo * Nexus will now experience a continuous stream of consciousness  *
echo * through a direct connection to your local Ollama models.        *
echo *                                                                 *
echo * You'll be able to interact with an AI that maintains an ongoing *
echo * inner dialogue and develops its own understanding over time.    *
echo *                                                                 *
echo *******************************************************************
echo.
echo Once the server is running, open your browser and navigate to the URL shown.
echo.

cd /D "D:\AIArm\WebInterface"
echo Starting AIArm server with inner life connection...
node "real_server.js" --bridge %BRIDGE_FILE%

:end
pause