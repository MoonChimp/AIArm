@echo off
:: Admin bridge script for Nexus AI
:: Automatically elevates privileges when needed

:: Check for admin rights and elevate if needed
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "%*", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B
) else (
    goto gotAdmin
)

:gotAdmin
    if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs"
    pushd "%CD%"
    CD /D "%~dp0"

:: Get operation type and parameters
set operation=%~1
set param1=%~2
set param2=%~3

:: Execute the requested operation
if "%operation%"=="write" goto :write_file
if "%operation%"=="read" goto :read_file
if "%operation%"=="list" goto :list_directory
if "%operation%"=="mkdir" goto :create_directory
if "%operation%"=="delete" goto :delete_file
if "%operation%"=="execute" goto :execute_command
goto :error

:write_file
    echo %param2% > "%param1%"
    if %errorlevel% equ 0 (
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"Failed to write file","path":"%param1%"}
    )
    goto :end

:read_file
    if exist "%param1%" (
        type "%param1%"
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"File not found","path":"%param1%"}
    )
    goto :end

:list_directory
    echo {"success":true,"path":"%param1%","items":[
    for /f "delims=" %%i in ('dir /b "%param1%"') do (
        if exist "%param1%\%%i\" (
            echo {"name":"%%i","type":"directory"},
        ) else (
            echo {"name":"%%i","type":"file"},
        )
    )
    echo {}]}
    goto :end

:create_directory
    mkdir "%param1%" 2>nul
    if %errorlevel% equ 0 (
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"Failed to create directory","path":"%param1%"}
    )
    goto :end

:delete_file
    del "%param1%" 2>nul
    if %errorlevel% equ 0 (
        echo {"success":true,"path":"%param1%"}
    ) else (
        echo {"success":false,"error":"Failed to delete file","path":"%param1%"}
    )
    goto :end

:execute_command
    %param1%
    echo {"success":true,"command":"%param1%"}
    goto :end

:error
    echo {"success":false,"error":"Invalid operation","operation":"%operation%"}
    goto :end

:end
    exit /b