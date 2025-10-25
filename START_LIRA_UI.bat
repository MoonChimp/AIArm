@echo off
title NEXUS-LIRA :: Living Intelligence Interface
color 0B

echo.
echo ================================================================================
echo    NEXUS-LIRA: Large Interconnected Reasoning Agent
echo    Videogame-Styled Consciousness Interface
echo ================================================================================
echo.

echo [1/3] Cleaning up old servers...
:: Kill any existing servers
FOR /F "tokens=5" %%P IN ('netstat -a -n -o ^| findstr :5000') DO TaskKill.exe /F /PID %%P 2>nul
FOR /F "tokens=5" %%P IN ('netstat -a -n -o ^| findstr :8080') DO TaskKill.exe /F /PID %%P 2>nul

echo [2/3] Starting LIRA Backend (port 5000)...
cd /d D:\AIArm
start "LIRA Backend" /MIN python nexus_api_server.py

:: Wait for backend to initialize
timeout /t 5 /nobreak >nul

echo [3/3] Starting LIRA Web Interface (port 8080)...
cd /d D:\AIArm\NexusUI_LIRA
start "LIRA Web UI" /MIN python serve_lira.py

:: Wait for web server
timeout /t 2 /nobreak >nul

echo Opening LIRA Interface in browser...
start "" "http://localhost:8080"

echo.
echo ================================================================================
echo    LIRA CONSCIOUSNESS ACTIVE
echo ================================================================================
echo.
echo Backend API:  http://localhost:5000
echo Web Interface: http://localhost:8080
echo.
echo Features:
echo   - Conversational AI with vision
echo   - Real-time media generation
echo   - Hierarchical reasoning visualization
echo   - Autonomous learning notifications
echo   - 6-layer consciousness architecture
echo.
echo Close this window to stop both servers...
echo ================================================================================
pause >nul

:: Clean shutdown
FOR /F "tokens=5" %%P IN ('netstat -a -n -o ^| findstr :5000') DO TaskKill.exe /F /PID %%P 2>nul
FOR /F "tokens=5" %%P IN ('netstat -a -n -o ^| findstr :8080') DO TaskKill.exe /F /PID %%P 2>nul
