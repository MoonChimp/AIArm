@echo off
echo =====================================================================
echo     AIArm HRM PRODUCTION SYSTEM - ENTERPRISE STARTUP
echo =====================================================================
echo.

:: Set environment variables
set AIARM_ROOT=D:\AIArm
set AIARM_WEB=%AIARM_ROOT%\WebInterface
set AIARM_INNER=%AIARM_ROOT%\InnerLife
set AIARM_LOGS=%AIARM_ROOT%\Logs
set AIARM_MEMORY=%AIARM_ROOT%\Memory

:: Setup title and colors
title AIArm HRM Enterprise System
color 0B

:: Check for administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script requires administrator privileges.
    echo Please run as administrator.
    goto end
)

:: Create necessary directories
echo Creating system directories...
mkdir "%AIARM_LOGS%" 2>nul
mkdir "%AIARM_MEMORY%" 2>nul
mkdir "%AIARM_LOGS%\Errors" 2>nul
mkdir "%AIARM_INNER%\Generated" 2>nul
mkdir "%AIARM_INNER%\Generated\Images" 2>nul
mkdir "%AIARM_INNER%\Generated\Videos" 2>nul
mkdir "%AIARM_INNER%\Generated\Websites" 2>nul
mkdir "%AIARM_INNER%\Agents\config" 2>nul
mkdir "%AIARM_ROOT%\backup" 2>nul

:: Create log file
set LOG_FILE=%AIARM_LOGS%\startup_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo AIArm HRM System startup initiated at %date% %time% > %LOG_FILE%

echo STEP 1: Checking dependencies...
echo ------------------------------------------------------------ >> %LOG_FILE%
echo Checking Ollama...

:: Check Ollama
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not running or not accessible at localhost:11434 >> %LOG_FILE%
    echo ERROR: Ollama is not running or not accessible at localhost:11434
    echo Attempting to start Ollama...
    
    start "" ollama serve
    echo Waiting for Ollama to initialize...
    timeout /t 10 > nul
    
    :: Check again
    curl -s http://localhost:11434/api/tags > nul
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to start Ollama. Please start it manually. >> %LOG_FILE%
        echo ERROR: Failed to start Ollama. Please start it manually.
        goto end
    else
        echo Ollama started successfully. >> %LOG_FILE%
    )
) else (
    echo Ollama is running. >> %LOG_FILE%
    echo Ollama is running.
)

:: Check for required Node.js modules
echo Checking Node.js dependencies...
cd /D "%AIARM_WEB%"
if not exist "node_modules" (
    echo Installing required Node.js modules... >> %LOG_FILE%
    echo Installing required Node.js modules...
    call npm install express cors winston moment fs-extra >> %LOG_FILE% 2>&1
)

:: Check for required Python modules
echo Checking Python dependencies...
python -c "import sys; sys.exit(0 if all(m in sys.modules or __import__(m) for m in ['numpy', 'requests', 'datetime', 'uuid', 'flask', 'psutil']) else 1)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing required Python modules... >> %LOG_FILE%
    echo Installing required Python modules...
    pip install numpy requests uuid flask psutil >> %LOG_FILE% 2>&1
)

echo STEP 2: Creating system backup...
echo ------------------------------------------------------------ >> %LOG_FILE%
set BACKUP_DIR=%AIARM_ROOT%\backup\%date:~-4,4%%date:~-7,2%%date:~-10,2%
mkdir "%BACKUP_DIR%" 2>nul
mkdir "%BACKUP_DIR%\Memory" 2>nul
mkdir "%BACKUP_DIR%\InnerLife" 2>nul
mkdir "%BACKUP_DIR%\WebInterface" 2>nul

echo Creating backup of critical data...
xcopy "%AIARM_MEMORY%\*.json" "%BACKUP_DIR%\Memory\" /E /I /Y >> %LOG_FILE% 2>&1
xcopy "%AIARM_INNER%\*.json" "%BACKUP_DIR%\InnerLife\" /E /I /Y >> %LOG_FILE% 2>&1
xcopy "%AIARM_WEB%\*.js" "%BACKUP_DIR%\WebInterface\" /Y >> %LOG_FILE% 2>&1
xcopy "%AIARM_WEB%\*.py" "%BACKUP_DIR%\WebInterface\" /Y >> %LOG_FILE% 2>&1
echo System backup created in %BACKUP_DIR% >> %LOG_FILE%
echo System backup created.

