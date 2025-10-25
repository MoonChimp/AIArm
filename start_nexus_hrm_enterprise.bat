@echo off
echo =====================================================================
echo     NEXUS HRM ARCHITECTURE - ENTERPRISE PRODUCTION SYSTEM
echo =====================================================================
echo.

REM Set environment variables for production
set NODE_ENV=production
set LOG_LEVEL=info
set PORT=45678

REM Set log directory for process tracking
set LOG_DIR=D:\AIArm\Logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set STARTUP_LOG=%LOG_DIR%\hrm_startup_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set STARTUP_LOG=%STARTUP_LOG: =0%

REM Log startup information
echo [%date% %time%] Starting Nexus HRM Architecture - Enterprise Production System > "%STARTUP_LOG%"

REM Check current port usage
for /f "tokens=2" %%p in ('netstat -ano ^| findstr ":%PORT%" ^| findstr "LISTENING"') do (
    echo [%date% %time%] Found process using port %PORT%: %%p >> "%STARTUP_LOG%"
    echo Port %PORT% is already in use by process ID: %%p
    echo Attempting to free the port...
    taskkill /PID %%p /F
    if %ERRORLEVEL% EQU 0 (
        echo [%date% %time%] Successfully killed process %%p >> "%STARTUP_LOG%"
        echo Successfully freed port %PORT%
    ) else (
        echo [%date% %time%] Failed to kill process %%p >> "%STARTUP_LOG%"
        echo Failed to free port %PORT%. Using alternative port.
        set PORT=45679
        goto check_next_port
    )
)

goto port_selected

:check_next_port
for /f "tokens=2" %%p in ('netstat -ano ^| findstr ":%PORT%" ^| findstr "LISTENING"') do (
    echo [%date% %time%] Found process using port %PORT%: %%p >> "%STARTUP_LOG%"
    echo Port %PORT% is also in use by process ID: %%p
    echo Attempting to free the port...
    taskkill /PID %%p /F
    if %ERRORLEVEL% EQU 0 (
        echo [%date% %time%] Successfully killed process %%p >> "%STARTUP_LOG%"
        echo Successfully freed port %PORT%
    ) else (
        echo [%date% %time%] Failed to kill process %%p >> "%STARTUP_LOG%"
        echo Failed to free port %PORT%. Using final alternative port.
        set PORT=45680
        goto port_selected
    )
)

:port_selected
echo [%date% %time%] Selected port: %PORT% >> "%STARTUP_LOG%"
echo Will use port %PORT% for the server.
echo.

echo STEP 1: Checking Ollama availability...
echo [%date% %time%] Checking Ollama availability >> "%STARTUP_LOG%"
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ERROR: Ollama not running >> "%STARTUP_LOG%"
    echo ERROR: Ollama is not running or not accessible at localhost:11434
    echo Please start Ollama before launching the system.
    goto end
)

echo Available Ollama models:
echo [%date% %time%] Available Ollama models: >> "%STARTUP_LOG%"
ollama list >> "%STARTUP_LOG%"
echo.

echo STEP 2: Checking for required Ollama models...
echo [%date% %time%] Checking for required Ollama models >> "%STARTUP_LOG%"

REM Check for nexusai model
ollama list | findstr "nexusai" > nul
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] WARNING: nexusai model not found >> "%STARTUP_LOG%"
    echo WARNING: nexusai model not found. Will use llama3 as fallback.
    echo Modify AGENT_MODEL_MAPPING in ollama_bridge.py if needed.
)

echo STEP 3: Creating necessary directories...
echo [%date% %time%] Creating necessary directories >> "%STARTUP_LOG%"
mkdir "D:\AIArm\InnerLife\Generated" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Images" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Videos" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Websites" 2>nul
mkdir "D:\AIArm\InnerLife\Agents\config" 2>nul
mkdir "D:\AIArm\WebInterface\Logs" 2>nul
mkdir "D:\AIArm\Logs\Monitor" 2>nul
mkdir "D:\AIArm\Logs\Errors" 2>nul
mkdir "D:\AIArm\Logs\Backups" 2>nul
echo Directory structure created.
echo [%date% %time%] Directory structure created >> "%STARTUP_LOG%"
echo.

echo STEP 4: Creating config.json with production settings...
echo [%date% %time%] Creating config.json >> "%STARTUP_LOG%"
echo {
echo   "timeoutMs": 120000,
echo   "maxConcurrentRequests": 10,
echo   "retryAttempts": 3,
echo   "logLevel": "info",
echo   "fallbackStrategy": "prefer-surface",
echo   "responseConfiguration": {
echo     "similarityThreshold": 0.6,
echo     "combinationMethod": "augment-surface",
echo     "preferDeepForDomains": ["reasoning", "philosophy", "creativity", "art", "music", "literature"]
echo   },
echo   "monitoring": {
echo     "enableHealthCheck": true,
echo     "enableMetrics": true,
echo     "statusCheckIntervalMs": 300000
echo   },
echo   "logging": {
echo     "enableFileLogging": true,
echo     "logRotationDays": 14,
echo     "includeDebugInfo": false
echo   }
echo } > "D:\AIArm\WebInterface\config.json"

