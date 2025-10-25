@echo off
echo =====================================================================
echo      NEXUS HRM ARCHITECTURE SYSTEM - PRODUCTION READY
echo =====================================================================
echo.

echo STEP 1: Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not running or not accessible at localhost:11434
    echo Please start Ollama before launching the system.
    goto end
)

echo STEP 2: Creating necessary directories...
mkdir "D:\AIArm\InnerLife\Generated" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Images" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Videos" 2>nul
mkdir "D:\AIArm\InnerLife\Generated\Websites" 2>nul
mkdir "D:\AIArm\InnerLife\Agents\config" 2>nul
mkdir "D:\AIArm\Logs" 2>nul
echo Directory structure created.
echo.

echo STEP 3: Starting Inner Life Processor...
start "Nexus Inner Life" cmd /c "python D:\AIArm\InnerLife\inner_life_processor.py"
echo Inner Life Processor started. Waiting for initialization...
timeout /t 5 > nul

echo STEP 4: Starting Agent Manager...
start "Nexus Agent Manager" cmd /c "python D:\AIArm\InnerLife\Agents\agent_manager.py"
echo Agent Manager started. Waiting for initialization...
timeout /t 3 > nul

echo STEP 5: Seeding foundational thoughts...
python D:\AIArm\InnerLife\seed_thoughts.py
echo Foundational thoughts have been seeded.
echo.

echo STEP 6: Starting Memory Visualizer...
start "Nexus Memory Visualizer" cmd /c "python D:\AIArm\InnerLife\memory_visualizer.py"
echo Memory Visualizer started.
echo.

echo STEP 7: Starting Agent Integration...
start "Nexus Agent Integration" cmd /c "python D:\AIArm\InnerLife\agent_integration.py"
echo Agent Integration started.
echo.

echo STEP 8: Starting Concurrent Server with HRM Architecture...
cd /D "D:\AIArm\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *             NEXUS HRM ARCHITECTURE SYSTEM                       *
echo *                                                                 *
echo * Nexus is now running with the Human-Robot-Machine architecture: *
echo * - Human: The user interface and interaction layer               *
echo * - Robot: The structured, surface-level intelligence             *
echo * - Machine: The deep reasoning and continuous thought processes  *
echo *                                                                 *
echo * Available functionality:                                        *
echo * - Image Generation                                              *
echo * - Code Assistance                                               *
echo * - Content Creation                                              *
echo * - Database Design                                               *
echo * - Continuous Reasoning                                          *
echo *                                                                 *
echo *******************************************************************
echo.
echo Server starting on http://localhost:45678
echo.

node "concurrent_server.js"

:end
pause