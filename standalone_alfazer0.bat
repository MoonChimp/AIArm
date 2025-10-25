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

title AlfaZer0 - Standalone
echo AlfaZer0 - Standalone
echo =====================
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
echo This file confirms that AlfaZer0 has administrative privileges. > "D:\AIArm\Test\alfazer0_standalone_test.txt"
echo Created on: %date% at %time% >> "D:\AIArm\Test\alfazer0_standalone_test.txt"

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
echo NOTICE: This is the standalone version of AlfaZer0
echo that doesn't require Ollama or any other external dependencies.
echo It will directly use the administrative filesystem capabilities.
echo =======================================================
echo.

REM Test the admin bridge
echo Testing administrative bridge...
cd /d "D:\AIArm\WebInterface"
echo {"operation":"write_file","path":"D:/AIArm/Test/bridge_test.txt","content":"Bridge test successful!"} | python alfazer0_bridge.py > bridge_test_result.json

echo Checking if bridge test was successful...
type bridge_test_result.json | findstr "success" > nul
if %errorlevel% equ 0 (
    echo Bridge test successful! File created at D:\AIArm\Test\bridge_test.txt
) else (
    echo Bridge test failed. Please check the logs.
    type bridge_test_result.json
)
echo.

echo Starting the server with standalone bridge...
node "real_server.js" --port %PORT% --bridge standalone_bridge.py

echo.
echo Server stopped. Press any key to exit...
pause > nul
