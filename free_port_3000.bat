@echo off
echo [1;36m=====================================================================[0m
echo [1;36m        AIArm Port Utility - Free Port 3000[0m
echo [1;36m=====================================================================[0m
echo.

echo [1;33mChecking if port 3000 is in use...[0m

:: Check if port 3000 is in use
netstat -ano | findstr :3000 > temp_ports.txt
set /p PORT_INFO=<temp_ports.txt
del temp_ports.txt

:: If port is in use, offer to kill the process
if not "%PORT_INFO%"=="" (
    echo [1;31mPort 3000 is currently in use![0m
    
    :: Extract PID
    for /f "tokens=5" %%a in ("%PORT_INFO%") do (
        set PID=%%a
    )
    
    echo Process ID: %PID%
    
    :: Get process name
    for /f "tokens=1" %%b in ('tasklist /fi "PID eq %PID%" /fo list ^| findstr "Image"') do (
        set PROC_INFO=%%b
    )
    
    echo Process: %PROC_INFO%
    
    echo.
    echo [1;33mWould you like to kill this process to free port 3000? (Y/N)[0m
    set /p KILL_PROCESS=
    
    if /i "%KILL_PROCESS%"=="Y" (
        echo [1;33mAttempting to kill process %PID%...[0m
        taskkill /F /PID %PID%
        
        if %errorlevel% equ 0 (
            echo [1;32mProcess successfully terminated. Port 3000 is now available.[0m
        ) else (
            echo [1;31mFailed to terminate process. You may need administrative privileges.[0m
            echo [1;33mTry running this script as Administrator or manually end the process.[0m
        )
    ) else (
        echo [1;33mPort 3000 remains in use. You can:[0m
        echo [1;33m1. Manually end the process using Task Manager[0m
        echo [1;33m2. Use a different port in the server configuration[0m
    )
) else (
    echo [1;32mPort 3000 is available and ready to use.[0m
)

echo.
pause
