@echo off
echo Testing NexusAI Agent System...
echo.

cd /d D:\AIArm\nexusai-assistant\nexus_enhanced_capabilities

echo [STEP 1] Building Agent Models...
echo.
call build-nexus-agents.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to build agent models
    pause
    exit /b 1
)

echo.
echo [STEP 2] Testing Main Agent...
echo Question: "Create a simple Python script that prints hello world"
ollama run nexusai-agent-enhanced "Create a simple Python script that prints hello world and explain what you're doing"
if %errorlevel% neq 0 (
    echo WARNING: Main agent test failed
)

echo.
echo [STEP 3] Testing Visual Agent...  
echo Question: "Describe how to create a logo design"
ollama run nexusai-visual-agent "Describe the process of creating a professional logo design using AI tools like Stable Diffusion"
if %errorlevel% neq 0 (
    echo WARNING: Visual agent test failed
)

echo.
echo [STEP 4] Testing Music Agent...
echo Question: "Compose a simple melody structure"
ollama run nexusai-music-agent "Compose a simple chord progression for a pop song and explain the music theory behind it"
if %errorlevel% neq 0 (
    echo WARNING: Music agent test failed
)

echo.
echo [STEP 5] Starting NexusAI Application...
echo.
cd /d D:\AIArm\nexusai-assistant
start "" npm start

echo.
echo ========================================
echo NexusAI Agent System Test Complete!
echo ========================================
echo.
echo Available models:
echo - nexusai-agent-enhanced (main agent)
echo - nexusai-visual-agent (visual/art creation)  
echo - nexusai-music-agent (music composition)
echo.
echo NexusAI application should be starting...
echo Test conversation loading and saving features.
echo.
echo To use agents in terminal:
echo   ollama run nexusai-agent-enhanced
echo   ollama run nexusai-visual-agent  
echo   ollama run nexusai-music-agent
echo.

pause
