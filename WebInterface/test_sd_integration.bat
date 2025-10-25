@echo off
echo.
echo === Testing AIArm with StableDiffusion Integration ===
echo.

REM Check if servers are running
echo Checking if AIArm server is running...
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; Write-Host '✓ AIArm server is running on port 45678' } catch { Write-Host '✗ AIArm server is NOT running on port 45678' }"

echo Checking if StableDiffusion WebUI is running...
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:7860/sdapi/v1/sd-models' -Method 'GET'; Write-Host '✓ StableDiffusion WebUI is running on port 7860' } catch { Write-Host '✗ StableDiffusion WebUI is NOT running on port 7860' }"

echo.
echo Making test request to AIArm Photo Generation API...
echo This will generate a test image using StableDiffusion...
echo.

set TEST_PROMPT=A colorful sunset over a peaceful lake with mountains in the background

echo Sending request with prompt: "%TEST_PROMPT%"
echo.

powershell -Command "$body = @{ prompt = '%TEST_PROMPT%'; options = @{ quality = 'high'; style = 'photorealistic' }; userId = 'test_user' } | ConvertTo-Json; try { $response = Invoke-RestMethod -Uri 'http://localhost:45678/api/photo-generation' -Method 'POST' -Body $body -ContentType 'application/json'; if ($response.success) { Write-Host '✓ Successfully generated image'; Write-Host ('Image URL: ' + $response.result); } else { Write-Host '✗ Failed to generate image'; Write-Host ('Error: ' + $response.error); } } catch { Write-Host '✗ API request failed'; Write-Host ('Error: ' + $_); }"

echo.
echo Test complete. If the test was successful, you should be able to access the AIArm interface at:
echo http://localhost:45678/real_interface.html
echo.
echo Press any key to exit...
pause >nul