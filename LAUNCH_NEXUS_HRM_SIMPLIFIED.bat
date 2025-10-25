@echo off
echo =====================================================================
echo     NEXUS HRM ARCHITECTURE - SIMPLIFIED STARTUP
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

echo STEP 3: Checking for available port...
set PORT=45678
netstat -ano | findstr ":%PORT%" > nul
if %ERRORLEVEL% EQU 0 (
    echo Port %PORT% is already in use. Trying alternative port 45679...
    set PORT=45679
    netstat -ano | findstr ":%PORT%" > nul
    if %ERRORLEVEL% EQU 0 (
        echo Port %PORT% is also in use. Trying alternative port 45680...
        set PORT=45680
        netstat -ano | findstr ":%PORT%" > nul
        if %ERRORLEVEL% EQU 0 (
            echo ERROR: Could not find an available port.
            echo Please ensure ports 45678-45680 are available or modify this script.
            goto end
        )
    )
)
echo Will use port %PORT% for the server.
echo.

echo STEP 4: Starting AIArm system with HRM Architecture...
cd /D "D:\AIArm\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *             NEXUS HRM ARCHITECTURE - SIMPLIFIED                 *
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
echo Once the server is running, open your browser to http://localhost:%PORT%
echo.

echo Starting HRM server with concurrent bridges...
node "concurrent_server.js" --port %PORT%

echo.
echo If the server crashed, check logs in D:\AIArm\WebInterface\logs
echo Restarting server in 10 seconds...
timeout /t 10 > nul
goto restart

:restart
echo Restarting HRM server...
node "concurrent_server.js" --port %PORT%
echo Server crashed. Restarting in 10 seconds...
timeout /t 10 > nul
goto restart

:end
pause