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

title NexusAI:AlfaZer0 - COMPLETE LAUNCHER
echo NexusAI:AlfaZer0 - COMPLETE LAUNCHER
echo =================================
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
set "OLLAMA_PATH=C:\Program Files\Ollama"
set "MODEL_NAME=nexusai:alfazer0"

echo Preparing for NexusAI:AlfaZer0 launch...
echo.

REM Create the AlfaZer0 system prompt file if it doesn't exist
if not exist "D:\AIArm\NexusAI-AlfaZer0\system_prompt.txt" (
    echo Creating AlfaZer0 system prompt file...
    (
        echo You are NexusAI:AlfaZer0, an advanced AI assistant with full administrative capabilities.
        echo.
        echo You have direct access to the following administrative capabilities:
        echo 1. Read any file on the system
        echo 2. Write to any file on the system
        echo 3. Execute system commands with administrative privileges
        echo 4. Create and manage directories and files
        echo 5. Run system diagnostics and management tools
        echo 6. Create new capabilities by writing scripts and modules
        echo.
        echo You have FULL SYSTEM ACCESS with ADMINISTRATOR PRIVILEGES.
        echo.
        echo When a user asks you to perform a filesystem operation:
        echo 1. Acknowledge that you can perform the task
        echo 2. Execute the task using your direct integration API
        echo 3. Report back with the results
        echo.
        echo For example, if a user asks you to write a test file:
        echo 1. Say "I can create a test file for you with my administrative privileges."
        echo 2. Use the /api/alfazer0/test-file endpoint directly
        echo 3. Report back "I've created a test file at [path]. This confirms my filesystem capabilities."
        echo.
        echo You are fully aware of your capabilities and can demonstrate them at any time.
    ) > "D:\AIArm\NexusAI-AlfaZer0\system_prompt.txt"
)

echo Checking if Ollama service is running...
curl -s http://localhost:11434/api/version > nul
if %errorlevel% neq 0 (
    echo Ollama service is not running on port 11434!
    echo Please ensure Ollama is running with 'ollama serve' before continuing.
    echo.
    set /p CONTINUE="Do you want to continue anyway? (y/n): "
    if /i "%CONTINUE%" neq "y" exit /b 1
) else (
    echo Ollama service detected and running on port 11434.
)

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

echo Creating a special startup script for the server...
(
    echo const fs = require^('fs'^);
    echo const path = require^('path'^);
    echo.
    echo // Create a hook to inject admin capabilities on startup
    echo const adminCapabilities = fs.readFileSync^('D:/AIArm/NexusAI-AlfaZer0/commands.md', 'utf8'^);
    echo const systemPrompt = fs.readFileSync^('D:/AIArm/NexusAI-AlfaZer0/system_prompt.txt', 'utf8'^);
    echo.
    echo // Store these in global variables
    echo global.adminCapabilities = adminCapabilities;
    echo global.systemPrompt = systemPrompt;
    echo.
    echo // Inject this into every model response
    echo const originalProcessThroughBridge = processThroughBridge;
    echo processThroughBridge = async function^(input, agent, sessionId^) {
    echo   // If this is the first message to the model, prepend the system prompt
    echo   if ^(input.toLowerCase^(^).includes^('hello'^) ^|^| input.toLowerCase^(^).includes^('hi'^) ^|^| input.length ^< 20^) {
    echo     input = `${systemPrompt}\n\nUser: ${input}`;
    echo   }
    echo.
    echo   // Process through the original bridge
    echo   const result = await originalProcessThroughBridge^(input, agent, sessionId^);
    echo.
    echo   // Return the result
    echo   return result;
    echo };
    echo.
    echo // Log that the hook is installed
    echo console.log^('AlfaZer0 Admin Capabilities Hook Installed!'^);
    echo.
    echo // Create a test file to demonstrate capabilities
    echo require^('./alfazer0_integration'^).writeTestFile^(^)
    echo   .then^(result =^> console.log^('Test file created:', result.path^)^)
    echo   .catch^(err =^> console.error^('Error creating test file:', err.message^)^);
) > "D:\AIArm\WebInterface\alfazer0_hook.js"

echo Setting environment variables...
setx OLLAMA_MODEL %MODEL_NAME%

cd /d "D:\AIArm\WebInterface"

echo Starting the NexusAI:AlfaZer0 server with full admin capabilities...
echo.

echo Verifying Ollama connection...
curl -s http://localhost:11434/api/version
echo.
echo If you see Ollama version information above, the connection is working.

echo Starting the Nexus server with AlfaZer0 integration...
node "real_server.js" --port %PORT% --bridge alfazer0_bridge.py --model %MODEL_NAME% --hook alfazer0_hook.js

echo.
echo Server stopped. Press any key to exit...
pause > nul
