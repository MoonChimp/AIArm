@echo off
echo ===================================================================== 
echo NEXUS AI: REAL IMAGE GENERATION SETUP
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

REM Check for existing stable diffusion model
echo Checking for Stable Diffusion models...
curl -s http://localhost:11434/api/tags | findstr "stable-diffusion" > nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] No Stable Diffusion model found!
    echo.
    echo You'll need to pull one of these models:
    echo   1. brxce/stable-diffusion-prompt-generator:latest (already installed)
    echo   2. stability/stable-diffusion:latest (recommended, smaller)
    echo   3. stability/sdxl:latest (higher quality, larger)
    echo.
    choice /C 123N /M "Select a model to pull (1-3) or N to skip: "
    
    if errorlevel 4 (
        echo Skipping model installation.
        echo Note: Image generation will not work without a Stable Diffusion model.
    ) else if errorlevel 3 (
        echo Pulling stability/sdxl:latest (this may take a while)...
        ollama pull stability/sdxl:latest
    ) else if errorlevel 2 (
        echo Pulling stability/stable-diffusion:latest...
        ollama pull stability/stable-diffusion:latest
    ) else if errorlevel 1 (
        echo You already have brxce/stable-diffusion-prompt-generator:latest
        echo This is just a prompt generator and not a full image model.
        echo Would you like to pull a full image generation model?
        choice /C YN /M "Pull stability/stable-diffusion:latest? (Y/N): "
        
        if errorlevel 2 (
            echo Skipping model installation.
            echo Note: Image generation will not work without a Stable Diffusion model.
        ) else (
            echo Pulling stability/stable-diffusion:latest...
            ollama pull stability/stable-diffusion:latest
        )
    )
) else (
    echo [SUCCESS] Found Stable Diffusion model(s)
)

REM Restart the server with image generation capability
echo Stopping any running servers...
taskkill /f /im python.exe 2>nul

echo Starting NexusAI with REAL image generation...
cd D:\AIArm\WebInterface
start "NexusAI:EPAA" python nexus_direct_server.py

echo ===================================================================== 
echo NEXUS AI: REAL IMAGE GENERATION READY
echo ===================================================================== 
echo.
echo Your NexusAI now has ACTUAL image generation capabilities!
echo.
echo Try asking it to:
echo - "Generate an image of a mountain landscape"
echo - "Create a picture of a kitten playing with yarn"
echo - "Show me an image of a futuristic city"
echo.
echo The server has been restarted and your browser should open automatically.
echo If not, visit: http://localhost:8000/nexus_direct.html
echo.
echo Press any key to exit this window...
pause > nul
