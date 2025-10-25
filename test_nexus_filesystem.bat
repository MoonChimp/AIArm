@echo off
title Test Nexus Filesystem Capabilities
echo Testing Nexus Filesystem Capabilities
echo.

set "FILE_PATH=D:\AIArm\Test\nexus_direct_test.txt"
set "CONTENT=This file was created by Nexus direct test on %date% at %time%."

echo Creating test directory...
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"

echo Writing test file...
echo %CONTENT% > "%FILE_PATH%"

if %errorlevel% neq 0 (
    echo ERROR: Failed to create test file!
    pause
    exit /b 1
)

echo Test file created at: %FILE_PATH%
echo.
echo Content:
echo ----------------------
type "%FILE_PATH%"
echo ----------------------
echo.
echo Test completed successfully!

pause