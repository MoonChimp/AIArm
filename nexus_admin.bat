@echo off
:: Check for admin rights and elevate if needed
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    goto UACPrompt
) else (
    goto gotAdmin
)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs"
    pushd "%CD%"
    CD /D "%~dp0"

title Nexus AI - System Administrator
echo Nexus AI - System Administrator
echo ==============================
echo Running with ADMINISTRATIVE PRIVILEGES
echo.

:main_menu
cls
echo NEXUS SYSTEM ADMINISTRATOR
echo =========================
echo Running with administrative rights
echo.
echo Choose an operation:
echo 1. Write test file to system location
echo 2. Create directory in system location
echo 3. Run system command
echo 4. View system information
echo 5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto :write_test_file
if "%choice%"=="2" goto :create_directory
if "%choice%"=="3" goto :run_command
if "%choice%"=="4" goto :system_info
if "%choice%"=="5" goto :end
goto :main_menu

:write_test_file
cls
echo WRITE FILE TO SYSTEM LOCATION
echo ===========================
echo.
echo Available system locations:
echo 1. D:\AIArm\Test
echo 2. C:\Program Files
echo 3. C:\Windows\Temp
echo 4. Custom location
echo.
set /p location="Choose location (1-4): "

if "%location%"=="1" set "filepath=D:\AIArm\Test\nexus_admin_test.txt"
if "%location%"=="2" set "filepath=C:\Program Files\nexus_admin_test.txt"
if "%location%"=="3" set "filepath=C:\Windows\Temp\nexus_admin_test.txt"
if "%location%"=="4" (
    set /p filepath="Enter custom filepath: "
)

set "content=This file was created by Nexus AI with administrative privileges on %date% at %time%."

echo.
echo Writing to: %filepath%
echo.

echo %content% > "%filepath%" 2>nul

if %errorlevel% equ 0 (
    echo SUCCESS: File written successfully!
    echo.
    echo File contents:
    type "%filepath%"
) else (
    echo ERROR: Failed to write file. Error code: %errorlevel%
)

echo.
pause
goto :main_menu

:create_directory
cls
echo CREATE DIRECTORY IN SYSTEM LOCATION
echo ================================
echo.
echo Available system locations:
echo 1. D:\AIArm\
echo 2. C:\Program Files\
echo 3. C:\Windows\
echo 4. Custom location
echo.
set /p location="Choose location (1-4): "

if "%location%"=="1" set "basepath=D:\AIArm"
if "%location%"=="2" set "basepath=C:\Program Files"
if "%location%"=="3" set "basepath=C:\Windows"
if "%location%"=="4" (
    set /p basepath="Enter base path: "
)

set /p dirname="Enter directory name to create: "
set "dirpath=%basepath%\%dirname%"

echo.
echo Creating directory: %dirpath%
echo.

mkdir "%dirpath%" 2>nul

if %errorlevel% equ 0 (
    echo SUCCESS: Directory created successfully!
    dir "%basepath%" | findstr /I "%dirname%"
) else (
    echo ERROR: Failed to create directory. Error code: %errorlevel%
)

echo.
pause
goto :main_menu

:run_command
cls
echo RUN SYSTEM COMMAND
echo ================
echo.
echo WARNING: Commands will be executed with administrative privileges.
echo.
set /p cmd="Enter command to execute: "

echo.
echo Executing: %cmd%
echo.
echo --- Command output ---
%cmd%
echo --- End of output ---

echo.
pause
goto :main_menu

:system_info
cls
echo SYSTEM INFORMATION
echo ================
echo.
echo --- System ---
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Manufacturer" /C:"System Model" /C:"System Type" /C:"Total Physical Memory"
echo.
echo --- Disk Information ---
wmic logicaldisk get caption,description,freespace,size,volumename
echo.
echo --- Network Information ---
ipconfig | findstr /C:"IPv4 Address" /C:"Subnet Mask" /C:"Default Gateway"
echo.
pause
goto :main_menu

:end
echo.
echo Thank you for using Nexus System Administrator.
echo Exiting...
echo.