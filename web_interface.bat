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

title Web Interface - Direct File Operation
echo Web Interface - Direct File Operation
echo ==================================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

REM Make sure all required directories exist
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"

REM Kill any existing processes using port 45678
echo Checking if port 45678 is already in use...
netstat -ano | findstr ":45678" > nul
if %errorlevel% equ 0 (
    echo Port 45678 is in use. Killing the process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":45678"') do (
        echo Killing process with PID %%a
        taskkill /F /PID %%a
    )
    timeout /t 3 /nobreak > nul
)

REM Create a simple test file to confirm we have write access
echo Creating test file to confirm admin access...
echo This file was created by the web interface launcher at %date% %time% > "D:\AIArm\Test\web_launcher_test.txt"
echo.

echo Starting the web server with direct file creation capabilities...
cd /d "D:\AIArm\WebInterface"

REM Test the bridge directly
echo Testing the web bridge directly...
echo test | python web_bridge.py
echo.

REM Start the server with our simplified bridge
echo Starting web server on port 45678...
node "real_server.js" --port 45678 --bridge web_bridge.py

echo.
echo Server stopped. Press any key to exit...
pause > nul
