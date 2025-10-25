@echo off
title NEXUS OS - Gaming AI Control Center
color 0C

echo.
echo ================================================================================
echo                            NEXUS OS LAUNCHER
echo                     AI Gaming Control Center
echo ================================================================================
echo.

:: Kill old processes
echo [1/4] Terminating old processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

:: Start Nexus API
echo [2/4] Starting Nexus API Backend (port 5000)...
cd /d D:\AIArm
start "Nexus API" /MIN python nexus_api_server.py
timeout /t 6 /nobreak >nul

:: Start NexusOS Web Server
echo [3/4] Starting NexusOS Interface (port 8080)...
cd /d D:\AIArm\NexusOS
start "NexusOS Web" /MIN python serve.py
timeout /t 2 /nobreak >nul

:: Open NexusOS
echo [4/4] Launching NexusOS...
start "" "http://localhost:8080"

echo.
echo ================================================================================
echo                         NEXUS OS ONLINE
echo ================================================================================
echo.
echo  NexusOS Interface:  http://localhost:8080
echo  Nexus API Backend:  http://localhost:5000
echo  Ollama LLM:         http://localhost:11434 (should be running)
echo.
echo  Send screenshots of NitroSense tabs to replicate exact design!
echo.
echo  Press any key to STOP all services...
pause >nul

:: Shutdown
taskkill /F /IM python.exe 2>nul
echo Stopped.
