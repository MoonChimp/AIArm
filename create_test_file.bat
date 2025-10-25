@echo off
echo Creating test file for Nexus AI...

set TEST_DIR=D:\AIArm\Test
set TEST_FILE=%TEST_DIR%\nexus_test_file.txt
set CONTENT=This is a test file created by Nexus AI on %date% at %time%.^

This file demonstrates that Nexus has filesystem capabilities and can create files on your system.^

If you can read this, the test was successful!

if not exist "%TEST_DIR%" mkdir "%TEST_DIR%"

echo %CONTENT% > "%TEST_FILE%"

if %errorlevel% neq 0 (
    echo Failed to create test file!
    exit /b 1
)

echo Test file created successfully at: %TEST_FILE%
echo.
echo Content:
echo --------
type "%TEST_FILE%"
echo --------
echo.

echo Test complete!
pause