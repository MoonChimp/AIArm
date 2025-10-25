@echo off
echo =====================================================================
echo     STARTING NEXUS HRM SYSTEM MONITOR
echo =====================================================================
echo.

echo Starting system monitor...
start "Nexus System Monitor" cmd /c "node D:\AIArm\WebInterface\system_monitor.js"

echo System monitor started.
echo.
echo The monitor will automatically restart the system if it detects issues.
echo Maximum automatic restarts per day: 3
echo.
