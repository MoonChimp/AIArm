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

title NexusAI:AlfaZer0 - Builder and Launcher
echo NexusAI:AlfaZer0 - Builder and Launcher
echo =====================================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

set "MODEL_DIR=D:\AIArm\NexusAI-AlfaZer0"
set "MODEL_NAME=nexusai:alfazer0"
set "OLLAMA_PATH=C:\Program Files\Ollama"

echo Checking for Ollama installation...
if not exist "%OLLAMA_PATH%\ollama.exe" (
    echo Ollama not found at %OLLAMA_PATH%
    set /p OLLAMA_PATH="Please enter the path to your Ollama installation: "
)

if not exist "%OLLAMA_PATH%\ollama.exe" (
    echo Ollama executable not found! Please install Ollama first.
    pause
    exit /b 1
)

echo Checking for nexusai:latest model...
"%OLLAMA_PATH%\ollama.exe" list | find "nexusai:latest" > nul
if %errorlevel% neq 0 (
    echo The base model 'nexusai:latest' was not found.
    echo Please pull the base model first by running: ollama pull nexusai:latest
    echo.
    choice /C YN /M "Do you want to try pulling nexusai:latest now?"
    if %errorlevel% equ 1 (
        echo Pulling nexusai:latest model...
        "%OLLAMA_PATH%\ollama.exe" pull nexusai:latest
        if %errorlevel% neq 0 (
            echo Failed to pull the base model. Please check your internet connection and try again.
            pause
            exit /b 1
        )
    ) else (
        echo Operation canceled.
        pause
        exit /b 1
    )
)

echo.
echo Creating necessary directories for NexusAI:AlfaZer0...
if not exist "D:\NexusAI" mkdir "D:\NexusAI"
if not exist "D:\NexusAI\Scripts" mkdir "D:\NexusAI\Scripts"
if not exist "D:\NexusAI\Knowledge" mkdir "D:\NexusAI\Knowledge"
if not exist "D:\NexusAI\Modules" mkdir "D:\NexusAI\Modules"
if not exist "D:\NexusAI\UserData" mkdir "D:\NexusAI\UserData"

echo.
echo Creating initial index file...
echo { "version": "1.0", "created": "%date% %time%", "scripts": [], "modules": [], "capabilities": [] } > "D:\NexusAI\index.json"

echo.
echo Building NexusAI:AlfaZer0 model...
cd /d "%MODEL_DIR%"
"%OLLAMA_PATH%\ollama.exe" create %MODEL_NAME% -f Modelfile

if %errorlevel% neq 0 (
    echo Failed to create the model. Please check the Modelfile for errors.
    pause
    exit /b 1
)

echo.
echo Model created successfully!
echo.

:menu
echo.
echo NexusAI:AlfaZer0 - Main Menu
echo ==========================
echo 1. Run NexusAI:AlfaZer0 in terminal
echo 2. Run NexusAI:AlfaZer0 with Nexus Web Interface
echo 3. View model information
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    cls
    echo Running NexusAI:AlfaZer0 in terminal...
    echo Type 'exit' to return to the menu.
    echo.
    "%OLLAMA_PATH%\ollama.exe" run %MODEL_NAME%
    goto menu
) else if "%choice%"=="2" (
    cls
    echo Running NexusAI:AlfaZer0 with Nexus Web Interface...
    echo.
    
    set "NEXUS_PORT=45678"
    echo Setting environment variable for Nexus...
    setx OLLAMA_MODEL %MODEL_NAME%
    
    echo Starting Nexus server...
    start "Nexus Server" cmd /c "cd /d D:\AIArm\WebInterface && node real_server.js --port %NEXUS_PORT% --bridge bridge_wrapper.py --model %MODEL_NAME%"
    
    timeout /t 3 /nobreak > nul
    
    echo Opening Nexus interface in your browser...
    start http://localhost:%NEXUS_PORT%/real_interface.html
    
    echo.
    echo Press any key to return to the menu (this will not stop the server)...
    pause > nul
    goto menu
) else if "%choice%"=="3" (
    cls
    echo NexusAI:AlfaZer0 Model Information:
    echo ================================
    echo.
    "%OLLAMA_PATH%\ollama.exe" show %MODEL_NAME%
    echo.
    pause
    goto menu
) else if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    goto menu
)
