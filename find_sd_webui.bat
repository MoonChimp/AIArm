@echo off
echo ===================================================================== 
echo NEXUS AI: FIND STABLE DIFFUSION WEBUI
echo ===================================================================== 

echo Searching for StableDiffusion WebUI installation...

REM Common installation locations
set POSSIBLE_PATHS=D:\AIArm\stable-diffusion-webui D:\stable-diffusion-webui C:\stable-diffusion-webui C:\Users\%USERNAME%\stable-diffusion-webui D:\AIArm\StableDiffusionWebUI D:\StableDiffusionWebUI C:\StableDiffusionWebUI

REM Try to find the WebUI
set WEBUI_PATH=

for %%p in (%POSSIBLE_PATHS%) do (
    if exist "%%p\webui-user.bat" (
        set WEBUI_PATH=%%p
        echo Found WebUI at: %%p
        goto :found
    )
)

echo Searching in D: drive...
for /f "tokens=*" %%a in ('dir /b /s /a:d "D:\*webui*" 2^>nul') do (
    if exist "%%a\webui-user.bat" (
        set WEBUI_PATH=%%a
        echo Found WebUI at: %%a
        goto :found
    )
)

echo Searching in C: drive (this may take longer)...
for /f "tokens=*" %%a in ('dir /b /s /a:d "C:\*webui*" 2^>nul') do (
    if exist "%%a\webui-user.bat" (
        set WEBUI_PATH=%%a
        echo Found WebUI at: %%a
        goto :found
    )
)

:notfound
echo.
echo Could not find StableDiffusion WebUI installation.
echo.
echo Please enter the full path to your StableDiffusion WebUI folder:
set /p WEBUI_PATH="Path: "

if not exist "%WEBUI_PATH%\webui-user.bat" (
    echo webui-user.bat not found in that location.
    echo Please install StableDiffusion WebUI or provide the correct path.
    goto :end
)

:found
echo.
echo StableDiffusion WebUI found at: %WEBUI_PATH%
echo.
echo Do you want to:
echo 1. Start WebUI with API enabled
echo 2. Create shortcut batch file to start WebUI
echo 3. Exit
choice /C 123 /M "Select option: "

if errorlevel 3 goto :end
if errorlevel 2 goto :create_shortcut
if errorlevel 1 goto :start_webui

:start_webui
echo.
echo Starting StableDiffusion WebUI with API enabled...
cd /d "%WEBUI_PATH%"
start "StableDiffusion WebUI" webui-user.bat --api
echo.
echo WebUI started in a new window.
goto :end

:create_shortcut
echo.
echo Creating shortcut batch file...
echo @echo off > "D:\AIArm\start_sd_webui.bat"
echo echo Starting StableDiffusion WebUI with API enabled... >> "D:\AIArm\start_sd_webui.bat"
echo cd /d "%WEBUI_PATH%" >> "D:\AIArm\start_sd_webui.bat"
echo webui-user.bat --api >> "D:\AIArm\start_sd_webui.bat"
echo.
echo Shortcut created at: D:\AIArm\start_sd_webui.bat
echo.
echo Do you want to start WebUI now?
choice /C YN /M "Start WebUI now? "
if errorlevel 2 goto :end
goto :start_webui

:end
echo.
echo Press any key to exit...
pause > nul
