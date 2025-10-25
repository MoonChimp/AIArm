@echo off
setlocal EnableDelayedExpansion

set "COMMAND=%~1"
set "CONFIG=%~2"
set "PROMPT=%~3"

if "%COMMAND%"=="" (
    echo Usage: nexus_command.bat "COMMAND" "CONFIG" "PROMPT"
    echo Commands: CREATE_VIDEO, OPEN_PROGRAM, STATUS
    exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\AIArm\nexus_interface.ps1" -Command "%COMMAND%" -Config "%CONFIG%" -Prompt "%PROMPT%"