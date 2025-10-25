@echo off
echo.
echo === AIArm Photo Generation Direct Test ===
echo.

REM Check if server is running
echo Checking if AIArm server is running...
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; Write-Host '✓ AIArm server is running on port 45678' } catch { Write-Host '✗ AIArm server is NOT running on port 45678'; exit 1 }"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Server is not running. Please start the server first.
  echo.
  echo Press any key to exit...
  pause >nul
  exit /b
)

echo.
echo Sending simplified test request to photo generation endpoint...
echo.

set TEST_PROMPT=Test mountain landscape

echo Using prompt: "%TEST_PROMPT%"
echo.

powershell -Command "
$ErrorActionPreference = 'Continue';
$body = @{
  prompt = '%TEST_PROMPT%';
  options = @{ 
    quality = 'medium';
    width = 512;
    height = 512;
    steps = 20;
  };
} | ConvertTo-Json;

Write-Host 'Request body:';
Write-Host $body;
Write-Host '';

try {
  Write-Host 'Sending request to http://localhost:45678/api/photo-generation...';
  $response = Invoke-RestMethod -Uri 'http://localhost:45678/api/photo-generation' -Method 'POST' -Body $body -ContentType 'application/json';
  Write-Host 'Got response:';
  $responseJson = ConvertTo-Json $response -Depth 5;
  Write-Host $responseJson;
  
  if ($response.success) {
    Write-Host '✓ Successfully generated image';
    Write-Host ('Image URL: ' + $response.image_url);
  } else {
    Write-Host '✗ Failed to generate image';
    Write-Host ('Error: ' + $response.error);
  }
} catch {
  Write-Host '✗ API request failed';
  Write-Host ('Error: ' + $_);
}
"

echo.
echo Test complete.
echo.
echo Press any key to exit...
pause >nul