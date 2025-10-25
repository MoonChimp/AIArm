@echo off
echo.
echo === Restarting AIArm System with StableDiffusion Integration ===
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
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:7860/sdapi/v1/sd-models' -Method 'GET'; Write-Host '✓ StableDiffusion WebUI is running on port 7860' } catch { Write-Host '✗ StableDiffusion WebUI is NOT running on port 7860'; Write-Host 'Please start StableDiffusion WebUI with API enabled first.'; exit 1 }"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Please start StableDiffusion WebUI with API enabled using the find_sd_webui.bat script
  echo and then run this script again.
  echo.
  echo Press any key to exit...
  pause >nul
  exit /b
)

REM Start the server
echo.
echo Starting AIArm concurrent server...
cd /d "D:\AIArm\WebInterface"
start "AIArm HRM Server" cmd /c "node concurrent_server.js --surface-bridge improved_bridge.py --deep-bridge ollama_bridge.py"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Check if server is running
echo Checking if AIArm server is running...
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; Write-Host '✓ AIArm server is running on port 45678' } catch { Write-Host '✗ AIArm server is NOT running on port 45678'; exit 1 }"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Failed to start AIArm server. Please check the logs for errors.
  echo.
  echo Press any key to exit...
  pause >nul
  exit /b
)

REM Make a test request
echo.
echo Making test request to generate an image...
echo.

set TEST_PROMPT=A beautiful mountain landscape with a lake and forest

echo Sending request with prompt: "%TEST_PROMPT%"
echo.

powershell -Command "$body = @{ prompt = '%TEST_PROMPT%'; options = @{ quality = 'high'; style = 'photorealistic' }; userId = 'test_user' } | ConvertTo-Json; try { $response = Invoke-RestMethod -Uri 'http://localhost:45678/api/photo-generation' -Method 'POST' -Body $body -ContentType 'application/json'; if ($response.success) { Write-Host '✓ Successfully generated image'; Write-Host ('Image URL: ' + $response.image_url); } else { Write-Host '✗ Failed to generate image'; Write-Host ('Error: ' + $response.error); } } catch { Write-Host '✗ API request failed'; Write-Host ('Error: ' + $_); }"

echo.
echo Setup complete!
echo.
echo You can now access the AIArm interface at:
echo http://localhost:45678/real_interface.html
echo.
echo Press any key to exit...
pause >nul