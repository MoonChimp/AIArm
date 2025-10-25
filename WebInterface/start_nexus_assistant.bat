@echo off
title Nexus AI - Intelligent Personal Assistant
echo Starting Nexus AI Intelligent Personal Assistant...
echo.

SET PORT=45678

echo Checking if port %PORT% is available...
netstat -ano | findstr ":%PORT% " > nul
if %errorlevel% equ 0 (
    echo Port %PORT% is already in use!
    echo Attempting to free the port...
    
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT% "') do (
        echo Killing process with PID %%a
        taskkill /f /pid %%a
        timeout /t 2 /nobreak > nul
    )
)

echo Setting up Nexus AI Personal Assistant...

REM Create Logs directory if it doesn't exist
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"

REM Create Memory directory if it doesn't exist
if not exist "D:\AIArm\Memory" mkdir "D:\AIArm\Memory"

echo Starting server on port %PORT%...
node "real_server.js" --port %PORT% --bridge improved_bridge.py

if %errorlevel% neq 0 (
    echo.
    echo Server failed to start! Error code: %errorlevel%
    echo Trying alternate approach...
    echo.
    timeout /t 2 /nobreak > nul
    
    echo Starting with direct bridge...
    node "real_server.js" --port %PORT% --bridge bridge_wrapper.py
)

echo.
echo Server terminated.
echo.
pause