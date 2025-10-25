@echo off
echo =====================================================================
echo                   AIArm Minimal Test Server
echo =====================================================================
echo.

:: Change to WebInterface directory
cd /d "D:\AIArm\WebInterface"

:: Ensure npm packages are installed
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install express
    if %errorlevel% neq 0 (
        echo Failed to install express!
        pause
        exit /b 1
    )
)

:: Start the minimal server
echo Starting minimal server on port 3050...
echo Once started, open http://localhost:3050/simple_interface.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

node minimal_server.js

pause
