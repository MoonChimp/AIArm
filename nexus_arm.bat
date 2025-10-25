@echo off
echo === AI ARM INTERFACE TO COMMANDER NEXUS ===
echo.

set "COMMAND=%~1"
set "CONTEXT=%~2"

if "%COMMAND%"=="" (
    echo Usage: nexus_arm.bat "COMMAND" "CONTEXT"
    echo.
    echo Commands:
    echo   CREATE_VIDEO   - Request video creation
    echo   OPEN_PROGRAM   - Request program launch  
    echo   STATUS         - Get system status
    echo   MEMORY_QUERY   - Query Commander Nexus memory
    echo.
    echo Examples:
    echo   nexus_arm.bat "CREATE_VIDEO" "Epic dragon flying over mountains"
    echo   nexus_arm.bat "STATUS"
    echo   nexus_arm.bat "OPEN_PROGRAM" "RunwayML"
    echo.
    exit /b 1
)

echo Connecting AI Arm to Commander Nexus (LLaMA 7B)...
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\AIArm\ai_arm.ps1" -Command "%COMMAND%" -Context "%CONTEXT%"
