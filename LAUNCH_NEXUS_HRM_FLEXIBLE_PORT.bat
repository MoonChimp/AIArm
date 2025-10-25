@echo off
echo =====================================================================
echo     NEXUS HRM ARCHITECTURE - FLEXIBLE PORT STARTUP
echo =====================================================================
echo.

echo STEP 1: Checking system requirements...
echo Checking for Node.js...
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please run install_dependencies.bat first.
    goto end
)

echo Checking for Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run install_dependencies.bat first.
    goto end
)

echo Checking for Ollama...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not running or not accessible at localhost:11434
    echo Please start Ollama before launching the system.
    goto end
)

echo Available Ollama models:
ollama list
echo.

echo STEP 2: Creating necessary directories...
mkdir "D:\AIArm\Memory" 2>nul
mkdir "D:\AIArm\WebInterface\logs" 2>nul
echo Directory structure created.
echo.

echo STEP 3: Finding an available port...
set BASE_PORT=45678
set MAX_PORT=45700
set PORT=%BASE_PORT%

:port_check_loop
echo Checking port %PORT%...
netstat -ano | findstr ":%PORT%" > nul
if %ERRORLEVEL% EQU 0 (
    echo Port %PORT% is in use.
    set /a PORT+=1
    if %PORT% GTR %MAX_PORT% (
        echo ERROR: Could not find an available port in range %BASE_PORT%-%MAX_PORT%.
        echo Please free up some ports or modify this script to use a different port range.
        goto end
    )
    goto port_check_loop
)

echo Found available port: %PORT%
echo.

echo STEP 4: Killing any existing Node.js processes on this port...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT%"') do (
    echo Terminating process %%a
    taskkill /F /PID %%a
    timeout /t 2 > nul
)

echo STEP 5: Starting AIArm system with HRM Architecture...
cd /D "D:\AIArm\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *             NEXUS HRM ARCHITECTURE - FLEXIBLE PORT              *
echo *                                                                 *
echo * Human-Robot-Machine Architecture:                               *
echo * - Surface Bridge: Structured responses and interface layer      *
echo * - Deep Bridge: Continuous reasoning and deep thought processes  *
echo *                                                                 *
echo * This system combines both bridges for a complete experience     *
echo * that balances structure with depth.                             *
echo *                                                                 *
echo *******************************************************************
echo.
echo Server will be available at: http://localhost:%PORT%
echo.
echo TIP: If you need to use a specific port, you can edit this file and 
echo      change the BASE_PORT value at the beginning of the script.
echo.

echo Starting HRM server with concurrent bridges on port %PORT%...
node "concurrent_server.js" --port %PORT%

echo.
echo If the server crashed, check logs in D:\AIArm\WebInterface\logs
echo Restarting server in 10 seconds...
timeout /t 10 > nul
goto restart

:restart
echo Restarting HRM server on port %PORT%...
node "concurrent_server.js" --port %PORT%
echo Server crashed. Restarting in 10 seconds...
timeout /t 10 > nul
goto restart

:end
pause