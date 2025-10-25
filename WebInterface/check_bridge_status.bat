@echo off
echo.
echo === AIArm Bridge Status Check ===
echo.

REM Check if server is running
echo Checking if AIArm server is running...
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; Write-Host '✓ AIArm server is running on port 45678' } catch { Write-Host '✗ AIArm server is NOT running on port 45678' }"

REM Get detailed server status
echo.
echo Getting detailed server status...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; Write-Host ('Server status: ' + $response.status); Write-Host ('Surface bridge: ' + $response.surface_bridge.status); Write-Host ('Deep bridge: ' + $response.deep_bridge.status); } catch { Write-Host '✗ Failed to get server status' }"

REM Check if server logs exist
echo.
echo Checking server logs...
if exist "D:\AIArm\WebInterface\Logs\server_2025-09-17.log" (
  echo ✓ Server log exists
  echo Analyzing recent errors...
  powershell -Command "Get-Content 'D:\AIArm\WebInterface\Logs\server_2025-09-17.log' -Tail 50 | Select-String -Pattern 'error','exception','failed' | ForEach-Object { Write-Host $_ }"
) else (
  echo ✗ Server log not found
)

echo.
echo Making simple test request...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; $responseJson = ConvertTo-Json $response -Depth 5; Write-Host $responseJson } catch { Write-Host '✗ Failed to get server status' }"

echo.
echo Status check complete.
echo.
echo Press any key to exit...
pause >nul