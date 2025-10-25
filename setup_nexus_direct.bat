@echo off
echo ===================================================================== 
echo NEXUS AI DIRECT - SETUP
echo ===================================================================== 

REM Check if Ollama is running
echo Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama is not running! Please start Ollama before running this script.
    echo Visit http://localhost:11434 to verify Ollama is running.
    pause
    exit /b 1
)
echo [SUCCESS] Ollama is running

REM Create the enhanced Nexus AI model
echo Creating enhanced Nexus AI model...
cd D:\AIArm
ollama create nexusai-enhanced:latest -f Modelfile

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create the enhanced model.
    pause
    exit /b 1
)
echo [SUCCESS] Created nexusai-enhanced:latest model

REM Start a simple HTTP server to serve the interface
echo Starting simple HTTP server...
echo The interface will be available at http://localhost:8000/nexus_direct.html

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Python not found. Please install Python or use your own web server.
    echo You can open the file directly in your browser: D:\AIArm\WebInterface\nexus_direct.html
    explorer "D:\AIArm\WebInterface\nexus_direct.html"
) else (
    cd D:\AIArm\WebInterface
    start "Nexus AI Direct Server" python -m http.server 8000
    timeout /t 2 >nul
    start http://localhost:8000/nexus_direct.html
)

echo ===================================================================== 
echo NEXUS AI DIRECT - SETUP COMPLETE
echo ===================================================================== 
echo.
echo You can now use the direct interface to interact with your enhanced Nexus AI model.
echo All capabilities are built into the model itself - no more bridge errors!
echo.
echo If the browser didn't open automatically, visit:
echo http://localhost:8000/nexus_direct.html
echo.
echo Press any key to exit...
pause > nul
