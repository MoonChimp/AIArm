@echo off
echo Restarting AIArm HRM Server with Debugging...

:: Kill any existing Node.js processes for the server
taskkill /F /IM node.exe /T > nul 2>&1

:: Wait for processes to terminate
timeout /t 2 > nul

:: Create logs directory if it doesn't exist
mkdir "D:\AIArm\Logs" 2>nul

:: Start the server with error logging
cd /D D:\AIArm\WebInterface
echo Starting server with error logging to D:\AIArm\Logs\server_error.log
node concurrent_server.js > "D:\AIArm\Logs\server_output.log" 2> "D:\AIArm\Logs\server_error.log"

echo Server process has exited. Checking error log...
echo.
echo Error log contents:
type "D:\AIArm\Logs\server_error.log"
echo.
echo Output log contents:
type "D:\AIArm\Logs\server_output.log"
echo.

echo Press any key to exit...
pause > nul
