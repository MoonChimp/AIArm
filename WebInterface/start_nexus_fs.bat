@echo off
title Nexus AI - FileSystem Interface
echo Starting Nexus AI with FileSystem capabilities...
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
    echo Using enhanced_orchestrator as fallback...
) else (
    echo Ollama is available! Using ollama_bridge.py...
    SET BRIDGE=ollama_bridge.py
    goto :startserver
)

echo Starting server on port %PORT%...
:startserver
if not defined BRIDGE SET BRIDGE=improved_bridge.py
echo Using bridge: %BRIDGE%

node "real_server.js" --port %PORT% --bridge %BRIDGE%

if %errorlevel% neq 0 (
    echo.
    echo Server failed to start! Error code: %errorlevel%
    echo Trying alternate approach...
    echo.
    timeout /t 2 /nobreak > nul
    
    if "%BRIDGE%"=="improved_bridge.py" (
        echo Starting with ollama_bridge.py configuration...
        node "real_server.js" --port %PORT% --bridge ollama_bridge.py
    ) else (
        echo Starting with improved_bridge.py configuration...
        node "real_server.js" --port %PORT% --bridge improved_bridge.py
    )
)

echo.
echo Server terminated.
echo.
pause