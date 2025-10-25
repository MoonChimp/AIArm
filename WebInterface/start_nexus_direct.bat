@echo off
title Nexus AI - Direct Bridge Filesystem Interface
echo Starting Nexus AI with Direct Bridge and FileSystem capabilities...
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

echo Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %errorlevel% neq 0 (
    echo WARNING: Ollama is not running or not available!
    echo Make sure Ollama is running on port 11434 before continuing.
    echo.
    choice /c YN /m "Do you want to continue anyway?"
    if %errorlevel% neq 1 exit /b
    echo.
    echo You chose to continue, but the system may not work correctly without Ollama.
    echo.
) else (
    echo Ollama is available! Using direct bridge...
)

echo Starting server on port %PORT% with direct bridge...
node "real_server.js" --port %PORT% --bridge bridge_wrapper.py

echo.
echo Server terminated.
echo.
pause