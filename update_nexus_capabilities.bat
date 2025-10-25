@echo off
echo ===================================================================== 
echo NEXUS AI DIRECT - UPDATE WITH ACTUAL AGENT CAPABILITIES
echo ===================================================================== 

REM Stop any running servers
echo Stopping any running servers...
taskkill /f /im python.exe 2>nul

REM Update the Modelfile with actual agent capabilities
echo Updating Nexus AI model with ACTUAL agent capabilities...
cd D:\AIArm
ollama create nexusai-enhanced:latest -f Modelfile

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to update the enhanced model.
    pause
    exit /b 1
)
echo [SUCCESS] Updated nexusai-enhanced:latest model with ACTUAL agent capabilities

REM Update logo size
echo Updating logo size in interface...
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace 'width: 80px;', 'width: 160px;' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace 'height: 80px;', 'height: 160px;' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

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

echo Starting Nexus AI Direct server with updated capabilities...
cd D:\AIArm\WebInterface
start "Nexus AI Direct" python nexus_direct_server.py

echo ===================================================================== 
echo NEXUS AI DIRECT - UPDATE COMPLETE
echo ===================================================================== 
echo.
echo Your Nexus AI has been updated with:
echo - ACTUAL agent capabilities (not simulated)
echo - Larger logo (160px)
echo.
echo The server has been restarted and your browser should open automatically.
echo If not, visit: http://localhost:8000/nexus_direct.html
echo.
echo Press any key to exit this window...
pause > nul
