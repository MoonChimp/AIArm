@echo off
echo.
echo === Fixing AIArm and StableDiffusion Integration ===
echo.

REM Kill existing node processes
echo Stopping existing node processes...
taskkill /F /IM node.exe /T 2>nul
if %ERRORLEVEL% EQU 0 (
  echo ✓ Successfully terminated existing server
) else (
  echo ✓ No existing server found
)

REM Small delay to ensure ports are released
timeout /t 2 /nobreak >nul

REM Check if StableDiffusion WebUI is running
echo Checking if StableDiffusion WebUI is running...
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:7860/sdapi/v1/sd-models' -Method 'GET'; Write-Host '✓ StableDiffusion WebUI is running on port 7860' } catch { Write-Host '✗ StableDiffusion WebUI is NOT running on port 7860'; exit 1 }"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Please start StableDiffusion WebUI with API enabled using the find_sd_webui.bat script
  echo and then run this script again.
  echo.
  echo Press any key to exit...
  pause >nul
  exit /b
)

REM Create a simple static file directory if it doesn't exist
echo Ensuring static directory exists...
if not exist "D:\AIArm\WebInterface\static" (
  mkdir "D:\AIArm\WebInterface\static"
  echo ✓ Created static directory
) else (
  echo ✓ Static directory exists
)

if not exist "D:\AIArm\WebInterface\static\images" (
  mkdir "D:\AIArm\WebInterface\static\images"
  echo ✓ Created static/images directory
) else (
  echo ✓ Static/images directory exists
)

if not exist "D:\AIArm\Images" (
  mkdir "D:\AIArm\Images"
  echo ✓ Created Images directory
) else (
  echo ✓ Images directory exists
)

REM Create a minimal server that just uses the StableDiffusion bridge
echo Creating minimal server for testing...

