@echo off
echo [1;36m=====================================================================[0m
echo [1;36m        AIArm Crystalline Multi-Agent System Launcher[0m
echo [1;36m=====================================================================[0m
echo.

:: Create necessary directories
if not exist "D:\AIArm\WebInterface\Logs" mkdir "D:\AIArm\WebInterface\Logs"
if not exist "D:\AIArm\TaskQueue" mkdir "D:\AIArm\TaskQueue"

:: Set the status to online
echo online > "D:\AIArm\WebInterface\service_status.txt"

:: Check if port 3000 is in use
echo [1;33mChecking if port 3000 is available...[0m
setlocal EnableDelayedExpansion
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    set PID=%%a
    echo [1;31mPort 3000 is in use by process !PID![0m
    
    :: Ask if user wants to kill the process
    set /p KILL_PROCESS=[1;33mWould you like to try killing this process to free port 3000? (Y/N) [0m
    
    if /i "!KILL_PROCESS!"=="Y" (
        echo [1;33mAttempting to kill process !PID!...[0m
        taskkill /F /PID !PID!
        
        if !errorlevel! equ 0 (
            echo [1;32mProcess successfully terminated. Port 3000 is now available.[0m
        ) else (
            echo [1;31mFailed to terminate process. The server will try alternate ports.[0m
        )
    ) else (
        echo [1;33mPort 3000 remains in use. The server will try alternate ports.[0m
    )
    
    goto :port_check_done
)

echo [1;32mPort 3000 is available.[0m

:port_check_done
endlocal

:: Start the Python bridge in a new window
start "AIArm Python Bridge" cmd /c "python D:\AIArm\WebInterface\bridge.py"

:: Start the web server in this window
cd /d "D:\AIArm\WebInterface"

:: Check if necessary packages are installed
if not exist "node_modules" (
    echo [1;33mInstalling required packages...[0m
    
    :: Install dependencies
    call npm install
    
    if %errorlevel% neq 0 (
        echo [1;31mERROR: Failed to install required packages.[0m
        pause
        exit /b 1
    )
)

echo [1;32mStarting AIArm Crystalline Interface server...[0m
echo [1;32mOnce the server is running, open a web browser and go to:[0m
echo [1;36mhttp://localhost:3000[0m
echo.
echo [1;33mPress Ctrl+C to stop the server[0m
echo.

:: Start the Node.js server
node server.js

echo.
echo [1;31mServer has been stopped.[0m

:: Cleanup
echo offline > "D:\AIArm\WebInterface\service_status.txt"
taskkill /F /FI "WINDOWTITLE eq AIArm Python Bridge" > nul 2>&1

pause
