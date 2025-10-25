@echo off
echo =====================================================================
echo             Ultimate Port Cleanup Utility
echo =====================================================================
echo.
echo This utility will kill ALL Node.js processes to free up ports
echo.

echo Killing all Node.js processes...
taskkill /F /IM node.exe

echo.
echo All Node.js processes have been terminated.
echo You can now restart the AIArm server.
echo.

pause
