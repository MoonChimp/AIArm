@echo off
title Nexus AI - Safe File Writer
echo Nexus AI - Safe File Writer
echo =========================
echo.

REM Try to create a user-writable directory
set "SAFE_DIR=%USERPROFILE%\NexusAI_Files"
if not exist "%SAFE_DIR%" mkdir "%SAFE_DIR%"

REM Create timestamp for unique filename
set "TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

REM Define a file in the user's Documents folder (which should be writable)
set "DOCS_FILE=%USERPROFILE%\Documents\nexus_test_%TIMESTAMP%.txt"
set "DESKTOP_FILE=%USERPROFILE%\Desktop\nexus_test_%TIMESTAMP%.txt"
set "TEMP_FILE=%TEMP%\nexus_test_%TIMESTAMP%.txt"
set "CUSTOM_FILE=%SAFE_DIR%\nexus_test_%TIMESTAMP%.txt"

echo I will try to write files to several locations that should be accessible:
echo.
echo 1. Your Documents folder: %DOCS_FILE%
echo 2. Your Desktop: %DESKTOP_FILE%
echo 3. Temp folder: %TEMP_FILE%
echo 4. Custom NexusAI folder: %CUSTOM_FILE%
echo.
echo Let's try writing to each location...
echo.

echo --------------------------
echo Content to write to files:
echo --------------------------
echo This is a test file created by Nexus AI on %date% at %time%.
echo This file demonstrates filesystem capabilities.
echo If you can read this, the test was successful!
echo --------------------------
echo.

REM Try to write to Documents folder
echo Attempting to write to Documents folder...
(
  echo This is a test file created by Nexus AI on %date% at %time%.
  echo This file demonstrates filesystem capabilities.
  echo If you can read this, the test was successful!
) > "%DOCS_FILE%" 2>nul

if %errorlevel% equ 0 (
  echo SUCCESS: File written to %DOCS_FILE%
) else (
  echo FAILED: Could not write to Documents folder
)
echo.

REM Try to write to Desktop
echo Attempting to write to Desktop...
(
  echo This is a test file created by Nexus AI on %date% at %time%.
  echo This file demonstrates filesystem capabilities.
  echo If you can read this, the test was successful!
) > "%DESKTOP_FILE%" 2>nul

if %errorlevel% equ 0 (
  echo SUCCESS: File written to %DESKTOP_FILE%
) else (
  echo FAILED: Could not write to Desktop
)
echo.

REM Try to write to Temp folder
echo Attempting to write to Temp folder...
(
  echo This is a test file created by Nexus AI on %date% at %time%.
  echo This file demonstrates filesystem capabilities.
  echo If you can read this, the test was successful!
) > "%TEMP_FILE%" 2>nul

if %errorlevel% equ 0 (
  echo SUCCESS: File written to %TEMP_FILE%
) else (
  echo FAILED: Could not write to Temp folder
)
echo.

REM Try to write to Custom folder
echo Attempting to write to custom NexusAI folder...
(
  echo This is a test file created by Nexus AI on %date% at %time%.
  echo This file demonstrates filesystem capabilities.
  echo If you can read this, the test was successful!
) > "%CUSTOM_FILE%" 2>nul

if %errorlevel% equ 0 (
  echo SUCCESS: File written to %CUSTOM_FILE%
) else (
  echo FAILED: Could not write to custom folder
)
echo.

echo Test complete!
echo.
echo Successfully written files:
dir "%DOCS_FILE%" 2>nul && echo - %DOCS_FILE%
dir "%DESKTOP_FILE%" 2>nul && echo - %DESKTOP_FILE%
dir "%TEMP_FILE%" 2>nul && echo - %TEMP_FILE%
dir "%CUSTOM_FILE%" 2>nul && echo - %CUSTOM_FILE%

echo.
pause