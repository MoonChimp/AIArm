@echo off
setlocal EnableDelayedExpansion

echo =====================================================================
echo             AIArm Port Cleanup Utility
echo =====================================================================
echo.
echo This utility will identify and kill processes using ports 3000-3050
echo.

REM Find and kill Node.js processes directly
echo Checking for Node.js processes...
for /f "tokens=1" %%p in ('tasklist /fi "IMAGENAME eq node.exe" /fo csv /nh') do (
    set PROC=%%p
    set PROC=!PROC:"=!
    if "!PROC!"=="node.exe" (
        for /f "tokens=2" %%i in ('tasklist /fi "IMAGENAME eq node.exe" /fo csv /nh') do (
            set PID=%%i
            set PID=!PID:"=!
            echo Found Node.js process with PID: !PID!
            echo Killing process with PID: !PID!
            taskkill /F /PID !PID!
        )
    )
)

REM Check for processes on specific ports
echo.
echo Checking for processes on specific ports...

for %%p in (3000 3001 3002 3003 3050) do (
    echo Checking port %%p...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%%p') do (
        set PID=%%a
        echo Port %%p is used by PID: !PID!
        echo Attempting to kill process with PID: !PID!
        taskkill /F /PID !PID!
    )
)

echo.
echo Port cleanup completed.
echo.
echo You can now restart the AIArm server.
echo.

endlocal
pause
