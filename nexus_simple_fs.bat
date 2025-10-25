@echo off
title Nexus AI - Simple Filesystem Demo
echo Nexus AI - Simple Filesystem Demo
echo ==================================
echo.

REM Check if we have a command-line argument
if "%~1"=="" goto :menu

REM Handle different commands
if /i "%~1"=="write" goto :write_file
if /i "%~1"=="read" goto :read_file
if /i "%~1"=="list" goto :list_dir
goto :menu

:menu
echo Choose an operation:
echo.
echo 1. Write a test file
echo 2. Read a file
echo 3. List directory contents
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto :write_menu
if "%choice%"=="2" goto :read_menu
if "%choice%"=="3" goto :list_menu
if "%choice%"=="4" goto :end
goto :menu

:write_menu
echo.
echo Write a Test File
echo ================
set /p filename="Enter filename (default: nexus_test.txt): "
if "%filename%"=="" set filename=nexus_test.txt
goto :do_write

:do_write
echo.
echo Creating test file: %filename%
echo This is a test file created by Nexus AI on %date% at %time%. > "%filename%"
echo This file demonstrates the filesystem capabilities of the Nexus AI system. >> "%filename%"
echo If you can read this file, the test was successful! >> "%filename%"
echo.
echo File created successfully!
echo.
echo Contents:
echo ---------
type "%filename%"
echo ---------
echo.
goto :continue

:read_menu
echo.
echo Read a File
echo ===========
set /p filename="Enter filename to read: "
if "%filename%"=="" goto :read_menu
goto :do_read

:do_read
echo.
if not exist "%filename%" (
    echo Error: File does not exist!
    goto :continue
)
echo Contents of %filename%:
echo -----------------------
type "%filename%"
echo -----------------------
echo.
goto :continue

:list_menu
echo.
echo List Directory Contents
echo ======================
set /p dirname="Enter directory path (default: current): "
if "%dirname%"=="" set dirname=.
goto :do_list

:do_list
echo.
if not exist "%dirname%\" (
    echo Error: Directory does not exist!
    goto :continue
)
echo Contents of directory: %dirname%
echo ------------------------------
dir /b "%dirname%"
echo ------------------------------
echo.
goto :continue

:write_file
if "%~2"=="" (
    echo Error: No filename specified
    goto :usage
)
echo Creating file: %~2
echo %~3 > "%~2"
echo File created successfully!
goto :end

:read_file
if "%~2"=="" (
    echo Error: No filename specified
    goto :usage
)
if not exist "%~2" (
    echo Error: File does not exist: %~2
    goto :end
)
echo Contents of %~2:
echo -----------------
type "%~2"
echo -----------------
goto :end

:list_dir
if "%~2"=="" (
    set dirname=.
) else (
    set dirname=%~2
)
if not exist "%dirname%\" (
    echo Error: Directory does not exist: %dirname%
    goto :end
)
echo Contents of directory: %dirname%
echo --------------------------
dir /b "%dirname%"
echo --------------------------
goto :end

:usage
echo Usage:
echo   nexus_simple_fs write [filename] [content]
echo   nexus_simple_fs read [filename]
echo   nexus_simple_fs list [directory]
echo.
echo Examples:
echo   nexus_simple_fs write test.txt "Hello, world!"
echo   nexus_simple_fs read test.txt
echo   nexus_simple_fs list D:\
goto :end

:continue
echo.
echo Press any key to return to menu...
pause > nul
cls
goto :menu

:end
echo.
echo Thank you for using Nexus AI Filesystem Demo
echo.