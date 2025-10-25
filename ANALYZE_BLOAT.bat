@echo off
echo ========================================
echo Nexus AI - Bloat Analysis
echo ========================================
echo.
echo Scanning D:\AIArm for bloat...
echo.

set OUTPUT_FILE=D:\AIArm\BLOAT_REPORT.txt

echo NEXUS AI - BLOAT ANALYSIS > "%OUTPUT_FILE%"
echo Generated: %date% %time% >> "%OUTPUT_FILE%"
echo ======================================== >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo Analyzing... Please wait...

echo === LARGE DIRECTORIES === >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo Checking Stable Diffusion...
if exist "D:\AIArm\stable-diffusion-webui-master" (
    echo [BLOAT] stable-diffusion-webui-master - ~9.5GB >> "%OUTPUT_FILE%"
    echo   Status: OPTIONAL - Only needed for image generation >> "%OUTPUT_FILE%"
    echo   Action: KEEP if using Photo Agent, otherwise DELETE >> "%OUTPUT_FILE%"
    echo. >> "%OUTPUT_FILE%"
)

echo Checking node_modules...
for /d /r "D:\AIArm" %%d in (node_modules) do (
    echo [BLOAT] %%d >> "%OUTPUT_FILE%"
    echo   Status: SAFE TO DELETE - Old React Native project >> "%OUTPUT_FILE%"
    echo. >> "%OUTPUT_FILE%"
)

echo Checking Python cache...
for /d /r "D:\AIArm" %%d in (__pycache__) do (
    echo [CACHE] %%d >> "%OUTPUT_FILE%"
    echo   Status: SAFE TO DELETE - Will regenerate >> "%OUTPUT_FILE%"
    echo. >> "%OUTPUT_FILE%"
)

echo Checking backups...
if exist "D:\AIArm\backup" (
    echo [BLOAT] D:\AIArm\backup - ~2MB >> "%OUTPUT_FILE%"
    echo   Status: SAFE TO DELETE - Old code backups >> "%OUTPUT_FILE%"
    echo. >> "%OUTPUT_FILE%"
)

echo Checking .git repositories...
for /d /r "D:\AIArm" %%d in (.git) do (
    echo [BLOAT] %%d >> "%OUTPUT_FILE%"
    echo   Status: SAFE TO DELETE - Git history >> "%OUTPUT_FILE%"
    echo. >> "%OUTPUT_FILE%"
)

echo Checking venv directories...
for /d /r "D:\AIArm" %%d in (venv) do (
    echo [BLOAT] %%d >> "%OUTPUT_FILE%"
    echo   Status: CHECK - May contain Stable Diffusion dependencies >> "%OUTPUT_FILE%"
    echo. >> "%OUTPUT_FILE%"
)

echo. >> "%OUTPUT_FILE%"
echo === SAFE TO DELETE SUMMARY === >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"
echo Can safely delete: >> "%OUTPUT_FILE%"
echo - D:\AIArm\nexusai-agent (old React Native project) >> "%OUTPUT_FILE%"
echo - D:\AIArm\backup (old code backups) >> "%OUTPUT_FILE%"
echo - All __pycache__ directories >> "%OUTPUT_FILE%"
echo - All .git directories (unless you need version history) >> "%OUTPUT_FILE%"
echo - D:\AIArm\WebInterface (unused old UI) >> "%OUTPUT_FILE%"
echo - D:\AIArm\IntelligentAgent (old test code) >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"
echo KEEP (REQUIRED): >> "%OUTPUT_FILE%"
echo - D:\AIArm\NexusCore >> "%OUTPUT_FILE%"
echo - D:\AIArm\InnerLife >> "%OUTPUT_FILE%"
echo - D:\AIArm\NexusUI_Static >> "%OUTPUT_FILE%"
echo - D:\AIArm\Memory >> "%OUTPUT_FILE%"
echo - D:\AIArm\Generated >> "%OUTPUT_FILE%"
echo - D:\AIArm\nexus_api_server.py >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"
echo OPTIONAL: >> "%OUTPUT_FILE%"
echo - D:\AIArm\stable-diffusion-webui-master (9.5GB) >> "%OUTPUT_FILE%"
echo   Keep if: You want Photo Agent to generate actual images >> "%OUTPUT_FILE%"
echo   Delete if: You only need Music/Code/Story agents >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo.
echo ========================================
echo Analysis complete!
echo ========================================
echo Report saved to: %OUTPUT_FILE%
echo.
type "%OUTPUT_FILE%"
echo.
pause
