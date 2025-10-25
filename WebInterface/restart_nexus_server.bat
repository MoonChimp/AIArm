@echo off
echo.
echo === Restarting NexusAI Server with FileSystem Capabilities ===
echo.

REM Kill existing node processes
echo Stopping existing node processes...
taskkill /F /IM node.exe /T 2>nul
if %ERRORLEVEL% EQU 0 (
  echo Successfully terminated existing server
) else (
  echo No existing server found
)

REM Small delay to ensure ports are released
timeout /t 2 /nobreak >nul

REM Start the server
echo.
echo Starting NexusAI server...
cd /d "D:\AIArm\WebInterface"
start "NexusAI Server" cmd /c "node concurrent_server.js --surface-bridge improved_bridge.py --deep-bridge ollama_bridge.py"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo Server started. You can now access the interface at:
echo http://localhost:45678/real_interface.html
echo.
echo To use the filesystem capabilities:
echo 1. Open the interface in your browser
echo 2. Click on the "File System" agent in the sidebar
echo 3. Use commands like "help", "list D:\", "read D:\filename.txt", etc.
echo.
echo Press any key to exit...
pause >nul