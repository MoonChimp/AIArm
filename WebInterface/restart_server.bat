@echo off
echo Restarting AIArm HRM Server...

:: Kill any existing Node.js processes for the server
taskkill /F /IM node.exe /T > nul 2>&1

:: Wait for processes to terminate
timeout /t 2 > nul

:: Start the server
cd /D D:\AIArm\WebInterface
start "AIArm HRM Concurrent Server" cmd /c "node concurrent_server.js"

echo Server restarted. Please go to http://localhost:45678 in your browser.
echo Press any key to exit...
pause > nul
