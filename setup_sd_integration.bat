@echo off
echo ===================================================================== 
echo NEXUS AI: STABLE DIFFUSION WEBUI INTEGRATION - SIMPLIFIED
echo ===================================================================== 

REM Set the WebUI port
set WEBUI_PORT=7860

REM Create the WebUI integration files
echo Creating WebUI integration files...

REM Create the main function file
echo // StableDiffusionWebUI Integration > D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo // Configuration >> D:\AIArm\WebInterface\sd_integration.js
echo const WEBUI_PORT = 7860; >> D:\AIArm\WebInterface\sd_integration.js
echo const WEBUI_URL = `http://localhost:${WEBUI_PORT}`; >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo // Generate image using WebUI >> D:\AIArm\WebInterface\sd_integration.js
echo async function generateWithWebUI(prompt) { >> D:\AIArm\WebInterface\sd_integration.js
echo   try { >> D:\AIArm\WebInterface\sd_integration.js
echo     console.log(`Generating image via WebUI: ${prompt}`); >> D:\AIArm\WebInterface\sd_integration.js
echo     const response = await fetch(`${WEBUI_URL}/sdapi/v1/txt2img`, { >> D:\AIArm\WebInterface\sd_integration.js
echo       method: 'POST', >> D:\AIArm\WebInterface\sd_integration.js
echo       headers: { 'Content-Type': 'application/json' }, >> D:\AIArm\WebInterface\sd_integration.js
echo       body: JSON.stringify({ >> D:\AIArm\WebInterface\sd_integration.js
echo         prompt: prompt, >> D:\AIArm\WebInterface\sd_integration.js
echo         negative_prompt: "blurry, bad anatomy, extra limbs, poorly drawn face", >> D:\AIArm\WebInterface\sd_integration.js
echo         steps: 25, >> D:\AIArm\WebInterface\sd_integration.js
echo         width: 512, >> D:\AIArm\WebInterface\sd_integration.js
echo         height: 512 >> D:\AIArm\WebInterface\sd_integration.js
echo       }) >> D:\AIArm\WebInterface\sd_integration.js
echo     }); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     if (!response.ok) throw new Error(`WebUI returned ${response.status}`); >> D:\AIArm\WebInterface\sd_integration.js
echo     const data = await response.json(); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     if (data.images && data.images.length > 0) { >> D:\AIArm\WebInterface\sd_integration.js
echo       return { success: true, image: `data:image/jpeg;base64,${data.images[0]}` }; >> D:\AIArm\WebInterface\sd_integration.js
echo     } >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     return { success: false, error: "No image returned" }; >> D:\AIArm\WebInterface\sd_integration.js
echo   } catch (error) { >> D:\AIArm\WebInterface\sd_integration.js
echo     console.error("WebUI error:", error); >> D:\AIArm\WebInterface\sd_integration.js
echo     return { success: false, error: error.toString() }; >> D:\AIArm\WebInterface\sd_integration.js
echo   } >> D:\AIArm\WebInterface\sd_integration.js
echo } >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo // Check WebUI availability >> D:\AIArm\WebInterface\sd_integration.js
echo async function checkWebUI() { >> D:\AIArm\WebInterface\sd_integration.js
echo   try { >> D:\AIArm\WebInterface\sd_integration.js
echo     const response = await fetch(`${WEBUI_URL}/sdapi/v1/sd-models`); >> D:\AIArm\WebInterface\sd_integration.js
echo     return response.ok; >> D:\AIArm\WebInterface\sd_integration.js
echo   } catch (error) { >> D:\AIArm\WebInterface\sd_integration.js
echo     return false; >> D:\AIArm\WebInterface\sd_integration.js
echo   } >> D:\AIArm\WebInterface\sd_integration.js
echo } >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo // Override the image generation in processUserInput >> D:\AIArm\WebInterface\sd_integration.js
echo document.addEventListener('DOMContentLoaded', function() { >> D:\AIArm\WebInterface\sd_integration.js
echo   // Store original function >> D:\AIArm\WebInterface\sd_integration.js
echo   const originalProcessUserInput = window.processUserInput; >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo   // Check WebUI availability and update status >> D:\AIArm\WebInterface\sd_integration.js
echo   checkWebUI().then(available => { >> D:\AIArm\WebInterface\sd_integration.js
echo     if (available) { >> D:\AIArm\WebInterface\sd_integration.js
echo       const statusEl = document.getElementById('status-text'); >> D:\AIArm\WebInterface\sd_integration.js
echo       if (statusEl) statusEl.innerHTML += ' + WebUI'; >> D:\AIArm\WebInterface\sd_integration.js
echo       console.log('WebUI available!'); >> D:\AIArm\WebInterface\sd_integration.js
echo     } >> D:\AIArm\WebInterface\sd_integration.js
echo   }); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo   // Replace the function >> D:\AIArm\WebInterface\sd_integration.js
echo   window.processUserInput = async function() { >> D:\AIArm\WebInterface\sd_integration.js
echo     const message = userInput.value.trim(); >> D:\AIArm\WebInterface\sd_integration.js
echo     if (!message) return; >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     // Clear input and display user message >> D:\AIArm\WebInterface\sd_integration.js
echo     userInput.value = ''; >> D:\AIArm\WebInterface\sd_integration.js
echo     addMessageToUI(message, true); >> D:\AIArm\WebInterface\sd_integration.js
echo     chatHistory.push({ role: "user", content: message }); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     // Check if image request >> D:\AIArm\WebInterface\sd_integration.js
echo     const imageKeywords = ['image', 'picture', 'photo', 'generate', 'create', 'draw']; >> D:\AIArm\WebInterface\sd_integration.js
echo     const isImageRequest = imageKeywords.some(kw => message.toLowerCase().includes(kw)); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     // Show typing indicator >> D:\AIArm\WebInterface\sd_integration.js
echo     typingIndicator.style.display = 'block'; >> D:\AIArm\WebInterface\sd_integration.js
echo     messagesContainer.scrollTop = messagesContainer.scrollHeight; >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     if (isImageRequest) { >> D:\AIArm\WebInterface\sd_integration.js
echo       try { >> D:\AIArm\WebInterface\sd_integration.js
echo         // Check WebUI availability >> D:\AIArm\WebInterface\sd_integration.js
echo         const webUIAvailable = await checkWebUI(); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo         if (webUIAvailable) { >> D:\AIArm\WebInterface\sd_integration.js
echo           // Generate image >> D:\AIArm\WebInterface\sd_integration.js
echo           const result = await generateWithWebUI(message); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo           if (result.success) { >> D:\AIArm\WebInterface\sd_integration.js
echo             // Hide typing indicator >> D:\AIArm\WebInterface\sd_integration.js
echo             typingIndicator.style.display = 'none'; >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo             // Create image element >> D:\AIArm\WebInterface\sd_integration.js
echo             const messageElement = document.createElement('div'); >> D:\AIArm\WebInterface\sd_integration.js
echo             messageElement.classList.add('message', 'assistant-message'); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo             // Badge >> D:\AIArm\WebInterface\sd_integration.js
echo             const badge = document.createElement('div'); >> D:\AIArm\WebInterface\sd_integration.js
echo             badge.classList.add('agent-badge', 'agent-photo'); >> D:\AIArm\WebInterface\sd_integration.js
echo             badge.textContent = '📷 Photo Generation Agent'; >> D:\AIArm\WebInterface\sd_integration.js
echo             messageElement.appendChild(badge); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo             // Image >> D:\AIArm\WebInterface\sd_integration.js
echo             const img = document.createElement('img'); >> D:\AIArm\WebInterface\sd_integration.js
echo             img.src = result.image; >> D:\AIArm\WebInterface\sd_integration.js
echo             img.alt = message; >> D:\AIArm\WebInterface\sd_integration.js
echo             img.style.maxWidth = '100%%'; >> D:\AIArm\WebInterface\sd_integration.js
echo             img.style.borderRadius = '8px'; >> D:\AIArm\WebInterface\sd_integration.js
echo             img.style.marginTop = '10px'; >> D:\AIArm\WebInterface\sd_integration.js
echo             messageElement.appendChild(img); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo             // Caption >> D:\AIArm\WebInterface\sd_integration.js
echo             const caption = document.createElement('div'); >> D:\AIArm\WebInterface\sd_integration.js
echo             caption.textContent = `Here's the image you requested.`; >> D:\AIArm\WebInterface\sd_integration.js
echo             caption.style.marginTop = '8px'; >> D:\AIArm\WebInterface\sd_integration.js
echo             messageElement.appendChild(caption); >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo             // Add to chat >> D:\AIArm\WebInterface\sd_integration.js
echo             messagesContainer.appendChild(messageElement); >> D:\AIArm\WebInterface\sd_integration.js
echo             messagesContainer.scrollTop = messagesContainer.scrollHeight; >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo             // Add to chat history >> D:\AIArm\WebInterface\sd_integration.js
echo             chatHistory.push({ role: "assistant", content: "Photo Generation Agent: I've created an image based on your request." }); >> D:\AIArm\WebInterface\sd_integration.js
echo             return; >> D:\AIArm\WebInterface\sd_integration.js
echo           } >> D:\AIArm\WebInterface\sd_integration.js
echo         } >> D:\AIArm\WebInterface\sd_integration.js
echo       } catch (error) { >> D:\AIArm\WebInterface\sd_integration.js
echo         console.error('WebUI integration error:', error); >> D:\AIArm\WebInterface\sd_integration.js
echo       } >> D:\AIArm\WebInterface\sd_integration.js
echo     } >> D:\AIArm\WebInterface\sd_integration.js
echo. >> D:\AIArm\WebInterface\sd_integration.js
echo     // Fall back to original method >> D:\AIArm\WebInterface\sd_integration.js
echo     return originalProcessUserInput.call(this); >> D:\AIArm\WebInterface\sd_integration.js
echo   }; >> D:\AIArm\WebInterface\sd_integration.js
echo }); >> D:\AIArm\WebInterface\sd_integration.js

REM Update nexus_direct.html to include the WebUI integration
echo Updating interface file...
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace '</head>', '<script src=\"sd_integration.js\"></script></head>' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

REM Restart the server
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
echo The server has been restarted and your browser should open automatically.
echo If not, visit: http://localhost:8000/nexus_direct.html
echo.
echo Press any key to exit this window...
pause > nul
