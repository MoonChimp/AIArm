@echo off
echo ===================================================================== 
echo NEXUS AI DIRECT - UPDATE INTERFACE
echo ===================================================================== 

REM Check if Nexus Logo exists and copy it if needed
echo Checking for Nexus Logo...
if exist "D:\AIArm\NexusLogo.gif" (
    echo Found Nexus Logo at D:\AIArm\NexusLogo.gif
    echo Copying logo to WebInterface directory...
    copy "D:\AIArm\NexusLogo.gif" "D:\AIArm\WebInterface\NexusLogo.gif" /Y
    if %ERRORLEVEL% NEQ 0 (
        echo [WARNING] Failed to copy logo. Interface will still work but may not display the logo.
    ) else (
        echo [SUCCESS] Logo copied successfully
    )
) else (
    echo [WARNING] Nexus Logo not found at D:\AIArm\NexusLogo.gif
    echo The interface will still work but will not display the logo.
    echo If you have a logo, place it at D:\AIArm\NexusLogo.gif and run this script again.
)

REM Restart the server if it's running
echo Stopping any running servers...
taskkill /f /im python.exe 2>nul

echo Starting Nexus AI Direct server with updated interface...
cd D:\AIArm\WebInterface
start "Nexus AI Direct" python nexus_direct_server.py

echo ===================================================================== 
echo NEXUS AI DIRECT - INTERFACE UPDATED
echo ===================================================================== 
echo.
echo The interface has been updated with:
echo - Darker background (25-30%%)
echo - Logo in the left corner (if available)
echo - Header text aligned to the right
echo.
echo The server has been restarted and your browser should open automatically.
echo If not, visit: http://localhost:8000/nexus_direct.html
echo.
echo Press any key to exit this window...
pause > nul
