@echo off
title Nexus AI - Direct File Operation
echo Nexus AI Direct File Operation
echo.

if "%~1"=="" goto :usage

if "%1"=="write" goto :write_file
if "%1"=="read" goto :read_file
if "%1"=="list" goto :list_dir
goto :usage

:write_file
if "%~2"=="" goto :usage
if "%~3"=="" goto :usage
echo Writing to file: %2
python D:\AIArm\WebInterface\nexus_direct_fs.py --operation write --path "%2" --content "%~3"
goto :end

:read_file
if "%~2"=="" goto :usage
echo Reading file: %2
python D:\AIArm\WebInterface\nexus_direct_fs.py --operation read --path "%2"
goto :end

:list_dir
if "%~2"=="" goto :usage
echo Listing directory: %2
python D:\AIArm\WebInterface\nexus_direct_fs.py --operation list --path "%2"
goto :end

:usage
echo Usage:
echo   nexus_fs write [path] [content]  - Write content to a file
echo   nexus_fs read [path]             - Read content from a file
echo   nexus_fs list [path]             - List contents of a directory
echo.
echo Examples:
echo   nexus_fs write D:\test.txt "Hello, world!"
echo   nexus_fs read D:\test.txt
echo   nexus_fs list D:\
goto :end

:end
pause