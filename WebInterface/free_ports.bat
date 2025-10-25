@echo off
echo =====================================================================
echo                    AIArm Port Cleaner Utility
echo =====================================================================
echo.

echo This utility will check for processes using the ports needed by AIArm
echo and offer to terminate them to free up the ports.
echo.

:: Check if running with administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: This script is not running with administrator privileges.
    echo Some processes may not be able to be terminated.
    echo Consider running this script as administrator.
    echo.
)

:: Check each port used by AIArm
set PORTS=3000 3100 3200 8000 8080 45678 45679 45680

for %%p in (%PORTS%) do (
    echo Checking port %%p...
    
    :: Find process using the port
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r "0.0.0.0:%%p .*:%%p"') do (
        set PID=%%a
        
        :: Get process name
        for /f "tokens=1" %%b in ('tasklist /fi "PID eq %%a" /nh') do (
            set PROCESS_NAME=%%b
            
            echo Port %%p is in use by !PROCESS_NAME! (PID: !PID!)
            
            set /p TERMINATE=Do you want to terminate this process? (Y/N): 
            
            if /i "!TERMINATE!"=="Y" (
                echo Attempting to terminate process !PID!...
                taskkill /F /PID !PID!
                
                if !errorlevel! equ 0 (
                    echo Process terminated successfully.
                ) else (
                    echo Failed to terminate process. You may need administrator privileges.
                )
            ) else (
                echo Process not terminated.
            )
        )
    )
)

echo.
echo Port check complete.
echo Run 'python check_ports.py' to verify port availability.
echo.

pause
