@echo off
echo.
echo === Restarting AIArm HRM Concurrent Server ===
echo.

REM Kill existing node process for the server
taskkill /F /IM node.exe /T 2>nul
if %ERRORLEVEL% EQU 0 (
  echo ✓ Successfully terminated existing server
) else (
  echo ✓ No existing server found
)

REM Small delay to ensure ports are released
timeout /t 2 /nobreak >nul

REM Start the server with improved configuration
echo.
echo Starting concurrent server...
cd /d "D:\AIArm\WebInterface"
start "AIArm HRM Server" cmd /c "node concurrent_server.js --surface-bridge improved_bridge.py --deep-bridge ollama_bridge.py"

echo.
echo ✓ Server restarted successfully!
echo.
echo Please check the Logs directory for any error messages.
echo The server should be accessible at http://localhost:45678
echo.
echo Press any key to exit...
pause >nul