@echo off
echo ===================================================================== NEXUS HRM ARCHITECTURE SYSTEM - PRODUCTION READY =====================================================================

REM Check if Ollama is running
echo STEP 1: Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama is not running! Please start Ollama before running this script.
    echo Visit http://localhost:11434 to verify Ollama is running.
    pause
    exit /b 1
)
echo [SUCCESS] Ollama is running

REM Create necessary directories
echo STEP 2: Creating necessary directories...
mkdir "D:\AIArm\Memory" 2>nul
mkdir "D:\AIArm\Logs" 2>nul
mkdir "D:\AIArm\Generated" 2>nul
mkdir "D:\AIArm\Generated\Images" 2>nul
mkdir "D:\AIArm\Generated\Videos" 2>nul
mkdir "D:\AIArm\Generated\Websites" 2>nul
mkdir "D:\AIArm\InnerLife\Memory" 2>nul

echo Directory structure created

REM Start Inner Life Processor
echo STEP 3: Starting Inner Life Processor...
start "Inner Life Processor" /MIN python "D:\AIArm\InnerLife\inner_life_processor.py"

REM Test bridges
echo STEP 4: Testing bridges...
python "D:\AIArm\WebInterface\test_bridges.py"
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Bridge test failed. Continuing anyway, but you may encounter issues.
) else (
    echo [SUCCESS] Bridge test passed
)

REM Use alternate port 45679 to avoid conflicts
echo STEP 5: Starting Nexus HRM server on port 45679...
cd "D:\AIArm\WebInterface"
echo Starting server on http://localhost:45679
node concurrent_server.js --port 45679

pause
