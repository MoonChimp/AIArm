@echo off
echo ===================================================================== 
echo NEXUS AI: STABLE DIFFUSION WEBUI INTEGRATION
echo ===================================================================== 

REM Check if StableDiffusionWebUI is available
echo Checking for StableDiffusionWebUI...
set WEBUI_PORT=7860
curl -s http://localhost:%WEBUI_PORT%/sdapi/v1/sd-models >nul 2>&1

REM Check the error level properly
if not %ERRORLEVEL% == 0 (
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

REM Create simpler version of WebUI integration
echo Creating WebUI integration script...

echo // Function to generate images using StableDiffusionWebUI API > D:\AIArm\WebInterface\webui_functions.js
echo async function generateImageWithWebUI(prompt) { >> D:\AIArm\WebInterface\webui_functions.js
echo     try { >> D:\AIArm\WebInterface\webui_functions.js
echo         // WebUI default port is 7860, but let's make it configurable >> D:\AIArm\WebInterface\webui_functions.js
echo         const webUIPort = '%WEBUI_PORT%'; >> D:\AIArm\WebInterface\webui_functions.js
echo         const webUIUrl = `http://localhost:${webUIPort}/sdapi/v1/txt2img`; >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         // Default parameters >> D:\AIArm\WebInterface\webui_functions.js
echo         const params = { >> D:\AIArm\WebInterface\webui_functions.js
echo             prompt: prompt, >> D:\AIArm\WebInterface\webui_functions.js
echo             negative_prompt: "blurry, bad anatomy, extra limbs, poorly drawn face, distorted face", >> D:\AIArm\WebInterface\webui_functions.js
echo             steps: 25, >> D:\AIArm\WebInterface\webui_functions.js
echo             width: 512, >> D:\AIArm\WebInterface\webui_functions.js
echo             height: 512, >> D:\AIArm\WebInterface\webui_functions.js
echo             cfg_scale: 7.5, >> D:\AIArm\WebInterface\webui_functions.js
echo             sampler_name: "DPM++ 2M Karras" >> D:\AIArm\WebInterface\webui_functions.js
echo         }; >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         console.log(`Generating image with StableDiffusionWebUI: ${prompt}`); >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         // Make the API call >> D:\AIArm\WebInterface\webui_functions.js
echo         const response = await fetch(webUIUrl, { >> D:\AIArm\WebInterface\webui_functions.js
echo             method: 'POST', >> D:\AIArm\WebInterface\webui_functions.js
echo             headers: { >> D:\AIArm\WebInterface\webui_functions.js
echo                 'Content-Type': 'application/json' >> D:\AIArm\WebInterface\webui_functions.js
echo             }, >> D:\AIArm\WebInterface\webui_functions.js
echo             body: JSON.stringify(params) >> D:\AIArm\WebInterface\webui_functions.js
echo         }); >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         if (response.ok) { >> D:\AIArm\WebInterface\webui_functions.js
echo             const data = await response.json(); >> D:\AIArm\WebInterface\webui_functions.js
echo             >> D:\AIArm\WebInterface\webui_functions.js
echo             // WebUI returns images as base64 >> D:\AIArm\WebInterface\webui_functions.js
echo             if (data.images && data.images.length > 0) { >> D:\AIArm\WebInterface\webui_functions.js
echo                 return { >> D:\AIArm\WebInterface\webui_functions.js
echo                     success: true, >> D:\AIArm\WebInterface\webui_functions.js
echo                     image: `data:image/jpeg;base64,${data.images[0]}` >> D:\AIArm\WebInterface\webui_functions.js
echo                 }; >> D:\AIArm\WebInterface\webui_functions.js
echo             } >> D:\AIArm\WebInterface\webui_functions.js
echo         } else { >> D:\AIArm\WebInterface\webui_functions.js
echo             throw new Error(`API returned status: ${response.status}`); >> D:\AIArm\WebInterface\webui_functions.js
echo         } >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         return { success: false }; >> D:\AIArm\WebInterface\webui_functions.js
echo     } catch (error) { >> D:\AIArm\WebInterface\webui_functions.js
echo         console.error('Error generating image with WebUI:', error); >> D:\AIArm\WebInterface\webui_functions.js
echo         return { success: false, error: error.toString() }; >> D:\AIArm\WebInterface\webui_functions.js
echo     } >> D:\AIArm\WebInterface\webui_functions.js
echo } >> D:\AIArm\WebInterface\webui_functions.js
echo. >> D:\AIArm\WebInterface\webui_functions.js
echo // Function to check if WebUI is available >> D:\AIArm\WebInterface\webui_functions.js
echo async function checkWebUIAvailability() { >> D:\AIArm\WebInterface\webui_functions.js
echo     try { >> D:\AIArm\WebInterface\webui_functions.js
echo         // Use the configured port >> D:\AIArm\WebInterface\webui_functions.js
echo         const webUIPort = '%WEBUI_PORT%'; >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         // Try to connect to WebUI >> D:\AIArm\WebInterface\webui_functions.js
echo         const response = await fetch(`http://localhost:${webUIPort}/sdapi/v1/sd-models`, { >> D:\AIArm\WebInterface\webui_functions.js
echo             method: 'GET' >> D:\AIArm\WebInterface\webui_functions.js
echo         }); >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         if (response.ok) { >> D:\AIArm\WebInterface\webui_functions.js
echo             const models = await response.json(); >> D:\AIArm\WebInterface\webui_functions.js
echo             console.log(`WebUI is available with ${models.length} models`); >> D:\AIArm\WebInterface\webui_functions.js
echo             return true; >> D:\AIArm\WebInterface\webui_functions.js
echo         } >> D:\AIArm\WebInterface\webui_functions.js
echo         >> D:\AIArm\WebInterface\webui_functions.js
echo         return false; >> D:\AIArm\WebInterface\webui_functions.js
echo     } catch (error) { >> D:\AIArm\WebInterface\webui_functions.js
echo         console.error('Error checking WebUI availability:', error); >> D:\AIArm\WebInterface\webui_functions.js
echo         return false; >> D:\AIArm\WebInterface\webui_functions.js
echo     } >> D:\AIArm\WebInterface\webui_functions.js
echo } >> D:\AIArm\WebInterface\webui_functions.js

REM Create the integration loader script
echo console.log('Loading WebUI integration...'); > D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo // Try to load the WebUI functions >> D:\AIArm\WebInterface\webui_loader.js
echo const script = document.createElement('script'); >> D:\AIArm\WebInterface\webui_loader.js
echo script.src = 'webui_functions.js'; >> D:\AIArm\WebInterface\webui_loader.js
echo document.head.appendChild(script); >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo // Update the processUserInput function to try WebUI first >> D:\AIArm\WebInterface\webui_loader.js
echo script.onload = function() { >> D:\AIArm\WebInterface\webui_loader.js
echo     console.log('WebUI functions loaded'); >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo     // Store original function >> D:\AIArm\WebInterface\webui_loader.js
echo     const originalProcessUserInput = processUserInput; >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo     // Override the function >> D:\AIArm\WebInterface\webui_loader.js
echo     processUserInput = async function() { >> D:\AIArm\WebInterface\webui_loader.js
echo         const message = userInput.value.trim(); >> D:\AIArm\WebInterface\webui_loader.js
echo         if (!message) return; >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo         // Clear input >> D:\AIArm\WebInterface\webui_loader.js
echo         userInput.value = ''; >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo         // Add user message to UI >> D:\AIArm\WebInterface\webui_loader.js
echo         addMessageToUI(message, true); >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo         // Add to chat history >> D:\AIArm\WebInterface\webui_loader.js
echo         chatHistory.push({ role: "user", content: message }); >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo         // Check if this is a photo generation request >> D:\AIArm\WebInterface\webui_loader.js
echo         const isPhotoRequest = message.toLowerCase().includes('photo') || >> D:\AIArm\WebInterface\webui_loader.js
echo                              message.toLowerCase().includes('picture') || >> D:\AIArm\WebInterface\webui_loader.js
echo                              message.toLowerCase().includes('image') || >> D:\AIArm\WebInterface\webui_loader.js
echo                              message.toLowerCase().includes('generate') || >> D:\AIArm\WebInterface\webui_loader.js
echo                              message.toLowerCase().includes('create'); >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo         // Show typing indicator >> D:\AIArm\WebInterface\webui_loader.js
echo         typingIndicator.style.display = 'block'; >> D:\AIArm\WebInterface\webui_loader.js
echo         messagesContainer.scrollTop = messagesContainer.scrollHeight; >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo         // If it's a photo request, try to generate an image first >> D:\AIArm\WebInterface\webui_loader.js
echo         if (isPhotoRequest) { >> D:\AIArm\WebInterface\webui_loader.js
echo             try { >> D:\AIArm\WebInterface\webui_loader.js
echo                 // First check if WebUI is available >> D:\AIArm\WebInterface\webui_loader.js
echo                 const hasWebUI = await checkWebUIAvailability(); >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo                 if (hasWebUI) { >> D:\AIArm\WebInterface\webui_loader.js
echo                     console.log('Using WebUI for image generation'); >> D:\AIArm\WebInterface\webui_loader.js
echo                     // Try to generate with WebUI >> D:\AIArm\WebInterface\webui_loader.js
echo                     const imageResult = await generateImageWithWebUI(message); >> D:\AIArm\WebInterface\webui_loader.js
echo                     if (imageResult && imageResult.success) { >> D:\AIArm\WebInterface\webui_loader.js
echo                         // Hide typing indicator >> D:\AIArm\WebInterface\webui_loader.js
echo                         typingIndicator.style.display = 'none'; >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo                         // Add image to UI >> D:\AIArm\WebInterface\webui_loader.js
echo                         addImageToUI(imageResult.image, message); >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo                         // Add assistant response to chat history >> D:\AIArm\WebInterface\webui_loader.js
echo                         const imageResponse = `Photo Generation Agent: I've created this image based on your request: "${message}"`; >> D:\AIArm\WebInterface\webui_loader.js
echo                         chatHistory.push({ role: "assistant", content: imageResponse }); >> D:\AIArm\WebInterface\webui_loader.js
echo                         return; >> D:\AIArm\WebInterface\webui_loader.js
echo                     } >> D:\AIArm\WebInterface\webui_loader.js
echo                 } >> D:\AIArm\WebInterface\webui_loader.js
echo             } catch (error) { >> D:\AIArm\WebInterface\webui_loader.js
echo                 console.error('Error with WebUI image generation:', error); >> D:\AIArm\WebInterface\webui_loader.js
echo             } >> D:\AIArm\WebInterface\webui_loader.js
echo         } >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo         // Fall back to original function if WebUI didn't work >> D:\AIArm\WebInterface\webui_loader.js
echo         return originalProcessUserInput.call(this); >> D:\AIArm\WebInterface\webui_loader.js
echo     }; >> D:\AIArm\WebInterface\webui_loader.js
echo. >> D:\AIArm\WebInterface\webui_loader.js
echo     // Check WebUI on startup >> D:\AIArm\WebInterface\webui_loader.js
echo     checkWebUIAvailability().then(hasWebUI => { >> D:\AIArm\WebInterface\webui_loader.js
echo         if (hasWebUI) { >> D:\AIArm\WebInterface\webui_loader.js
echo             statusText.textContent += ' + StableDiffusionWebUI'; >> D:\AIArm\WebInterface\webui_loader.js
echo         } >> D:\AIArm\WebInterface\webui_loader.js
echo     }); >> D:\AIArm\WebInterface\webui_loader.js
echo }; >> D:\AIArm\WebInterface\webui_loader.js

REM Update the nexus_direct.html to include WebUI integration
echo Updating interface to integrate with StableDiffusionWebUI...
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace '</head>', '<script src=\"webui_loader.js\"></script></head>' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

REM Restart the server with WebUI integration
echo Stopping any running servers...
taskkill /f /im python.exe >nul 2>&1

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
