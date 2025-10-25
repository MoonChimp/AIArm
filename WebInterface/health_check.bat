@echo off
echo.
echo === AIArm HRM Health Check ===
echo.

REM Check if server is running
netstat -ano | find "45678" > nul
if %ERRORLEVEL% EQU 0 (
  echo ✓ Server is running on port 45678
) else (
  echo ✗ Server is NOT running on port 45678
  echo.
  echo Would you like to start the server? (Y/N)
  choice /C YN /M "Start server"
  if %ERRORLEVEL% EQU 1 (
    call "D:\AIArm\WebInterface\restart_hrm_concurrent.bat"
    goto :end
  )
)

REM Check if Ollama is running
powershell -Command "try { $null = Invoke-RestMethod -Uri 'http://localhost:11434/api/tags' -Method 'GET'; Write-Host '✓ Ollama is running on port 11434' } catch { Write-Host '✗ Ollama is NOT running on port 11434' }"

REM Check if logs directory exists
if exist "D:\AIArm\WebInterface\Logs" (
  echo ✓ Logs directory exists
) else (
  echo ✗ Logs directory does not exist
  mkdir "D:\AIArm\WebInterface\Logs"
  echo   Created Logs directory
)

REM Check if Memory directory exists
if exist "D:\AIArm\Memory" (
  echo ✓ Memory directory exists
) else (
  echo ✗ Memory directory does not exist
  mkdir "D:\AIArm\Memory"
  echo   Created Memory directory
)

REM Check bridge files
if exist "D:\AIArm\WebInterface\improved_bridge.py" (
  echo ✓ Surface bridge (improved_bridge.py) exists
) else (
  echo ✗ Surface bridge (improved_bridge.py) does not exist
)

if exist "D:\AIArm\WebInterface\ollama_bridge.py" (
  echo ✓ Deep bridge (ollama_bridge.py) exists
) else (
  echo ✗ Deep bridge (ollama_bridge.py) does not exist
)

REM Make a test API call to the server if it's running
echo.
echo Performing server health check API call...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; Write-Host ('Server status: ' + $response.status); Write-Host ('Surface bridge: ' + $response.surface_bridge.status); Write-Host ('Deep bridge: ' + $response.deep_bridge.status); } catch { Write-Host '✗ Failed to connect to server API' }"

echo.
echo Health check complete.
echo.

:end
echo Press any key to exit...
pause >nul