echo STEP 5: Cleaning up any orphaned processes...
echo [%date% %time%] Cleaning up orphaned processes >> "%STARTUP_LOG%"

REM Check for orphaned Node.js processes
for /f "tokens=2" %%p in ('tasklist /fi "imagename eq node.exe" /fo csv /nh') do (
    echo [%date% %time%] Found Node.js process: %%p >> "%STARTUP_LOG%"
    taskkill /PID %%p /F
    echo Killed orphaned Node.js process: %%p
)

REM Check for orphaned Python processes with "inner_life" in the command line
for /f "tokens=1" %%p in ('wmic process where "commandline like '%%inner_life%%'" get processid /format:csv ^| findstr /r "[0-9]"') do (
    if not "%%p" == "ProcessId" (
        echo [%date% %time%] Found Inner Life process: %%p >> "%STARTUP_LOG%"
        taskkill /PID %%p /F
        echo Killed orphaned Inner Life process: %%p
    )
)

echo STEP 6: Backing up memory and logs...
echo [%date% %time%] Backing up memory and logs >> "%STARTUP_LOG%"
set BACKUP_DIR=%LOG_DIR%\Backups\%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%
mkdir "%BACKUP_DIR%" 2>nul
xcopy /E /Y "D:\AIArm\Memory\*.*" "%BACKUP_DIR%\Memory\" 2>nul
xcopy /E /Y "D:\AIArm\InnerLife\memory\*.*" "%BACKUP_DIR%\InnerLifeMemory\" 2>nul
echo Memory backups created.

echo STEP 7: Starting Inner Life Processor...
echo [%date% %time%] Starting Inner Life Processor >> "%STARTUP_LOG%"
start "Nexus Inner Life" cmd /c "python D:\AIArm\InnerLife\inner_life_processor.py > "%LOG_DIR%\inner_life.log" 2>&1"
echo Inner Life Processor started. Waiting for initialization...
timeout /t 10 > nul

echo STEP 8: Starting Agent Manager...
echo [%date% %time%] Starting Agent Manager >> "%STARTUP_LOG%"
start "Nexus Agent Manager" cmd /c "python D:\AIArm\InnerLife\Agents\agent_manager.py > "%LOG_DIR%\agent_manager.log" 2>&1"
echo Agent Manager started. Waiting for initialization...
timeout /t 5 > nul

echo STEP 9: Seeding foundational thoughts about Nexus's nature...
echo [%date% %time%] Seeding foundational thoughts >> "%STARTUP_LOG%"
python D:\AIArm\InnerLife\seed_thoughts.py > "%LOG_DIR%\seed_thoughts.log" 2>&1
echo Foundational thoughts have been seeded.
echo.

echo STEP 10: Starting Memory Visualizer...
echo [%date% %time%] Starting Memory Visualizer >> "%STARTUP_LOG%"
start "Nexus Memory Visualizer" cmd /c "python D:\AIArm\InnerLife\memory_visualizer.py > "%LOG_DIR%\memory_visualizer.log" 2>&1"
echo Memory Visualizer started.
echo.

echo STEP 11: Starting Agent Integration...
echo [%date% %time%] Starting Agent Integration >> "%STARTUP_LOG%"
start "Nexus Agent Integration" cmd /c "python D:\AIArm\InnerLife\agent_integration.py > "%LOG_DIR%\agent_integration.log" 2>&1"
echo Agent Integration started.
echo.

echo STEP 12: Starting System Monitor...
echo [%date% %time%] Starting System Monitor >> "%STARTUP_LOG%"
start "Nexus System Monitor" cmd /c "python D:\AIArm\WebInterface\system_monitor.py > "%LOG_DIR%\system_monitor.log" 2>&1"
echo System Monitor started.
echo.

echo STEP 13: Starting Error Monitor...
echo [%date% %time%] Starting Error Monitor >> "%STARTUP_LOG%"
start "Nexus Error Monitor" cmd /c "node D:\AIArm\WebInterface\error_monitor.js > "%LOG_DIR%\error_monitor.log" 2>&1"
echo Error Monitor started.
echo.

