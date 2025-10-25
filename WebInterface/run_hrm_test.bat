@echo off
echo =====================================================================
echo              HRM SYSTEM TEST - VERIFYING DUAL BRIDGES
echo =====================================================================
echo.

echo Step 1: Checking that the HRM system is running...
curl -s http://localhost:45678/health > nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: HRM System is not running or not accessible at localhost:45678
    echo Please start the HRM System with start_nexus_hrm.bat before running this test.
    goto end
)

echo Step 2: Running HRM system test...
python test_hrm_system.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: HRM System test failed. Please check logs for details.
    goto end
)

echo.
echo =====================================================================
echo              HRM SYSTEM TEST COMPLETED
echo =====================================================================

:end
pause
