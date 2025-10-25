@echo off
setlocal enabledelayedexpansion

title NexusAI - Complete Startup System
echo NexusAI - Complete Startup System
echo ================================
echo.

:: Set colors for better readability
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "MAGENTA=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "RESET=[0m"

:: Configuration
set "OLLAMA_PORT=11434"
set "NEXUS_PORT=45678"
set "OLLAMA_EXE=ollama.exe"
set "OLLAMA_PATH="

:: Models to ensure are available (add more as needed)
set "MODELS=llama3,codellama,mistral,nexusai:alfazer0"

:: Check for admin rights and elevate if needed
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo %YELLOW%Requesting administrative privileges...%RESET%
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

:: Create necessary directories
if not exist "D:\AIArm\Logs" mkdir "D:\AIArm\Logs"
if not exist "D:\AIArm\Temp" mkdir "D:\AIArm\Temp"

:: Log file setup
set "LOG_FILE=D:\AIArm\Logs\nexusai_startup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log"
set "LOG_FILE=%LOG_FILE: =0%"

:: Function to log messages
:log
echo %~1
echo [%date% %time%] %~1 >> "%LOG_FILE%"
goto :eof

:: Function to check if a process is running by name
:isProcessRunning
set "PROCESS_NAME=%~1"
set "IS_RUNNING=false"
tasklist /FI "IMAGENAME eq %PROCESS_NAME%" 2>nul | find /I "%PROCESS_NAME%" >nul
if %errorlevel% equ 0 set "IS_RUNNING=true"
goto :eof

:: Function to check if port is in use
:isPortInUse
set "PORT=%~1"
set "PORT_IN_USE=false"
netstat -ano | findstr ":%PORT% " >nul
if %errorlevel% equ 0 set "PORT_IN_USE=true"
goto :eof

:: Find Ollama installation
echo %CYAN%Finding Ollama installation...%RESET%
call :log "Finding Ollama installation..."

:: Check standard locations
set "POSSIBLE_PATHS=C:\Program Files\Ollama;C:\Ollama;%USERPROFILE%\AppData\Local\Programs\Ollama;%USERPROFILE%\Ollama"
for %%p in (%POSSIBLE_PATHS%) do (
    if exist "%%p\%OLLAMA_EXE%" (
        set "OLLAMA_PATH=%%p"
        call :log "Found Ollama at: %%p"
        goto :foundOllama
    )
)

:: Check PATH environment variable
for /f "tokens=*" %%i in ('where ollama 2^>nul') do (
    set "OLLAMA_PATH=%%~dpi"
    call :log "Found Ollama in PATH: %%i"
    goto :foundOllama
)

:foundOllama
if "%OLLAMA_PATH%"=="" (
    echo %RED%Ollama installation not found!%RESET%
    call :log "Ollama installation not found!"
    
    echo.
    echo %YELLOW%Would you like to download and install Ollama now?%RESET%
    set /p INSTALL_OLLAMA="Enter y/n: "
    if /i "%INSTALL_OLLAMA%"=="y" (
        call :downloadOllama
    ) else (
        echo %RED%Cannot proceed without Ollama. Exiting...%RESET%
        call :log "User chose not to install Ollama. Exiting."
        exit /b 1
    )
) else (
    echo %GREEN%Found Ollama at: %OLLAMA_PATH%%RESET%
)

:: Function to download and install Ollama
:downloadOllama
echo %CYAN%Downloading Ollama installer...%RESET%
call :log "Downloading Ollama installer..."

:: Set download URL and path
set "DOWNLOAD_URL=https://ollama.com/download/ollama-installer.exe"
set "INSTALLER_PATH=D:\AIArm\Temp\ollama-installer.exe"

:: Download the installer
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%INSTALLER_PATH%'"
if %errorlevel% neq 0 (
    echo %RED%Failed to download Ollama installer!%RESET%
    call :log "Failed to download Ollama installer!"
    exit /b 1
)

:: Run the installer
echo %CYAN%Running Ollama installer...%RESET%
call :log "Running Ollama installer..."
start /wait "" "%INSTALLER_PATH%"

:: Check if installation was successful
call :isProcessRunning "ollama.exe"
if "%IS_RUNNING%"=="true" (
    echo %GREEN%Ollama installed successfully!%RESET%
    call :log "Ollama installed successfully!"
    
    :: Try to find the installation path
    for /f "tokens=*" %%i in ('where ollama 2^>nul') do (
        set "OLLAMA_PATH=%%~dpi"
        call :log "Found newly installed Ollama in PATH: %%i"
        goto :ollamaInstalled
    )
) else (
    :: Check standard locations again
    for %%p in (%POSSIBLE_PATHS%) do (
        if exist "%%p\%OLLAMA_EXE%" (
            set "OLLAMA_PATH=%%p"
            call :log "Found newly installed Ollama at: %%p"
            goto :ollamaInstalled
        )
    )
)

echo %RED%Could not find Ollama installation after install!%RESET%
call :log "Could not find Ollama installation after install!"
exit /b 1

:ollamaInstalled
goto :checkOllamaRunning

:: Check if Ollama is already running
:checkOllamaRunning
echo %CYAN%Checking if Ollama is already running...%RESET%
call :log "Checking if Ollama is already running..."

:: Check if the port is in use
call :isPortInUse %OLLAMA_PORT%

if "%PORT_IN_USE%"=="true" (
    echo %YELLOW%Ollama port %OLLAMA_PORT% is in use.%RESET%
    call :log "Ollama port %OLLAMA_PORT% is in use."
    
    :: Check if it's actually Ollama
    for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%OLLAMA_PORT% "') do (
        set "PROCESS_PID=%%p"
        for /f "tokens=1" %%n in ('tasklist /FI "PID eq %%p" ^| findstr /v "PID"') do (
            if "%%n"=="%OLLAMA_EXE%" (
                set "IS_OLLAMA=true"
                call :log "Confirmed process on port %OLLAMA_PORT% is Ollama (PID: %%p)"
            ) else (
                set "IS_OLLAMA=false"
                set "OTHER_PROCESS=%%n"
                call :log "Port %OLLAMA_PORT% is used by another process: %%n (PID: %%p)"
            )
        )
    )
    
    if "%IS_OLLAMA%"=="true" (
        echo %GREEN%Ollama is running.%RESET%
        
        echo.
        echo %YELLOW%Would you like to restart Ollama to ensure a clean state?%RESET%
        set /p RESTART_OLLAMA="Enter y/n: "
        if /i "%RESTART_OLLAMA%"=="y" (
            echo %CYAN%Stopping Ollama...%RESET%
            call :log "Stopping Ollama..."
            
            taskkill /F /IM "%OLLAMA_EXE%" /T >nul 2>&1
            timeout /t 2 /nobreak >nul
            
            goto :startOllama
        ) else (
            echo %GREEN%Continuing with existing Ollama process.%RESET%
            call :log "Continuing with existing Ollama process."
            goto :checkOllamaConnection
        )
    ) else (
        echo %RED%Port %OLLAMA_PORT% is in use by another process: %OTHER_PROCESS%%RESET%
        call :log "Port %OLLAMA_PORT% is in use by another process: %OTHER_PROCESS%"
        
        echo.
        echo %YELLOW%Would you like to terminate this process and start Ollama?%RESET%
        set /p KILL_PROCESS="Enter y/n: "
        if /i "%KILL_PROCESS%"=="y" (
            echo %CYAN%Terminating process...%RESET%
            call :log "Terminating process PID: %PROCESS_PID%"
            
            taskkill /F /PID "%PROCESS_PID%" /T >nul 2>&1
            timeout /t 2 /nobreak >nul
            
            goto :startOllama
        ) else (
            echo %RED%Cannot start Ollama while port %OLLAMA_PORT% is in use. Exiting...%RESET%
            call :log "User chose not to terminate the conflicting process. Exiting."
            exit /b 1
        )
    )
) else (
    echo %CYAN%Ollama is not running.%RESET%
    call :log "Ollama is not running."
    goto :startOllama
)

