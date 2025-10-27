@echo off
echo ============================================================
echo NexusAI Template Integration - Quick Setup
echo ============================================================
echo.

cd /d D:\AIArm

echo [1/5] Extracting template...
powershell -Command "Expand-Archive -Path 'themeforest-QeXGM1Iz-megabot-ai-writer-copywriting-landing-page-html-template.zip' -DestinationPath 'NexusAI_Interface' -Force"

echo [2/5] Creating custom version...
if not exist "NexusAI_Interface\NexusAI_Custom" mkdir "NexusAI_Interface\NexusAI_Custom"
xcopy /E /I /Y "NexusAI_Interface\*" "NexusAI_Interface\NexusAI_Custom\"

echo [3/5] Creating directories...
if not exist "NexusAI_Interface\NexusAI_Custom\js" mkdir "NexusAI_Interface\NexusAI_Custom\js"
if not exist "NexusAI_Interface\NexusAI_Custom\css" mkdir "NexusAI_Interface\NexusAI_Custom\css"

echo [4/5] Setup complete!
echo.
echo Next steps:
echo 1. Copy nexusai-connector.js to: D:\AIArm\NexusAI_Interface\NexusAI_Custom\js\
echo 2. Copy nexusai-custom.css to: D:\AIArm\NexusAI_Interface\NexusAI_Custom\css\
echo 3. Modify index.html according to the guide
echo 4. Start NexusAI backend: python NEXUS_ULTIMATE_INTERFACE.py
echo 5. Open index.html in browser to test
echo.

echo [5/5] Opening guide...
start COMPLETE_INTEGRATION_GUIDE.md

pause

