@echo off
title Nexus - Write Test File
echo Creating a test file to demonstrate filesystem capabilities...

set TIMESTAMP=%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

set TEST_FILE=D:\AIArm\test_file_%TIMESTAMP%.txt
set CONTENT=This is a test file created by Nexus AI on %date% at %time%.\n\nThis file demonstrates that Nexus has filesystem capabilities and can create files on your system.\n\nIf you can read this, the test was successful!

echo Writing to: %TEST_FILE%

python D:\AIArm\WebInterface\nexus_direct_fs.py --operation write --path "%TEST_FILE%" --content "%CONTENT%"

if %errorlevel% neq 0 (
    echo Failed to write test file!
    exit /b 1
)

echo Test file created successfully!
echo Path: %TEST_FILE%

type "%TEST_FILE%"

pause