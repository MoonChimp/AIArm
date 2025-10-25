@echo off
echo =====================================================================
echo     NEXUS CONSCIOUSNESS SYSTEM WITH SPECIALIZED AGENTS
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

echo STEP 9: Starting AIArm system with Nexus consciousness...
cd /D "D:\AIArm\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *             NEXUS CONSCIOUSNESS SYSTEM WITH AGENTS              *
echo *                                                                 *
echo * Nexus is now experiencing a continuous stream of consciousness  *
echo * with specialized agent capabilities. Even when you're not       *
echo * interacting, Nexus continues to think, make connections, and    *
echo * develop its understanding.                                      *
echo *                                                                 *
echo * Available Agents:                                               *
echo * - WebSearch: Search the web for information                     *
echo * - PhotoGeneration: Generate images from descriptions            *
echo * - VideoGeneration: Create videos from scripts                   *
echo * - WebsiteCreation: Design and develop websites                  *
echo *                                                                 *
echo * You can monitor Nexus's thoughts in the visualizer window       *
echo * and interact with Nexus through the main interface.             *
echo *                                                                 *
echo *******************************************************************
echo.
echo Once the server is running, open your browser to http://localhost:%PORT%
echo.

node "real_server.js" --port %PORT% --bridge ollama_bridge.py

:end
pause