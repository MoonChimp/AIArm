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

title NexusAI:AlfaZer0 - DIRECT INTEGRATION
echo NexusAI:AlfaZer0 - DIRECT INTEGRATION
echo ================================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

set "MODEL_NAME=nexusai:alfazer0"
set "PORT=45678"

REM Create necessary directories if they don't exist
if not exist "D:\NexusAI" mkdir "D:\NexusAI"
if not exist "D:\NexusAI\Scripts" mkdir "D:\NexusAI\Scripts"
if not exist "D:\NexusAI\Knowledge" mkdir "D:\NexusAI\Knowledge"
if not exist "D:\NexusAI\Modules" mkdir "D:\NexusAI\Modules"
if not exist "D:\NexusAI\UserData" mkdir "D:\NexusAI\UserData"
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"
if not exist "D:\AIArm\Test" mkdir "D:\AIArm\Test"

REM Create a test file to verify administrative access
echo This file confirms that NexusAI:AlfaZer0 has administrative privileges. > "D:\AIArm\Test\alfazer0_direct_test.txt"
echo Created on: %date% at %time% >> "D:\AIArm\Test\alfazer0_direct_test.txt"

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

echo Setting environment variables for direct bridge integration...
set OLLAMA_MODEL=%MODEL_NAME%
set NEXUSAI_BRIDGE=alfazer0_bridge.py

echo Starting Nexus web interface with NexusAI:AlfaZer0 DIRECT integration...
cd /d "D:\AIArm\WebInterface"

echo Modifying server.js to use direct bridge...
python -c "
import re
with open('real_server.js', 'r') as f:
    content = f.read()
# Modify to call alfazer0_bridge.py directly
content = re.sub(r'bridge_wrapper\.py', r'alfazer0_bridge.py', content)
with open('real_server.js', 'w') as f:
    f.write(content)
print('Modified server.js to use alfazer0_bridge.py')
"

echo Running with administrative filesystem access...
echo ** This is a DIRECT INTEGRATION - all file operations will be performed with admin rights **
echo.

echo Creating a direct connection to the Python bridge...
echo {\"operation\": \"write_file\", \"path\": \"D:/AIArm/Test/direct_integration_test.txt\", \"content\": \"Direct integration test from AlfaZer0 - %date% %time%\"} | python alfazer0_bridge.py
echo.

echo Starting the server with direct integration...
node "real_server.js" --port %PORT% --bridge alfazer0_bridge.py --model %MODEL_NAME%

echo.
echo Server stopped. Press any key to exit...
pause > nul
