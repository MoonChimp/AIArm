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

title NexusAI:AlfaZer0 - Web Interface
echo NexusAI:AlfaZer0 - Web Interface
echo ===============================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

set "MODEL_NAME=nexusai:alfazer0"
set "PORT=45678"

REM Create directories if they don't exist
if not exist "D:\NexusAI" mkdir "D:\NexusAI"
if not exist "D:\NexusAI\Scripts" mkdir "D:\NexusAI\Scripts"
if not exist "D:\NexusAI\Knowledge" mkdir "D:\NexusAI\Knowledge"
if not exist "D:\NexusAI\Modules" mkdir "D:\NexusAI\Modules"
if not exist "D:\NexusAI\UserData" mkdir "D:\NexusAI\UserData"
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"

REM Create a test file to verify administrative access
echo This file confirms that NexusAI:AlfaZer0 has administrative privileges. > "D:\AIArm\Test\alfazer0_admin_test.txt"
echo Created on: %date% at %time% >> "D:\AIArm\Test\alfazer0_admin_test.txt"

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

echo Setting environment variable for Ollama model...
setx OLLAMA_MODEL %MODEL_NAME%

echo Starting Nexus web interface with NexusAI:AlfaZer0...
cd /d "D:\AIArm\WebInterface"

echo Running with administrative filesystem access...
node "real_server.js" --port %PORT% --bridge bridge_wrapper.py --model %MODEL_NAME%

echo.
echo Server stopped. Press any key to exit...
pause > nul
