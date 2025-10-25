@echo off
title NEXUS - Complete System Launch
color 0A

echo.
echo ================================================================================
echo                         NEXUS AI SYSTEM LAUNCHER
echo                    Initializing All Backend Services
echo ================================================================================
echo.

:: Step 1: Clean up all existing processes
echo [1/5] Terminating existing processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

:: Step 2: Start Stable Diffusion WebUI
echo [2/5] Starting Stable Diffusion WebUI (port 7860)...
cd /d D:\AIArm\stable-diffusion-webui-master
start "Stable Diffusion WebUI" /MIN webui-user.bat --api
cd /d D:\AIArm
timeout /t 3 /nobreak >nul

:: Step 3: Start Nexus API Backend
echo [3/5] Starting Nexus API Server (port 5000)...
start "Nexus API Backend" /MIN python nexus_api_server.py
timeout /t 8 /nobreak >nul

:: Step 4: Open interfaces
echo [4/5] Opening System Monitor...
start "" "D:\AIArm\NexusUI_Monitor\monitor.html"
timeout /t 2 /nobreak >nul

echo [5/5] Opening Nexus Chat Interface...
start "" "D:\AIArm\NexusUI_Crystal\index.html"

echo.
echo ================================================================================
echo                      ALL SYSTEMS OPERATIONAL
echo ================================================================================
echo.
echo RUNNING SERVICES:
echo   [*] Stable Diffusion WebUI - http://localhost:7860
echo   [*] Nexus API Server       - http://localhost:5000
echo   [*] System Monitor         - Monitoring all services
echo   [*] Crystal UI             - Chat interface ready
echo.
echo AVAILABLE CAPABILITIES:
echo   - All 6 Agents (Code, Music, Photo, Story, Video, WebSearch)
echo   - LIRA 6-Layer Consciousness
echo   - LightWare + DarkWare Learning
echo   - Inner Life (Memory, Emotions)
echo   - Hierarchical Reasoning
echo   - Filesystem Access
echo.
echo MONITOR: Check the System Monitor window for real-time status
echo.
echo Press any key to STOP ALL SERVICES...
pause >nul

:: Clean shutdown
echo.
echo Shutting down all services...
taskkill /F /IM python.exe 2>nul
echo All services stopped.
timeout /t 2 /nobreak >nul
