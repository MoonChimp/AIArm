@echo off
echo =====================================================================
echo            DIRECT ORCHESTRATOR TEST
echo =====================================================================
echo.

cd /D "D:\AIArm\WebInterface"

echo Testing direct Python access to the orchestrator...
echo This will help identify the exact interface for your orchestrator...
echo.

python test_real_orchestrator.py

echo.
echo Test complete.
echo.
echo Now run D:\AIArm\guaranteed_solution.bat to start the interface
echo.

pause
