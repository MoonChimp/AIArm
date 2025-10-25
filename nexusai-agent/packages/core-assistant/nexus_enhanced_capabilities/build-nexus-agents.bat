@echo off
echo Building NexusAI Agent Models...
echo.

cd /d D:\AIArm\nexusai-assistant\nexus_enhanced_capabilities

echo [1/3] Building NexusAI Enhanced Agent...
ollama create nexusai-agent-enhanced -f nexusai-agent-enhanced.modelfile
if %errorlevel% neq 0 (
    echo ERROR: Failed to build nexusai-agent-enhanced
    pause
    exit /b 1
)

echo [2/3] Building NexusAI Visual Agent...
ollama create nexusai-visual-agent -f nexusai-visual-agent.modelfile
if %errorlevel% neq 0 (
    echo ERROR: Failed to build nexusai-visual-agent
    pause
    exit /b 1
)

echo [3/3] Building NexusAI Music Agent...
ollama create nexusai-music-agent -f nexusai-music-agent.modelfile
if %errorlevel% neq 0 (
    echo ERROR: Failed to build nexusai-music-agent
    pause
    exit /b 1
)

echo.
echo SUCCESS: All NexusAI Agent models built successfully!
echo.
echo Available models:
echo - nexusai-agent-enhanced (main agent with execution capabilities)
echo - nexusai-visual-agent (Stable Diffusion + visual AI integration)
echo - nexusai-music-agent (Music composition and audio processing)
echo.
echo To test: ollama run nexusai-agent-enhanced
echo.

pause
