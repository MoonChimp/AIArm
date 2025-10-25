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

title NexusAI:AlfaZer0 - SIMPLIFIED LAUNCHER
echo NexusAI:AlfaZer0 - SIMPLIFIED LAUNCHER
echo =====================================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

REM Create necessary directories if they don't exist
if not exist "D:\NexusAI" mkdir "D:\NexusAI"
if not exist "D:\NexusAI\Scripts" mkdir "D:\NexusAI\Scripts"
if not exist "D:\NexusAI\Knowledge" mkdir "D:\NexusAI\Knowledge"
if not exist "D:\NexusAI\Modules" mkdir "D:\NexusAI\Modules"
if not exist "D:\NexusAI\UserData" mkdir "D:\NexusAI\UserData"
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"

REM Create a test file to verify administrative access
echo This file confirms that NexusAI:AlfaZer0 has administrative privileges. > "D:\AIArm\Test\alfazer0_launcher_test.txt"
echo Created on: %date% at %time% >> "D:\AIArm\Test\alfazer0_launcher_test.txt"

REM Create environment variables
set "PORT=45678"

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

echo =======================================================
echo IMPORTANT: No need to use Ollama for this version!
echo This launcher directly connects to the server without
echo requiring Ollama to be running.
echo =======================================================
echo.

REM Create a special test file to demonstrate filesystem capabilities
echo Creating test file with administrative privileges...
echo This file was created by the AlfaZer0 launcher with administrative privileges. > "D:\AIArm\Test\alfazer0_filesystem_test.txt"
echo Created on: %date% at %time% >> "D:\AIArm\Test\alfazer0_filesystem_test.txt"
echo System information: >> "D:\AIArm\Test\alfazer0_filesystem_test.txt"
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Manufacturer" >> "D:\AIArm\Test\alfazer0_filesystem_test.txt"

echo Test file created at: D:\AIArm\Test\alfazer0_filesystem_test.txt
echo.

cd /d "D:\AIArm\WebInterface"

echo Starting the NexusAI:AlfaZer0 server with full admin capabilities...
echo.

echo Starting the server WITHOUT Ollama dependency...
node "real_server.js" --port %PORT% --bridge alfazer0_bridge.py

echo.
echo Server stopped. Press any key to exit...
pause > nul
