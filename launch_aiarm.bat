@echo off
echo =====================================================================
echo                   AIARM SYSTEM QUICK LAUNCHER
echo =====================================================================
echo.

echo Choose the interface to launch:
echo.
echo [1] Crystalline Interface
echo [2] HRM Production System
echo [3] Code Assistant
echo [4] System Monitor
echo [5] Check Port Availability
echo [6] Free Up Ports
echo.

set /p choice=Enter your choice (1-6): 

if "%choice%"=="1" (
    echo Launching Crystalline Interface...
    start "" cmd /c "D:\AIArm\WebInterface\start_crystalline_interface.bat"
) else if "%choice%"=="2" (
    echo Launching HRM Production System...
    start "" cmd /c "D:\AIArm\WebInterface\start_hrm_production.bat"
) else if "%choice%"=="3" (
    echo Launching Code Assistant...
    start "" http://localhost:3100/code_assistant.html
) else if "%choice%"=="4" (
    echo Launching System Monitor...
    start "" cmd /c "D:\AIArm\WebInterface\system_monitor.bat"
) else if "%choice%"=="5" (
    echo Checking Port Availability...
    python D:\AIArm\WebInterface\check_ports.py
    pause
) else if "%choice%"=="6" (
    echo Running Port Cleanup Utility...
    call D:\AIArm\WebInterface\free_ports.bat
) else (
    echo Invalid choice. Please enter a number between 1 and 6.
    timeout /t 3 >nul
    %0
)

echo.
echo If you encounter any issues, run option 5 to check port availability
echo and option 6 to free up any ports that might be in use.
echo.

if not "%choice%"=="5" if not "%choice%"=="6" (
    echo Process started. You can close this window.
)
