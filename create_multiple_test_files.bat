@echo off
title Nexus AI - Write Multiple Test Files
echo Nexus AI - Write Multiple Test Files
echo ===================================
echo.

echo This script will create 5 test files in different locations.
echo.

REM Create test directories if they don't exist
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"
if not exist "D:\Nexus" mkdir "D:\Nexus"
if not exist "D:\Nexus\TestFiles" mkdir "D:\Nexus\TestFiles"

REM File 1
set "FILE1=D:\AIArm\Test\nexus_test_1.txt"
echo Creating test file 1: %FILE1%
echo This is test file 1 created by Nexus AI on %date% at %time%. > "%FILE1%"
echo This file demonstrates that Nexus AI has filesystem capabilities. >> "%FILE1%"
echo.

REM File 2
set "FILE2=D:\AIArm\Test\nexus_test_2.txt"
echo Creating test file 2: %FILE2%
echo This is test file 2 created by Nexus AI on %date% at %time%. > "%FILE2%"
echo This file contains different content to demonstrate writing capabilities. >> "%FILE2%"
echo.

REM File 3
set "FILE3=D:\Nexus\test_file.txt"
echo Creating test file 3: %FILE3%
echo This is test file 3 created by Nexus AI on %date% at %time%. > "%FILE3%"
echo This file is in a different directory to demonstrate path handling. >> "%FILE3%"
echo.

REM File 4
set "FILE4=D:\Nexus\TestFiles\test_data.txt"
echo Creating test file 4: %FILE4%
echo This is test file 4 created by Nexus AI on %date% at %time%. > "%FILE4%"
echo This file contains test data for the Nexus AI system. >> "%FILE4%"
echo Line 1: This is a test of multiline content. >> "%FILE4%"
echo Line 2: The system should be able to write multiple lines. >> "%FILE4%"
echo Line 3: This demonstrates more advanced file writing. >> "%FILE4%"
echo.

REM File 5
set "FILE5=%TEMP%\nexus_temp_test.txt"
echo Creating test file 5: %FILE5%
echo This is test file 5 created by Nexus AI on %date% at %time%. > "%FILE5%"
echo This file is in the system's temp directory to demonstrate writing to system paths. >> "%FILE5%"
echo.

echo All test files have been created successfully.
echo.

echo Summary of Created Files:
echo -------------------------
echo 1: %FILE1%
echo 2: %FILE2%
echo 3: %FILE3%
echo 4: %FILE4%
echo 5: %FILE5%
echo -------------------------
echo.

echo You can now view these files to verify that Nexus AI has filesystem capabilities.
echo.

pause