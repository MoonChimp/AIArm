@echo off
title NEXUS AI - Service Manager
color 0E

echo.
echo ╔══════════════════════════════════════╗
echo ║     NEXUS AI - Service Manager      ║
echo ╚══════════════════════════════════════╝
echo.

REM Kill existing Python processes
echo [*] Cleaning up existing processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start Python service manager
echo [*] Starting unified service manager...
python START_NEXUS.py

pause
