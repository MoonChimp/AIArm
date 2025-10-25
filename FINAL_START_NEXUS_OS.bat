@echo off
title NEXUS OS - Final Launch
color 0C

echo.
echo ================================================================================
echo                         NEXUS OS - FINAL LAUNCHER
echo                     Gaming AI Control Center
echo ================================================================================
echo.

:: Step 1: KILL EVERYTHING
echo [1/5] Killing ALL old processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq Stable Diffusion*" >nul 2>&1
taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq Nexus*" >nul 2>&1
timeout /t 3 /nobreak >nul

:: Step 2: Start Stable Diffusion WebUI
echo [2/5] Starting Stable Diffusion WebUI...
echo    This may take 15-20 seconds to initialize...
cd /d "D:\AIArm\stable-diffusion-webui-master"
start "Stable Diffusion WebUI" cmd /k "webui-user.bat --api"
cd /d D:\AIArm
timeout /t 5 /nobreak >nul

:: Step 3: Start Nexus API Server
echo [3/5] Starting Nexus API Backend...
start "Nexus API Server" cmd /k "python nexus_api_server.py"
timeout /t 8 /nobreak >nul

:: Step 4: Start NexusOS Web Server
echo [4/5] Starting NexusOS Web Interface...
cd /d D:\AIArm\NexusOS
start "NexusOS Web Server" cmd /k "python serve.py"
timeout /t 3 /nobreak >nul

:: Step 5: Open NexusOS in Browser
echo [5/5] Launching NexusOS in browser...
start "" "http://localhost:8080"

echo.
echo ================================================================================
echo                         NEXUS OS LAUNCHED
echo ================================================================================
echo.
echo  SERVICES STARTED:
echo   - Stable Diffusion WebUI  (http://localhost:7860)
echo   - Nexus API Backend       (http://localhost:5000)
echo   - NexusOS Interface       (http://localhost:8080)
echo.
echo  WAIT 15-20 SECONDS for Stable Diffusion to fully initialize.
echo  Then refresh the NexusOS page - all services should be GREEN.
echo.
echo  Press any key to STOP all services...
pause >nul

:: Shutdown all services
echo.
echo Stopping all services...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq Stable Diffusion*" >nul 2>&1
taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq Nexus*" >nul 2>&1
echo All services stopped.
timeout /t 2 /nobreak >nul
