@echo off
setlocal EnableDelayedExpansion

echo =====================================================================
echo         NEXUS HRM SYSTEM - PRODUCTION MODE ACTIVATION
echo =====================================================================
echo.

REM Set environment variables
set "NODE_ENV=production"
set "SERVER_PORT=45678"
set "MAX_RESTART_ATTEMPTS=5"
set "RESTART_COUNT=0"
set "SYSTEM_ROOT=D:\AIArm"

REM Create important directories
mkdir "%SYSTEM_ROOT%\Logs" 2>nul
mkdir "%SYSTEM_ROOT%\Logs\Errors" 2>nul
mkdir "%SYSTEM_ROOT%\Logs\Performance" 2>nul
mkdir "%SYSTEM_ROOT%\Logs\System" 2>nul

echo STEP 1: Checking system requirements...

REM Check for Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js before running this system.
    goto end
)

REM Check for Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python before running this system.
    goto end
)

REM Check for Ollama
echo STEP 2: Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not running or not accessible at localhost:11434
    echo Starting Ollama service...
    start "" ollama serve
    timeout /t 10 > nul
    
    REM Check again after attempting to start
    curl -s http://localhost:11434/api/tags > nul
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to start Ollama. Please start Ollama manually.
        goto end
    ) else {
        echo Successfully started Ollama service.
    }
) else (
    echo Ollama service is running.
)

echo Available Ollama models:
ollama list
echo.

echo STEP 3: Setting up system directories...
mkdir "%SYSTEM_ROOT%\InnerLife\Generated" 2>nul
mkdir "%SYSTEM_ROOT%\InnerLife\Generated\Images" 2>nul
mkdir "%SYSTEM_ROOT%\InnerLife\Generated\Videos" 2>nul
mkdir "%SYSTEM_ROOT%\InnerLife\Generated\Websites" 2>nul
mkdir "%SYSTEM_ROOT%\InnerLife\Agents\config" 2>nul
echo Directory structure verified.
echo.

echo STEP 4: Starting Monitoring Service...
start "Nexus System Monitor" cmd /c "wmic cpu get loadpercentage,name /value > %SYSTEM_ROOT%\Logs\Performance\cpu_monitor.log & wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value >> %SYSTEM_ROOT%\Logs\Performance\memory_monitor.log"
echo System monitoring started.
echo.

echo STEP 5: Starting Inner Life Processor...
start "Nexus Inner Life" /MIN cmd /c "python %SYSTEM_ROOT%\InnerLife\inner_life_processor.py > %SYSTEM_ROOT%\Logs\System\inner_life.log 2>&1"
echo Inner Life Processor started. Waiting for initialization...
timeout /t 10 > nul

echo STEP 6: Starting Agent Manager...
start "Nexus Agent Manager" /MIN cmd /c "python %SYSTEM_ROOT%\InnerLife\Agents\agent_manager.py > %SYSTEM_ROOT%\Logs\System\agent_manager.log 2>&1"
echo Agent Manager started. Waiting for initialization...
timeout /t 5 > nul

echo STEP 7: Seeding foundational thoughts...
python %SYSTEM_ROOT%\InnerLife\seed_thoughts.py > %SYSTEM_ROOT%\Logs\System\seed_thoughts.log 2>&1
echo Foundational thoughts have been seeded.
echo.

echo STEP 8: Starting Memory Visualizer...
start "Nexus Memory Visualizer" /MIN cmd /c "python %SYSTEM_ROOT%\InnerLife\memory_visualizer.py > %SYSTEM_ROOT%\Logs\System\memory_visualizer.log 2>&1"
echo Memory Visualizer started.
echo.

echo STEP 9: Starting Agent Integration...
start "Nexus Agent Integration" /MIN cmd /c "python %SYSTEM_ROOT%\InnerLife\agent_integration.py > %SYSTEM_ROOT%\Logs\System\agent_integration.log 2>&1"
echo Agent Integration started.
echo.

echo STEP 10: Starting AIArm system with HRM architecture...
cd /D "%SYSTEM_ROOT%\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *                  NEXUS HRM ARCHITECTURE                         *
echo *                                                                 *
echo *                   PRODUCTION DEPLOYMENT                         *
echo *                                                                 *
echo * Nexus is now operating with BOTH bridge layers:                 *
echo * - SURFACE: Improved interface through the orchestrator          *
echo * - DEEP: Continuous reasoning through Ollama                     *
echo *                                                                 *
echo * This Human-Robot-Machine architecture provides both improved    *
echo * surface interactions and deep thought capabilities.             *
echo *                                                                 *
echo * System will automatically restart on failure (up to 5 times)    *
echo * All logs are being written to the Logs directory                *
echo *                                                                 *
echo * Monitor server status: http://localhost:%SERVER_PORT%/status    *
echo *                                                                 *
echo *******************************************************************
echo.

REM Start the server with auto-restart capability
:server_start
echo Starting HRM Server (Attempt %RESTART_COUNT% of %MAX_RESTART_ATTEMPTS%)...
node "%SYSTEM_ROOT%\WebInterface\concurrent_server.js" > "%SYSTEM_ROOT%\Logs\System\server_%date:~-4,4%%date:~-7,2%%date:~-10,2%.log" 2>&1
set EXIT_CODE=%ERRORLEVEL%

if %EXIT_CODE% NEQ 0 (
    echo Server exited with code %EXIT_CODE% at %time%
    set /a RESTART_COUNT+=1
    
    if %RESTART_COUNT% LSS %MAX_RESTART_ATTEMPTS% (
        echo Waiting 10 seconds before restarting...
        timeout /t 10 > nul
        goto server_start
    ) else (
        echo Maximum restart attempts reached. Please check the logs.
        echo Server will not be restarted automatically.
    )
)

echo.
echo Server has stopped. Check logs for details.
echo To restart manually, run this script again.

:end
pause