:: Start Ollama
:startOllama
echo %CYAN%Starting Ollama...%RESET%
call :log "Starting Ollama..."

if "%OLLAMA_PATH%"=="" (
    :: Try to start from PATH
    start "" /b cmd /c "ollama serve > D:\AIArm\Logs\ollama.log 2>&1"
) else (
    :: Start from known location
    start "" /b cmd /c "cd /d "%OLLAMA_PATH%" && ollama serve > D:\AIArm\Logs\ollama.log 2>&1"
)

echo %CYAN%Waiting for Ollama to initialize...%RESET%
call :log "Waiting for Ollama to initialize..."
timeout /t 5 /nobreak >nul

:: Verify Ollama is running
:checkOllamaConnection
echo %CYAN%Verifying Ollama connection...%RESET%
call :log "Verifying Ollama connection..."

set "RETRY_COUNT=0"
set "MAX_RETRIES=5"

:checkConnection
set /a RETRY_COUNT+=1

curl -s http://localhost:%OLLAMA_PORT%/api/version >nul
if %errorlevel% equ 0 (
    echo %GREEN%Successfully connected to Ollama!%RESET%
    call :log "Successfully connected to Ollama!"
    goto :checkModels
) else (
    if %RETRY_COUNT% lss %MAX_RETRIES% (
        echo %YELLOW%Could not connect to Ollama. Retrying in 2 seconds... (Attempt %RETRY_COUNT%/%MAX_RETRIES%)%RESET%
        call :log "Could not connect to Ollama. Retrying... (Attempt %RETRY_COUNT%/%MAX_RETRIES%)"
        timeout /t 2 /nobreak >nul
        goto :checkConnection
    ) else (
        echo %RED%Failed to connect to Ollama after %MAX_RETRIES% attempts!%RESET%
        call :log "Failed to connect to Ollama after %MAX_RETRIES% attempts!"
        
        echo.
        echo %YELLOW%Would you like to continue without Ollama verification?%RESET%
        set /p CONTINUE_ANYWAY="Enter y/n: "
        if /i "%CONTINUE_ANYWAY%"=="y" (
            echo %YELLOW%Continuing without Ollama verification...%RESET%
            call :log "Continuing without Ollama verification..."
            goto :startNexus
        ) else (
            echo %RED%Exiting...%RESET%
            call :log "User chose not to continue without Ollama verification. Exiting."
            exit /b 1
        )
    )
)