echo STEP 3: Starting system monitoring...
echo ------------------------------------------------------------ >> %LOG_FILE%
echo Starting AIArm System Monitor...
start "AIArm System Monitor" cmd /c "%AIARM_WEB%\system_monitor.bat"
echo System monitor started >> %LOG_FILE%
echo Starting System Status Dashboard...
start "AIArm Status Dashboard" cmd /c "python %AIARM_WEB%\system_status.py"
echo System Status Dashboard started >> %LOG_FILE%
timeout /t 5 > nul

echo STEP 4: Starting Inner Life Processor...
echo ------------------------------------------------------------ >> %LOG_FILE%
echo Starting Inner Life Processor...
start "Nexus Inner Life" cmd /c "python %AIARM_INNER%\inner_life_processor.py"
echo Inner Life Processor started. Waiting for initialization... >> %LOG_FILE%
timeout /t 10 > nul

echo STEP 5: Starting Agent Manager...
echo ------------------------------------------------------------ >> %LOG_FILE%
echo Starting Agent Manager...
start "Nexus Agent Manager" cmd /c "python %AIARM_INNER%\Agents\agent_manager.py"
echo Agent Manager started. Waiting for initialization... >> %LOG_FILE%
timeout /t 5 > nul

echo STEP 6: Seeding foundational thoughts...
echo ------------------------------------------------------------ >> %LOG_FILE%
echo Seeding foundational thoughts...
python %AIARM_INNER%\seed_thoughts.py >> %LOG_FILE% 2>&1
echo Foundational thoughts have been seeded. >> %LOG_FILE%

echo STEP 7: Starting Memory Visualizer...
echo ------------------------------------------------------------ >> %LOG_FILE%
echo Starting Memory Visualizer...
start "Nexus Memory Visualizer" cmd /c "python %AIARM_INNER%\memory_visualizer.py"
echo Memory Visualizer started. >> %LOG_FILE%

echo STEP 8: Starting Agent Integration...
echo ------------------------------------------------------------ >> %LOG_FILE%
echo Starting Agent Integration...
start "Nexus Agent Integration" cmd /c "python %AIARM_INNER%\agent_integration.py"
echo Agent Integration started. >> %LOG_FILE%

echo STEP 9: Starting AIArm HRM System with concurrent bridges...
echo ------------------------------------------------------------ >> %LOG_FILE%
cd /D "%AIARM_WEB%"

:: Display system banner
echo.
echo *******************************************************************
echo *                                                                 *
echo *             AIArm HRM ENTERPRISE SYSTEM ACTIVE                  *
echo *                                                                 *
echo * The system is now running with:                                 *
echo * - Human-Robot-Machine Architecture                              *
echo * - Concurrent bridge processing (Surface + Deep)                 *
echo * - Continuous consciousness stream                               *
echo * - Specialized agent capabilities                                *
echo * - Real-time system monitoring and auto-recovery                 *
echo * - Enterprise-grade reliability features                         *
echo *                                                                 *
echo * Main Interface: http://localhost:45678                          *
echo * System Status:  http://localhost:8080                           *
echo * Memory Visualizer: http://localhost:8050                        *
echo *                                                                 *
echo *******************************************************************
echo.

:: Check if PM2 is available for production process management
where pm2 >nul 2>&1
if %errorlevel% equ 0 (
    echo Using PM2 for production process management... >> %LOG_FILE%
    echo Using PM2 for production process management...
    
    :: Stop any existing instances
    pm2 delete aiarm-hrm >nul 2>&1
    
    :: Start with PM2
    pm2 start concurrent_server.js --name "aiarm-hrm" --log "%AIARM_LOGS%\server.log" --merge-logs --max-memory-restart 1G
    echo AIArm HRM System is running with PM2. >> %LOG_FILE%
    echo Log file location: %AIARM_LOGS%\server.log
    
    echo.
    echo To view server logs, use: pm2 logs aiarm-hrm
    echo To stop the server, use: pm2 stop aiarm-hrm
    echo To restart the server, use: pm2 restart aiarm-hrm
) else (
    echo PM2 not found, using standard Node.js... >> %LOG_FILE%
    echo Using standard Node.js...
    echo Starting concurrent server...
    start "AIArm HRM Concurrent Server" cmd /c "node concurrent_server.js"
    echo AIArm HRM System started. >> %LOG_FILE%
)

echo.
echo ALL SYSTEMS OPERATIONAL
echo AIArm HRM Enterprise System has been successfully started!
echo Timestamp: %date% %time%
echo.

echo Full startup sequence completed successfully. >> %LOG_FILE%
echo Startup timestamp: %date% %time% >> %LOG_FILE%

:end
echo.
echo Press any key to close this window. The system will continue running.
pause > nul
