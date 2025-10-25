@echo off
echo ===================================================================== 
echo NEXUS AI: ENHANCED PERSONAL ASSISTANT AGENT (EPAA) - SETUP
echo ===================================================================== 

REM Stop any running servers
echo Stopping any running servers...
taskkill /f /im python.exe 2>nul

REM Create the enhanced EPAA model
echo Creating NexusAI:EPAA with personality traits from Jarvis, Cortana, and TARS...
cd D:\AIArm
ollama create nexusai-epaa:latest -f ModelfileEPAA

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create the EPAA model.
    pause
    exit /b 1
)
echo [SUCCESS] Created nexusai-epaa:latest model with Jarvis/Cortana/TARS personality blend

REM Update the interface to use the EPAA model
echo Updating interface to use the new EPAA model...
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace 'let modelToUse = ''nexusai-enhanced:latest'';', 'let modelToUse = ''nexusai-epaa:latest'';' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

REM Update header text
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace '<h1 style=\"text-align: right;\">Nexus AI - Direct</h1>', '<h1 style=\"text-align: right;\">NexusAI:EPAA</h1>' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

REM Update status text code
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace 'statusText.textContent = ''Connected to Ollama \(nexusai-enhanced\)'';', 'statusText.textContent = ''Connected to Ollama \(NexusAI:EPAA\)'';' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

REM Update footer text
powershell -Command "(Get-Content D:\AIArm\WebInterface\nexus_direct.html) -replace 'Nexus AI Direct v1.0 - Connected directly to Ollama', 'NexusAI:EPAA - Enhanced Personal Assistant Agent' | Set-Content D:\AIArm\WebInterface\nexus_direct.html"

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

echo Starting NexusAI:EPAA server...
cd D:\AIArm\WebInterface
start "NexusAI:EPAA" python nexus_direct_server.py

echo ===================================================================== 
echo NEXUS AI:EPAA - SETUP COMPLETE
echo ===================================================================== 
echo.
echo Your NexusAI:EPAA has been created with:
echo - Personality blend of Jarvis (Iron Man), Cortana (Halo), and TARS (Interstellar)
echo - ACTUAL agent capabilities
echo - Enhanced interface branding
echo.
echo The server has been restarted and your browser should open automatically.
echo If not, visit: http://localhost:8000/nexus_direct.html
echo.
echo Press any key to exit this window...
pause > nul