:: Check and pull required models
:checkModels
echo %CYAN%Checking available models...%RESET%
call :log "Checking available models..."

:: Get list of available models
curl -s http://localhost:%OLLAMA_PORT%/api/tags > D:\AIArm\Temp\models.json
if %errorlevel% neq 0 (
    echo %YELLOW%Could not get list of models. Will attempt to pull required models anyway.%RESET%
    call :log "Could not get list of models. Will attempt to pull required models anyway."
) else (
    echo %GREEN%Successfully retrieved list of models!%RESET%
    call :log "Successfully retrieved list of models!"
)

:: Parse the list to find which models we need to pull
for %%m in (%MODELS%) do (
    set "MODEL_NAME=%%m"
    set "MODEL_EXISTS=false"
    
    :: Check if model exists in the models.json file
    type D:\AIArm\Temp\models.json | findstr /C:"""name"": ""%%m""" >nul
    if %errorlevel% equ 0 (
        set "MODEL_EXISTS=true"
        echo %GREEN%Model %%m is already available.%RESET%
        call :log "Model %%m is already available."
    ) else (
        echo %YELLOW%Model %%m is not available. Pulling...%RESET%
        call :log "Model %%m is not available. Pulling..."
        
        :: Pull the model
        start /wait "" cmd /c "ollama pull %%m"
        
        :: Verify the model was pulled
        curl -s http://localhost:%OLLAMA_PORT%/api/tags | findstr /C:"""name"": ""%%m""" >nul
        if %errorlevel% equ 0 (
            echo %GREEN%Successfully pulled model %%m!%RESET%
            call :log "Successfully pulled model %%m!"
        ) else (
            echo %YELLOW%Could not verify if model %%m was pulled. Continuing...%RESET%
            call :log "Could not verify if model %%m was pulled. Continuing..."
        )
    )
)

:: Check if Nexus server port is already in use
:checkNexusPort
echo %CYAN%Checking if Nexus port %NEXUS_PORT% is available...%RESET%
call :log "Checking if Nexus port %NEXUS_PORT% is available..."

call :isPortInUse %NEXUS_PORT%
if "%PORT_IN_USE%"=="true" (
    echo %YELLOW%Nexus port %NEXUS_PORT% is in use. Stopping the process...%RESET%
    call :log "Nexus port %NEXUS_PORT% is in use. Stopping the process..."
    
    for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%NEXUS_PORT% "') do (
        echo %CYAN%Terminating process with PID: %%p%RESET%
        call :log "Terminating process with PID: %%p"
        taskkill /f /pid %%p >nul 2>&1
    )
    
    timeout /t 2 /nobreak >nul
)

:: Start NexusAI
:startNexus
echo.
echo %CYAN%Starting NexusAI...%RESET%
call :log "Starting NexusAI..."

cd /d "%~dp0"

:: Get current date and time for logging
set "TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

:: Start the server with the direct Ollama bridge
echo %CYAN%Starting Node.js server with direct Ollama bridge...%RESET%
call :log "Starting Node.js server with direct Ollama bridge..."

:: Redirect output to log file
start "" cmd /c "node real_server.js --bridge direct_ollama_bridge.py > D:\AIArm\Logs\nexus_server_%TIMESTAMP%.log 2>&1"

:: Give the server a moment to start
timeout /t 3 /nobreak >nul

:: Check if server started successfully
curl -s http://localhost:%NEXUS_PORT%/api/status >nul
if %errorlevel% equ 0 (
    echo %GREEN%NexusAI server started successfully!%RESET%
    call :log "NexusAI server started successfully!"
) else (
    echo %YELLOW%Could not verify if NexusAI server started. It may still be initializing...%RESET%
    call :log "Could not verify if NexusAI server started. It may still be initializing..."
)

:: Open the interface in the default browser
echo %CYAN%Opening NexusAI interface in your browser...%RESET%
call :log "Opening NexusAI interface in browser..."
start "" "http://localhost:%NEXUS_PORT%/real_interface.html"

echo.
echo %GREEN%NexusAI startup complete!%RESET%
echo %CYAN%The system is now running at: http://localhost:%NEXUS_PORT%/real_interface.html%RESET%
echo %CYAN%Logs are available in: D:\AIArm\Logs%RESET%
echo.
echo %MAGENTA%Press any key to exit this startup script (the NexusAI server will continue running)%RESET%
call :log "NexusAI startup complete!"

pause >nul
exit /b 0