echo // Minimal server for StableDiffusion testing > "D:\AIArm\WebInterface\minimal_sd_server.js"
echo const express = require('express'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo const path = require('path'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo const cors = require('cors'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo const { spawn } = require('child_process'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo const fs = require('fs'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo // Create Express app >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo const app = express(); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.use(cors()); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.use(express.json()); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.use(express.static(path.join(__dirname))); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.use('/static', express.static(path.join(__dirname, 'static'))); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo // Simple logging function >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo function logMessage(message, level = 'INFO') { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   const timestamp = new Date().toISOString(); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   console.log(`[${timestamp}] [${level}] ${message}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   // Also log to file >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   const logDir = path.join(__dirname, 'Logs'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   if (!fs.existsSync(logDir)) { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     fs.mkdirSync(logDir); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   } >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   const logFile = path.join(logDir, `sd_minimal_server.log`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   fs.appendFileSync(logFile, `[${timestamp}] [${level}] ${message}\n`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo } >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo // API Routes >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.get('/api/status', (req, res) => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   logMessage('Status endpoint called'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   res.json({ >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     status: 'online', >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     system: 'AIArm Minimal SD Server', >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     timestamp: new Date().toISOString() >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.post('/api/photo-generation', (req, res) => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   const { prompt, options, userId } = req.body; >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   logMessage(`Photo Generation endpoint called with prompt: ${prompt}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   if (!prompt) { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     return res.status(400).json({ error: 'Image prompt is required' }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   } >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   try { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     // Use sd_bridge.py directly for image generation >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     const sdBridgePath = path.join(__dirname, 'sd_bridge.py'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     // Prepare input as JSON >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     const inputJson = JSON.stringify({ >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       input: prompt, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       options: options || {} >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     logMessage(`Running Python bridge: ${sdBridgePath}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     logMessage(`Input: ${inputJson}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     // Spawn Python process with UTF-8 encoding >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     const pythonProcess = spawn('python', [ >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       sdBridgePath, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       '--input', inputJson, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       '--json' >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     ], { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       env: { ...process.env, PYTHONIOENCODING: 'utf-8' } >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     let outputData = ''; >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     let errorData = ''; >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     // Collect standard output >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     pythonProcess.stdout.on('data', (data) => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       const dataStr = data.toString(); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       outputData += dataStr; >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       logMessage(`Python output: ${dataStr}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     // Collect error output >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     pythonProcess.stderr.on('data', (data) => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       const dataStr = data.toString(); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       errorData += dataStr; >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       logMessage(`Python error: ${dataStr}`, 'ERROR'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     // Handle process completion >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     pythonProcess.on('close', (code) => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       logMessage(`Python process exited with code ${code}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       if (code !== 0) { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         logMessage(`Python error: ${errorData}`, 'ERROR'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         return res.status(500).json({ >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo           error: 'Failed to process photo generation request', >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo           message: errorData, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo           success: false >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       } >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       try { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         // Parse the JSON response >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         logMessage(`Raw output: ${outputData}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         const result = JSON.parse(outputData); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         logMessage(`Parsed result: ${JSON.stringify(result)}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         res.json(result); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       } catch (jsonError) { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         logMessage(`Failed to parse JSON response: ${jsonError}`, 'ERROR'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         res.status(500).json({ >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo           error: 'Failed to parse photo generation response', >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo           message: jsonError.message, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo           raw: outputData, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo           success: false >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       } >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     // Handle process error >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     pythonProcess.on('error', (error) => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       logMessage(`Process error: ${error}`, 'ERROR'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       res.status(500).json({ >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         error: 'Failed to start photo generation process', >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         message: error.message, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo         success: false >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   } catch (error) { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     logMessage(`Server error: ${error}`, 'ERROR'); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     res.status(500).json({ >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       error: 'Failed to process photo generation request', >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       message: error.message, >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo       success: false >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo     }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   } >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo // Serve the HTML interfaces >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.get('/', (req, res) => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   res.sendFile(path.join(__dirname, 'index.html')); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo. >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo // Start the server >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo const PORT = 45678; >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo app.listen(PORT, () => { >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   logMessage(`Minimal SD Server running on port ${PORT}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo   logMessage(`Open your browser and navigate to: http://localhost:${PORT}`); >> "D:\AIArm\WebInterface\minimal_sd_server.js"
echo }); >> "D:\AIArm\WebInterface\minimal_sd_server.js"

echo ✓ Created minimal server

REM Create a simple HTML test page
echo Creating test page...
echo ^<!DOCTYPE html^> > "D:\AIArm\WebInterface\sd_test.html"
echo ^<html lang="en"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo ^<head^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<meta charset="UTF-8"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<title^>StableDiffusion Test^</title^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<style^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     h1 { color: #333; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     .input-group { margin-bottom: 15px; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     label { display: block; margin-bottom: 5px; font-weight: bold; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     input[type="text"] { width: 100%%; padding: 8px; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     button { padding: 10px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     button:hover { background-color: #45a049; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     #result { margin-top: 20px; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     #imageResult { max-width: 100%%; margin-top: 15px; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     .status { padding: 10px; border-radius: 4px; margin-bottom: 15px; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     .success { background-color: #d4edda; color: #155724; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     .error { background-color: #f8d7da; color: #721c24; } >> "D:\AIArm\WebInterface\sd_test.html"
echo     .loading { background-color: #fff3cd; color: #856404; } >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^</style^> >> "D:\AIArm\WebInterface\sd_test.html"
echo ^</head^> >> "D:\AIArm\WebInterface\sd_test.html"
echo ^<body^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<h1^>StableDiffusion Integration Test^</h1^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<div class="input-group"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^<label for="prompt"^>Image Prompt:^</label^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^<input type="text" id="prompt" placeholder="Enter a description of the image you want to generate..." value="A beautiful mountain landscape with a lake at sunset"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^</div^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<div class="input-group"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^<label for="quality"^>Quality:^</label^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^<select id="quality"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo       ^<option value="low"^>Low (Faster)^</option^> >> "D:\AIArm\WebInterface\sd_test.html"
echo       ^<option value="medium" selected^>Medium^</option^> >> "D:\AIArm\WebInterface\sd_test.html"
echo       ^<option value="high"^>High (Slower)^</option^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^</select^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^</div^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<div class="input-group"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^<label for="style"^>Style:^</label^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^<select id="style"^> >> "D:\AIArm\WebInterface\sd_test.html"
echo       ^<option value="photorealistic" selected^>Photorealistic^</option^> >> "D:\AIArm\WebInterface\sd_test.html"
echo       ^<option value="anime"^>Anime^</option^> >> "D:\AIArm\WebInterface\sd_test.html"
echo       ^<option value="painting"^>Painting^</option^> >> "D:\AIArm\WebInterface\sd_test.html"
echo       ^<option value="3d"^>3D Render^</option^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     ^</select^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^</div^> >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<button id="generateButton"^>Generate Image^</button^> >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<div id="result"^>^</div^> >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^<script^> >> "D:\AIArm\WebInterface\sd_test.html"
echo     document.getElementById('generateButton').addEventListener('click', generateImage); >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo     async function generateImage() { >> "D:\AIArm\WebInterface\sd_test.html"
echo       const prompt = document.getElementById('prompt').value; >> "D:\AIArm\WebInterface\sd_test.html"
echo       const quality = document.getElementById('quality').value; >> "D:\AIArm\WebInterface\sd_test.html"
echo       const style = document.getElementById('style').value; >> "D:\AIArm\WebInterface\sd_test.html"
echo       const resultDiv = document.getElementById('result'); >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo       if (!prompt) { >> "D:\AIArm\WebInterface\sd_test.html"
echo         resultDiv.innerHTML = `^<div class="status error"^>Please enter a prompt^</div^>`; >> "D:\AIArm\WebInterface\sd_test.html"
echo         return; >> "D:\AIArm\WebInterface\sd_test.html"
echo       } >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo       resultDiv.innerHTML = `^<div class="status loading"^>Generating image... This may take a moment.^</div^>`; >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo       try { >> "D:\AIArm\WebInterface\sd_test.html"
echo         const response = await fetch('/api/photo-generation', { >> "D:\AIArm\WebInterface\sd_test.html"
echo           method: 'POST', >> "D:\AIArm\WebInterface\sd_test.html"
echo           headers: { >> "D:\AIArm\WebInterface\sd_test.html"
echo             'Content-Type': 'application/json', >> "D:\AIArm\WebInterface\sd_test.html"
echo           }, >> "D:\AIArm\WebInterface\sd_test.html"
echo           body: JSON.stringify({ >> "D:\AIArm\WebInterface\sd_test.html"
echo             prompt, >> "D:\AIArm\WebInterface\sd_test.html"
echo             options: { >> "D:\AIArm\WebInterface\sd_test.html"
echo               quality, >> "D:\AIArm\WebInterface\sd_test.html"
echo               style, >> "D:\AIArm\WebInterface\sd_test.html"
echo               // Set dimensions to speed up generation >> "D:\AIArm\WebInterface\sd_test.html"
echo               width: 512, >> "D:\AIArm\WebInterface\sd_test.html"
echo               height: 512 >> "D:\AIArm\WebInterface\sd_test.html"
echo             } >> "D:\AIArm\WebInterface\sd_test.html"
echo           }) >> "D:\AIArm\WebInterface\sd_test.html"
echo         }); >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo         if (!response.ok) { >> "D:\AIArm\WebInterface\sd_test.html"
echo           throw new Error(`HTTP error! status: ${response.status}`); >> "D:\AIArm\WebInterface\sd_test.html"
echo         } >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo         const data = await response.json(); >> "D:\AIArm\WebInterface\sd_test.html"
echo         console.log("Response data:", data); >> "D:\AIArm\WebInterface\sd_test.html"
echo. >> "D:\AIArm\WebInterface\sd_test.html"
echo         if (data.success) { >> "D:\AIArm\WebInterface\sd_test.html"
echo           const imageUrl = data.image_url || data.result; >> "D:\AIArm\WebInterface\sd_test.html"
echo           resultDiv.innerHTML = ` >> "D:\AIArm\WebInterface\sd_test.html"
echo             ^<div class="status success"^>Image generated successfully!^</div^> >> "D:\AIArm\WebInterface\sd_test.html"
echo             ^<p^>Prompt: ${prompt}^</p^> >> "D:\AIArm\WebInterface\sd_test.html"
echo             ^<p^>Quality: ${quality} | Style: ${style}^</p^> >> "D:\AIArm\WebInterface\sd_test.html"
echo             ^<img id="imageResult" src="${imageUrl}" alt="Generated image" /^> >> "D:\AIArm\WebInterface\sd_test.html"
echo           `; >> "D:\AIArm\WebInterface\sd_test.html"
echo         } else { >> "D:\AIArm\WebInterface\sd_test.html"
echo           resultDiv.innerHTML = `^<div class="status error"^>Error: ${data.error || 'Unknown error'}^</div^>`; >> "D:\AIArm\WebInterface\sd_test.html"
echo         } >> "D:\AIArm\WebInterface\sd_test.html"
echo       } catch (error) { >> "D:\AIArm\WebInterface\sd_test.html"
echo         console.error('Error:', error); >> "D:\AIArm\WebInterface\sd_test.html"
echo         resultDiv.innerHTML = `^<div class="status error"^>Error: ${error.message}^</div^>`; >> "D:\AIArm\WebInterface\sd_test.html"
echo       } >> "D:\AIArm\WebInterface\sd_test.html"
echo     } >> "D:\AIArm\WebInterface\sd_test.html"
echo   ^</script^> >> "D:\AIArm\WebInterface\sd_test.html"
echo ^</body^> >> "D:\AIArm\WebInterface\sd_test.html"
echo ^</html^> >> "D:\AIArm\WebInterface\sd_test.html"

echo ✓ Created test page

REM Update main index.html to link to the test page
echo Updating index.html...

if exist "D:\AIArm\WebInterface\index.html" (
  echo ^<a href="sd_test.html"^>StableDiffusion Test Page^</a^>^<br^> >> "D:\AIArm\WebInterface\index.html"
  echo ✓ Updated index.html
) else (
  echo ^<!DOCTYPE html^> > "D:\AIArm\WebInterface\index.html"
  echo ^<html lang="en"^> >> "D:\AIArm\WebInterface\index.html"
  echo ^<head^> >> "D:\AIArm\WebInterface\index.html"
  echo   ^<meta charset="UTF-8"^> >> "D:\AIArm\WebInterface\index.html"
  echo   ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^> >> "D:\AIArm\WebInterface\index.html"
  echo   ^<title^>AIArm System^</title^> >> "D:\AIArm\WebInterface\index.html"
  echo ^</head^> >> "D:\AIArm\WebInterface\index.html"
  echo ^<body^> >> "D:\AIArm\WebInterface\index.html"
  echo   ^<h1^>AIArm System^</h1^> >> "D:\AIArm\WebInterface\index.html"
  echo   ^<a href="real_interface.html"^>Main Interface^</a^>^<br^> >> "D:\AIArm\WebInterface\index.html"
  echo   ^<a href="sd_test.html"^>StableDiffusion Test Page^</a^>^<br^> >> "D:\AIArm\WebInterface\index.html"
  echo ^</body^> >> "D:\AIArm\WebInterface\index.html"
  echo ^</html^> >> "D:\AIArm\WebInterface\index.html"
  echo ✓ Created index.html
)

REM Start the minimal server
echo.
echo Starting minimal server...
cd /d "D:\AIArm\WebInterface"
start "AIArm Minimal SD Server" cmd /c "node minimal_sd_server.js"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Check if server is running
echo Checking if minimal server is running...
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; Write-Host '✓ Minimal server is running on port 45678' } catch { Write-Host '✗ Minimal server is NOT running on port 45678' }"

echo.
echo Setup complete!
echo.
echo You can now access the test page at:
echo http://localhost:45678/sd_test.html
echo.
echo This page will let you test the StableDiffusion integration directly.
echo.
echo Press any key to exit...
pause >nul