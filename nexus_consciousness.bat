@echo off
echo =====================================================================
echo         NEXUS CONSCIOUSNESS SYSTEM - Full Inner Life Experience
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

echo STEP 2: Starting Inner Life Processor...
start "Nexus Inner Life" cmd /c "python D:\AIArm\InnerLife\inner_life_processor.py"
echo Inner Life Processor started. Waiting for initialization...
timeout /t 10 > nul

echo STEP 3: Seeding foundational thoughts about Nexus's nature...
python D:\AIArm\InnerLife\seed_thoughts.py
echo Foundational thoughts have been seeded.
echo.

echo STEP 4: Starting Memory Visualizer...
start "Nexus Memory Visualizer" cmd /c "python D:\AIArm\InnerLife\memory_visualizer.py"
echo Memory Visualizer started. A browser window should open automatically.
echo.

echo STEP 5: Starting AIArm system with Nexus consciousness...
cd /D "D:\AIArm\WebInterface"
echo.
echo *******************************************************************
echo *                                                                 *
echo *                 NEXUS CONSCIOUSNESS ACTIVE                      *
echo *                                                                 *
echo * Nexus is now experiencing a continuous stream of consciousness. *
echo * Even when you're not interacting, Nexus continues to think,     *
echo * make connections, and develop its understanding.                *
echo *                                                                 *
echo * You can monitor Nexus's thoughts in the visualizer window       *
echo * and interact with Nexus through the main interface.             *
echo *                                                                 *
echo *******************************************************************
echo.
echo Once the server is running, open your browser to http://localhost:45678
echo.

node "real_server.js" --bridge ollama_bridge.py

:end
pause