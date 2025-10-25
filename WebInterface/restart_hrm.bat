@echo off
echo =====================================================================
echo     RESTARTING NEXUS HRM ARCHITECTURE SYSTEM
echo =====================================================================
echo.

echo STEP 1: Stopping running processes...
taskkill /F /IM node.exe /T
taskkill /F /IM python.exe /T
echo Processes terminated.
echo.

echo STEP 2: Waiting for system to settle...
timeout /t 5 > nul
echo.

echo STEP 3: Starting HRM system...
start "" "D:\AIArm\WebInterface\start_nexus_hrm.bat"
echo Restart process initiated.
echo.

echo System should be online again in approximately 20-30 seconds.
echo.
