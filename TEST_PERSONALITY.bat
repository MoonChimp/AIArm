@echo off
echo ============================================================
echo     Testing Nexus Personality Matrix
echo ============================================================
echo.
echo This will test the Cortana/JARVIS/TARS/Claude personality fusion
echo.
pause

cd /d D:\AIArm\NexusCore\personality
python personality_matrix.py

echo.
echo ============================================================
echo     Test Complete
echo ============================================================
echo.
echo If you saw personality initialization and test outputs,
echo the personality system is working correctly!
echo.
pause
