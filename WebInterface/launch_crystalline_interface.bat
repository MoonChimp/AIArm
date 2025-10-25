@echo off
echo [1;36m=====================================================================[0m
echo [1;36m                   AIArm Crystalline Interface[0m
echo [1;36m=====================================================================[0m
echo.

echo [1;33mInitializing AIArm Multi-Agent System with Crystalline Interface...[0m
echo.

:: Create necessary directories if they don't exist
if not exist "TaskQueue" mkdir TaskQueue
if not exist "Logs" mkdir Logs

:: Set the status to online
echo online > service_status.txt

:: Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [1;31mERROR: Node.js is not installed. Please install Node.js and try again.[0m
    pause
    exit /b 1
)

:: Check if necessary packages are installed
if not exist "node_modules" (
    echo [1;33mInstalling required packages...[0m
    
    :: Check if package.json exists
    if not exist "package.json" (
        echo [1;33mCreating package.json...[0m
        echo {
        echo   "name": "aiarm-crystalline-interface",
        echo   "version": "1.0.0",
        echo   "description": "AIArm Multi-Agent System Crystalline Interface",
        echo   "main": "server.js",
        echo   "scripts": {
        echo     "start": "node server.js"
        echo   },
        echo   "dependencies": {
        echo     "express": "^4.18.2",
        echo     "cors": "^2.8.5",
        echo     "body-parser": "^1.20.2"
        echo   }
        echo }
        ) > package.json
    )
    
    :: Install dependencies
    call npm install
    
    if %errorlevel% neq 0 (
        echo [1;31mERROR: Failed to install required packages.[0m
        pause
        exit /b 1
    )
)

:: Start the server
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
pause
