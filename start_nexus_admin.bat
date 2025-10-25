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

title Nexus AI - Administrator
echo Nexus AI - Administrator
echo ======================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

SET PORT=45678

echo Checking if port %PORT% is available...
netstat -ano | findstr ":%PORT% " > nul
if %errorlevel% equ 0 (
    echo Port %PORT% is already in use!
    echo Attempting to free the port...
    
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT% "') do (
        echo Killing process with PID %%a
        taskkill /f /pid %%a
        timeout /t 2 /nobreak > nul
    )
)

echo Setting up Nexus AI with Administrative Privileges...

REM Create necessary directories if they don't exist
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"
if not exist "D:\AIArm\Memory" mkdir "D:\AIArm\Memory"
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"

REM Create a test file to verify administrative access
echo This file confirms that Nexus AI has administrative privileges. > "D:\AIArm\Test\admin_test.txt"
echo Created on: %date% at %time% >> "D:\AIArm\Test\admin_test.txt"

echo Starting server on port %PORT% with administrative privileges...
cd /d "D:\AIArm\WebInterface"
node "real_server.js" --port %PORT% --bridge bridge_wrapper.py

echo.
echo Server terminated.
echo.
pause