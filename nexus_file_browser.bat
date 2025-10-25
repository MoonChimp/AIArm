@echo off
title Nexus AI - File Browser
echo Nexus AI - File Browser
echo ======================
echo.

:main_menu
cls
echo Choose an option:
echo ----------------
echo 1. Browse directories
echo 2. Read a file
echo 3. Write a new file
echo 4. Search for files
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto :browse
if "%choice%"=="2" goto :read_file
if "%choice%"=="3" goto :write_file
if "%choice%"=="4" goto :search_files
if "%choice%"=="5" goto :end
goto :main_menu

:browse
cls
echo Nexus AI - Directory Browser
echo ===========================
echo.

set /p dir="Enter directory to browse (e.g., D:\, C:\Users): "

if not exist "%dir%\" (
    echo Error: Directory does not exist!
    pause
    goto :browse
)

cls
echo Contents of %dir%
echo ==================

echo Directories:
echo -----------
for /d %%i in ("%dir%\*") do echo [DIR]  %%~nxi

echo.
echo Files:
echo -----
for %%i in ("%dir%\*.*") do echo [FILE] %%~nxi

echo.
echo.
echo Commands:
echo  - Enter directory name to navigate into it
echo  - Type '..' to go up one level
echo  - Type 'menu' to return to main menu
echo.
set /p nav="Enter directory name or command: "

if "%nav%"=="menu" goto :main_menu
if "%nav%"==".." (
    for %%I in ("%dir%\..") do set "dir=%%~fI"
    goto :browse
)

if exist "%dir%\%nav%\" (
    set "dir=%dir%\%nav%"
    goto :browse
) else (
    echo Error: Directory not found!
    pause
    goto :browse
)

:read_file
cls
echo Nexus AI - File Reader
echo ====================
echo.

set /p file="Enter file path to read: "

if not exist "%file%" (
    echo Error: File does not exist!
    pause
    goto :read_file
)

cls
echo Contents of %file%
echo ==================
echo.
type "%file%"
echo.
echo.
pause
goto :main_menu

:write_file
cls
echo Nexus AI - File Writer
echo ====================
echo.

set /p file="Enter file path to write: "
set /p content="Enter content to write: "

echo %content% > "%file%"

if %errorlevel% neq 0 (
    echo Error: Failed to write to file!
) else (
    echo File written successfully!
)
pause
goto :main_menu

:search_files
cls
echo Nexus AI - File Search
echo ====================
echo.

set /p search_dir="Enter directory to search in: "
set /p pattern="Enter search pattern (e.g., *.txt): "

if not exist "%search_dir%\" (
    echo Error: Directory does not exist!
    pause
    goto :search_files
)

cls
echo Search Results: %pattern% in %search_dir%
echo =======================================
echo.

dir /s /b "%search_dir%\%pattern%" 2>nul

echo.
echo.
pause
goto :main_menu

:end
echo.
echo Thank you for using Nexus AI File Browser
echo.