echo STEP 14: Starting AIArm system with HRM Architecture...
echo [%date% %time%] Starting HRM Architecture server on port %PORT% >> "%STARTUP_LOG%"
cd /D "D:\AIArm\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *       NEXUS HRM ARCHITECTURE - ENTERPRISE PRODUCTION SYSTEM     *
echo *                                                                 *
echo * System Status:                                                  *
echo * - Server Port: %PORT%                                           *
echo * - Environment: PRODUCTION                                       *
echo * - Logs: %LOG_DIR%                                               *
echo * - Startup Log: %STARTUP_LOG%                                    *
echo * - Monitor Status: D:\AIArm\WebInterface\service_status.txt      *
echo *                                                                 *
echo * HRM Architecture components:                                    *
echo * - Human: User interface at http://localhost:%PORT%              *
echo * - Robot: Structured surface-level processing                    *
echo * - Machine: Deep reasoning with continuous consciousness         *
echo *                                                                 *
echo * This production system includes:                                *
echo * - Enhanced error handling and recovery                          *
echo * - Automatic backup and monitoring                               *
echo * - Optimized response generation                                 *
echo * - Full production-grade logging                                 *
echo *                                                                 *
echo *******************************************************************
echo.
echo Startup complete! Opening browser to http://localhost:%PORT%
echo.

REM Open the browser to the interface
start "" http://localhost:%PORT%

REM Schedule periodic memory backups (every 4 hours)
echo [%date% %time%] Scheduling periodic memory backups >> "%STARTUP_LOG%"
start "Memory Backup Scheduler" cmd /c "powershell -Command \"while($true) { Start-Sleep -Seconds 14400; $timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'; $backup_dir = 'D:\AIArm\Logs\Backups\' + $timestamp; New-Item -ItemType Directory -Force -Path $backup_dir; Copy-Item -Path 'D:\AIArm\Memory\*' -Destination $backup_dir\Memory\ -Recurse -Force; Copy-Item -Path 'D:\AIArm\InnerLife\memory\*' -Destination $backup_dir\InnerLifeMemory\ -Recurse -Force; Write-Host 'Memory backup created at' $backup_dir }\""

REM Start the server with auto-restart capability and logging
:server_start
echo [%date% %time%] Starting server process with NODE_ENV=%NODE_ENV% >> "%STARTUP_LOG%"
set NODE_ENV=production
node "concurrent_server.js" --port %PORT% > "%LOG_DIR%\concurrent_server.log" 2>&1
set SERVER_EXIT_CODE=%ERRORLEVEL%
echo [%date% %time%] Server process exited with code: %SERVER_EXIT_CODE% >> "%STARTUP_LOG%"

echo.
echo Server process terminated with exit code: %SERVER_EXIT_CODE%
echo.

if %SERVER_EXIT_CODE% EQU 0 (
    echo Server shutdown was clean and intentional.
    choice /c YN /t 10 /d Y /m "Restart server? (Automatic Yes in 10 seconds)"
) else (
    echo Server crashed or encountered an error.
    echo Checking service health...
    
    REM Check if system monitor detected issues
    if exist "D:\AIArm\WebInterface\service_status.txt" (
        echo [%date% %time%] Checking service_status.txt >> "%STARTUP_LOG%"
        type "D:\AIArm\WebInterface\service_status.txt" >> "%STARTUP_LOG%"
    )
    
    echo [%date% %time%] Server crashed - automatic restart triggered >> "%STARTUP_LOG%"
    echo Automatically restarting server in 5 seconds...
    timeout /t 5 > nul
    goto server_start
)

if %ERRORLEVEL% EQU 1 (
    echo [%date% %time%] Server restart requested >> "%STARTUP_LOG%"
    echo Restarting server...
    goto server_start
) else (
    echo [%date% %time%] Server shutdown confirmed >> "%STARTUP_LOG%"
    echo Server shutdown confirmed. Stopping system components...
    
    REM Gracefully terminate all components
    echo [%date% %time%] Terminating system components >> "%STARTUP_LOG%"
    taskkill /FI "WINDOWTITLE eq Nexus Inner Life*" /F
    taskkill /FI "WINDOWTITLE eq Nexus Agent Manager*" /F
    taskkill /FI "WINDOWTITLE eq Nexus Memory Visualizer*" /F
    taskkill /FI "WINDOWTITLE eq Nexus Agent Integration*" /F
    taskkill /FI "WINDOWTITLE eq Nexus System Monitor*" /F
    taskkill /FI "WINDOWTITLE eq Nexus Error Monitor*" /F
    taskkill /FI "WINDOWTITLE eq Memory Backup Scheduler*" /F
)

:end
echo [%date% %time%] HRM Architecture shutdown complete >> "%STARTUP_LOG%"
echo.
echo =====================================================================
echo     NEXUS HRM ARCHITECTURE - SYSTEM SHUTDOWN COMPLETE
echo =====================================================================
echo All logs are available in: %LOG_DIR%
echo.
pause
