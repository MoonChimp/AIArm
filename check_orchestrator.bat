@echo off
echo =====================================================================
echo            AIArm ORCHESTRATOR CHECK UTILITY
echo =====================================================================
echo.

cd /D "D:\AIArm\WebInterface"

echo Checking for Python orchestrator...
echo This will try to locate and test your AI orchestrator...
echo.

node check_orchestrator.js

echo.
echo Check complete.
echo.
echo Once you know your orchestrator's capabilities, you can:
echo 1. Run D:\AIArm\guaranteed_solution.bat to start the interface
echo 2. Or run D:\AIArm\launch_real_agents.bat to connect to real agents
echo.

pause
