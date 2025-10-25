@echo off
echo ============================================================
echo     NEXUS AI - Working Startup (No Node.js Issues)
echo ============================================================
echo.
echo Starting backend only (React UI has Node.js v24 issue)
echo Use standalone HTML interface instead!
echo.

echo [1/2] Starting Nexus Backend...
start "Nexus Backend" cmd /k "cd /d D:\AIArm && python nexus_api_server.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo [2/2] Opening Standalone Interface...
start "" "D:\AIArm\NEXUS_STANDALONE.html"

echo.
echo ============================================================
echo     NEXUS STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo Backend running on: http://localhost:5000
echo Interface opened in your browser
echo.
echo This avoids the Node.js v24 / Rollup issue completely!
echo.
echo To fix React UI (optional):
echo 1. Download Node.js v20 LTS from nodejs.org
echo 2. Reinstall NexusUI dependencies
echo 3. Then React UI will work
echo.
echo But standalone interface has ALL features you need!
echo.
pause
