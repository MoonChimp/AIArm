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

title Nexus AI - File Creator with Full Privileges
echo Nexus AI - File Creator with Full Privileges
echo ============================================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

:: Set target file path
set "TARGET_FILE=D:\AIArm\Test\nexus_admin_test.txt"
set "TARGET_DIR=D:\AIArm\Test"

:: Create directory if it doesn't exist
if not exist "%TARGET_DIR%" (
    echo Creating directory: %TARGET_DIR%
    mkdir "%TARGET_DIR%"
)

:: Create content
echo Creating test file with administrative privileges...
echo.

:: Write content to file
(
echo This file was created by Nexus AI with administrative privileges.
echo Created on: %date% at %time%
echo.
echo This file demonstrates that Nexus has FULL ACCESS to the system.
echo If you can read this file, the system has been properly configured with administrative access.
echo.
echo System Information:
echo ------------------
echo Computer Name: %COMPUTERNAME%
echo Username: %USERNAME%
echo Windows Directory: %WINDIR%
) > "%TARGET_FILE%"

:: Check if file was created successfully
if exist "%TARGET_FILE%" (
    echo SUCCESS: Test file created at %TARGET_FILE%
    echo.
    echo File contents:
    echo --------------
    type "%TARGET_FILE%"
    echo --------------
) else (
    echo ERROR: Failed to create test file.
)

echo.
echo Process complete.
pause