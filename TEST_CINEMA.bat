@echo off
echo ============================================================
echo     Testing Nexus Cinema Agent
echo ============================================================
echo.
echo This will test Hollywood-quality content generation with SDXL
echo Note: First run will download models (several GB)
echo.
pause

cd /d D:\AIArm\NexusCore\cinema
python cinema_agent.py

echo.
echo ============================================================
echo     Test Complete
echo ============================================================
echo.
echo If you saw cinema agent initialization and status,
echo the system is working correctly!
echo.
echo Generated images will be saved to:
echo D:\AIArm\Generated\Cinema\
echo.
pause
