@echo off
echo =====================================================================
echo            AIArm FINAL LAUNCHER - With Real Orchestrator
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

echo STEP 3: Checking Python orchestrator availability...
python -c "import sys; sys.path.append('D:/AIArm/MultiAgent'); import enhanced_orchestrator; print('Orchestrator module available: True')"
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Orchestrator module check failed. The interface might not be able to connect to the AI agents.
    echo The interface will still start, but actual AI functionality may be limited.
    echo.
)

echo STEP 4: Starting server on port 45678...
echo This server will connect to your REAL orchestrator using the process_request method
echo.
echo Once the server is running, open your browser and navigate to the URL shown.
echo.

node "D:\AIArm\WebInterface\real_server.js"

:end
pause
