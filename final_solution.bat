@echo off
echo =====================================================================
echo            AIArm FINAL SOLUTION - With Real Orchestrator
echo =====================================================================
echo.

echo STEP 1: Killing ALL Node.js processes...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 >nul

echo STEP 2: Checking that orchestrator bridge works...
python WebInterface\orchestrator_bridge.py
echo.

echo STEP 3: Starting server on port 45678...
echo This server will connect to your REAL orchestrator using the process_request method
echo.
echo Once the server is running, open your browser and navigate to the URL shown.
echo.

cd /D "D:\AIArm\WebInterface"
node final_server.js

pause
