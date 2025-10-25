@echo off
echo =====================================================================
echo            AIArm ORCHESTRATOR METHOD FINDER
echo =====================================================================
echo.

cd /D "D:\AIArm\WebInterface"

echo Finding all available methods in your orchestrator...
echo This will help us identify how to interact with it correctly...
echo.

python orchestrator_bridge.py --list-methods

echo.
echo Test complete.
echo.

pause
