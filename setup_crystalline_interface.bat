@echo off
echo [1;36m=====================================================================[0m
echo [1;36m        AIArm Crystalline Interface - Initial Setup[0m
echo [1;36m=====================================================================[0m
echo.

:: Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [1;31mERROR: Node.js is not installed. Please install Node.js and try again.[0m
    echo [1;33mYou can download Node.js from: https://nodejs.org/[0m
    pause
    exit /b 1
)

:: Create WebInterface directory if it doesn't exist
if not exist "D:\AIArm\WebInterface" (
    echo [1;33mCreating WebInterface directory...[0m
    mkdir "D:\AIArm\WebInterface"
)

:: Change to WebInterface directory
cd /d "D:\AIArm\WebInterface"

:: Create package.json if it doesn't exist
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
echo [1;33mInstalling required Node.js packages...[0m
call npm install

if %errorlevel% neq 0 (
    echo [1;31mERROR: Failed to install required packages.[0m
    pause
    exit /b 1
)

echo.
echo [1;32mInitial setup completed successfully![0m
echo [1;32mYou can now run the AIArm Crystalline Interface using:[0m
echo [1;36mD:\AIArm\start_crystalline_multiagent.bat[0m
echo.

pause
