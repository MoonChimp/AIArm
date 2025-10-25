@echo off
echo ===================================================================== 
echo NEXUS AI: STABLE DIFFUSION WEBUI INTEGRATION
echo ===================================================================== 

REM Check if StableDiffusionWebUI is available
echo Checking for StableDiffusionWebUI...
set WEBUI_PORT=7860
curl -s http://localhost:%WEBUI_PORT%/sdapi/v1/sd-models > nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] StableDiffusionWebUI not detected on port %WEBUI_PORT%
    echo.
    echo If your WebUI is running on a different port, please enter it below.
    echo Press Enter to use the default port (7860) if WebUI is not currently running.
    echo.
    set /p CUSTOM_PORT="Enter WebUI port (default: 7860): "
    
    if not "%CUSTOM_PORT%"=="" (
        set WEBUI_PORT=%CUSTOM_PORT%
    )
    
    echo.
    echo Will use port %WEBUI_PORT% for WebUI connection.
    echo Make sure to start StableDiffusionWebUI with the --api flag:
    echo.
    echo   webui-user.bat --api
    echo.
) else (
    echo [SUCCESS] StableDiffusionWebUI detected on port %WEBUI_PORT%
    
    curl -s http://localhost:%WEBUI_PORT%/sdapi/v1/sd-models > sd_models.tmp
    for /f %%A in ('type sd_models.tmp ^| find /c "title"') do set MODEL_COUNT=%%A
    del sd_models.tmp
    
    echo Found %MODEL_COUNT% models available!
)

REM Update the nexus_direct.html to include WebUI integration
echo Updating interface to integrate with StableDiffusionWebUI...
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace '</head>', '<script>localStorage.setItem(\"sd_webui_port\", \"%WEBUI_PORT%\");</script></head>' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

REM Add the WebUI integration script to the page
powershell -Command "$content = Get-Content D:\AIArm\WebInterface\nexus_direct.html -Raw; $webui_js = Get-Content D:\AIArm\WebInterface\webui_integration.js -Raw; $updated = $content -replace 'window.addEventListener\(''load'', \(\) => \{', 'window.addEventListener(''load'', () => { checkWebUIAvailability().then(hasWebUI => { if(hasWebUI) { statusText.textContent += '' + StableDiffusionWebUI detected!''; }}); '; Set-Content D:\AIArm\WebInterface\nexus_direct.html -Value $updated"

REM Merge the WebUI processUserInput function
powershell -Command "$content = Get-Content D:\AIArm\WebInterface\nexus_direct.html -Raw; $webui_js = Get-Content D:\AIArm\WebInterface\webui_integration.js -Raw; $process_input = ($webui_js -split 'async function processUserInput\(\)')[1] -split '\}'; $content = $content -replace 'async function processUserInput\(\)[^}]*\}', $process_input[0] + '}'; Set-Content D:\AIArm\WebInterface\nexus_direct.html -Value $content"

REM Add WebUI integration functions
echo Adding WebUI integration functions to the interface...
powershell -Command "$content = Get-Content D:\AIArm\WebInterface\nexus_direct.html -Raw; $webui_js = Get-Content D:\AIArm\WebInterface\webui_integration.js -Raw; $webui_functions = ($webui_js -split 'async function checkWebUIAvailability\(\)')[0]; $content = $content -replace '// Initialize(.|\n)*</script>', $webui_functions + '// Initialize$1</script>'; Set-Content D:\AIArm\WebInterface\nexus_direct.html -Value $content"

REM Restart the server with WebUI integration
echo Stopping any running servers...
taskkill /f /im python.exe 2>nul

echo Starting NexusAI with StableDiffusionWebUI integration...
cd D:\AIArm\WebInterface
start "NexusAI:EPAA" python nexus_direct_server.py

echo ===================================================================== 
echo NEXUS AI: WEBUI INTEGRATION COMPLETE
echo ===================================================================== 
echo.
echo Your NexusAI is now connected to StableDiffusionWebUI!
echo.
echo IMPORTANT: Make sure to start StableDiffusionWebUI with the --api flag:
echo   webui-user.bat --api
echo.
echo Try asking for images like:
echo - "Generate an image of a mountain landscape at sunset"
echo - "Create a photorealistic portrait of a cyberpunk character"
echo - "Show me an image of a futuristic space station"
echo.
echo The system will use your full StableDiffusionWebUI installation with:
echo - All your installed models and checkpoints
echo - Your custom embeddings and LoRAs
echo - Better quality than the basic Ollama implementation
echo.
echo The server has been restarted and your browser should open automatically.
echo If not, visit: http://localhost:8000/nexus_direct.html
echo.
echo Press any key to exit this window...
pause > nul
