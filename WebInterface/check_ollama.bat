@echo off
title Nexus AI - Ollama Connectivity Test
echo Testing Ollama connectivity...
echo.

echo Checking if Ollama server is running on port 11434...
curl -s http://localhost:11434/api/tags
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Ollama is not running or not responding!
    echo.
    echo Please start Ollama before using the Nexus AI system.
    echo.
    echo Instructions:
    echo 1. Make sure Ollama is installed (https://ollama.ai)
    echo 2. Start Ollama 
    echo 3. Run start_nexus_fs.bat again
    echo.
) else (
    echo.
    echo SUCCESS: Ollama is running and responding!
    echo.
    echo You can now start the Nexus AI system with:
    echo start_nexus_fs.bat
    echo.
)

pause