@echo off
:: Check for admin rights and elevate if needed
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B
) else (
    goto gotAdmin
)

:gotAdmin
    if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs"
    pushd "%CD%"
    CD /D "%~dp0"

title AlfaZer0 - Diagnostic Mode
echo AlfaZer0 - Diagnostic Mode
echo =========================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

REM Create necessary directories if they don't exist
if not exist "D:\NexusAI" mkdir "D:\NexusAI"
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"

echo Creating a diagnostic test file from the launcher...
echo This is a diagnostic test file created by the launcher on %date% at %time%. > "D:\AIArm\Test\launcher_test.txt"
echo.

REM Set up diagnostic mode
set "PORT=45678"
set "DIAGNOSTIC_MODE=true"

echo Running a direct command test from the batch file...
echo This is a test file created by the diagnostic batch file > "D:\AIArm\Test\direct_batch_test.txt"
echo Batch file test completed.
echo.

echo Testing Python directly from the batch file...
python -c "
import os
with open('D:/AIArm/Test/python_batch_test.txt', 'w') as f:
    f.write('This is a test file created by Python from the batch file')
print('Python direct test completed.')
"
echo.

echo Testing alfazer0_bridge.py directly...
cd /d "D:\AIArm\WebInterface"
echo {"operation":"write_file","path":"D:/AIArm/Test/bridge_direct_test.txt","content":"Bridge direct test"} | python alfazer0_bridge.py
echo.

echo Running diagnostic bridge test...
echo {"operation":"test"} | python diagnostic_bridge.py > diagnostic_output.json
echo Diagnostic bridge test completed. Output saved to diagnostic_output.json
echo.

echo Starting server in diagnostic mode...
node "real_server.js" --port %PORT% --bridge diagnostic_bridge.py

echo.
echo Server stopped. Press any key to exit...
pause > nul
