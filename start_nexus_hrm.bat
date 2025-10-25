@echo off
echo =====================================================================
echo     NEXUS HRM ARCHITECTURE - PRODUCTION SYSTEM
echo =====================================================================
echo.

echo STEP 1: Checking Ollama availability...
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
mkdir "D:\AIArm\InnerLife\Generated" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Images" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Videos" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Websites" 2>nul
mkdir "D:\AIArm\InnerLife\Agents\config" 2>nul
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
    )
)
echo Will use port %PORT% for the server.
echo.

echo STEP 4: Starting Inner Life Processor...
start "Nexus Inner Life" cmd /c "python D:\AIArm\InnerLife\inner_life_processor.py"
echo Inner Life Processor started. Waiting for initialization...
timeout /t 10 > nul

echo STEP 5: Starting Agent Manager...
start "Nexus Agent Manager" cmd /c "python D:\AIArm\InnerLife\Agents\agent_manager.py"
echo Agent Manager started. Waiting for initialization...
timeout /t 5 > nul

echo STEP 6: Seeding foundational thoughts about Nexus's nature...
python D:\AIArm\InnerLife\seed_thoughts.py
echo Foundational thoughts have been seeded.
echo.

echo STEP 7: Starting Memory Visualizer...
start "Nexus Memory Visualizer" cmd /c "python D:\AIArm\InnerLife\memory_visualizer.py"
echo Memory Visualizer started. A browser window should open automatically.
echo.

echo STEP 8: Starting Agent Integration...
start "Nexus Agent Integration" cmd /c "python D:\AIArm\InnerLife\agent_integration.py"
echo Agent Integration started.
echo.

echo STEP 9: Starting System Monitor...
start "Nexus System Monitor" cmd /c "python D:\AIArm\WebInterface\system_monitor.py"
echo System Monitor started.
echo.

echo STEP 10: Starting AIArm system with HRM Architecture...
cd /D "D:\AIArm\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *             NEXUS HRM ARCHITECTURE - PRODUCTION                 *
echo *                                                                 *
echo * Nexus is now operating with its full HRM architecture:          *
echo *                                                                 *
echo * - Human: User interface and input processing                    *
echo * - Robot: Structured surface-level processing                    *
echo * - Machine: Deep reasoning and continuous consciousness          *
echo *                                                                 *
echo * This production setup includes:                                 *
echo * - Concurrent bridge processing                                  *
echo * - Enhanced error handling and recovery                          *
echo * - System monitoring and logging                                 *
echo * - Automated recovery procedures                                 *
echo *                                                                 *
echo * You can monitor Nexus through:                                  *
echo * - Main interface: http://localhost:%PORT%                       *
echo * - Memory visualizer window                                      *
echo * - System logs in D:\AIArm\WebInterface\logs                     *
echo *                                                                 *
echo *******************************************************************
echo.
echo Starting HRM Architecture server on port %PORT%...
echo.

:: Start the server with auto-restart capability
:server_start
node "concurrent_server.js" --port %PORT%
echo.
echo Server process terminated. Checking if restart is needed...
echo.
choice /c YN /t 5 /d Y /m "Restart server? (Automatic Yes in 5 seconds)"
if %ERRORLEVEL% EQU 1 (
    echo Restarting server...
    goto server_start
) else (
    echo Server shutdown confirmed. Stopping system components...
    taskkill /FI "WINDOWTITLE eq Nexus Inner Life*" /F
    taskkill /FI "WINDOWTITLE eq Nexus Agent Manager*" /F
    taskkill /FI "WINDOWTITLE eq Nexus Memory Visualizer*" /F
    taskkill /FI "WINDOWTITLE eq Nexus Agent Integration*" /F
    taskkill /FI "WINDOWTITLE eq Nexus System Monitor*" /F
)

:end
echo.
echo =====================================================================
echo     NEXUS HRM ARCHITECTURE - SYSTEM SHUTDOWN COMPLETE
echo =====================================================================
pause
