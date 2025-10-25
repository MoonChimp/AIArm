@echo off
echo =====================================================================
echo             AIArm Port Cleanup Utility
echo =====================================================================
echo.
echo This utility will identify and kill processes using ports 3000-3050
echo.

echo Checking for processes using port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    set PID=%%a
    echo Port 3000 is used by PID: !PID!
    echo Killing process with PID: !PID!
    taskkill /F /PID !PID!
)

echo Checking for processes using port 3001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001') do (
    set PID=%%a
    echo Port 3001 is used by PID: !PID!
    echo Killing process with PID: !PID!
    taskkill /F /PID !PID!
)

echo Checking for processes using port 3002...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3002') do (
    set PID=%%a
    echo Port 3002 is used by PID: !PID!
    echo Killing process with PID: !PID!
    taskkill /F /PID !PID!
)

echo Checking for processes using port 3003...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3003') do (
    set PID=%%a
    echo Port 3003 is used by PID: !PID!
    echo Killing process with PID: !PID!
    taskkill /F /PID !PID!
)

echo Checking for processes using port 3050...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3050') do (
    set PID=%%a
    echo Port 3050 is used by PID: !PID!
    echo Killing process with PID: !PID!
    taskkill /F /PID !PID!
)

echo.
echo Port cleanup completed.
echo.
echo You can now restart the AIArm server.
echo.

pause
