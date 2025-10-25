@echo off
:: Administrator script for NexusAI:AlfaZer0
:: Used to create new capabilities and execute administrative tasks

:: Check for admin rights and elevate if needed
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "%*", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B
) else (
    goto gotAdmin
)

:gotAdmin
    if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs"
    pushd "%CD%"
    CD /D "%~dp0"

:: Get operation and parameters
set "operation=%~1"
set "param1=%~2"
set "param2=%~3"
set "param3=%~4"

if "%operation%"=="" goto :usage

:: Create necessary directories if they don't exist
if not exist "D:\NexusAI" mkdir "D:\NexusAI"
if not exist "D:\NexusAI\Scripts" mkdir "D:\NexusAI\Scripts"
if not exist "D:\NexusAI\Knowledge" mkdir "D:\NexusAI\Knowledge"
if not exist "D:\NexusAI\Modules" mkdir "D:\NexusAI\Modules"
if not exist "D:\NexusAI\UserData" mkdir "D:\NexusAI\UserData"

:: Process operations
if /i "%operation%"=="createScript" goto :createScript
if /i "%operation%"=="createModule" goto :createModule
if /i "%operation%"=="storeKnowledge" goto :storeKnowledge
if /i "%operation%"=="executeAdmin" goto :executeAdmin
if /i "%operation%"=="updateIndex" goto :updateIndex
goto :usage

:createScript
if "%param1%"=="" goto :usage
if "%param2%"=="" goto :usage

echo Creating script: %param1%
echo // %param1% > "D:\NexusAI\Scripts\%param1%.js"
echo // Created by NexusAI:AlfaZer0 on %date% at %time% >> "D:\NexusAI\Scripts\%param1%.js"
echo // Description: %param2% >> "D:\NexusAI\Scripts\%param1%.js"
echo. >> "D:\NexusAI\Scripts\%param1%.js"

if "%param3%"=="" goto :noScriptContent
echo %param3% >> "D:\NexusAI\Scripts\%param1%.js"
:noScriptContent

echo Script created: D:\NexusAI\Scripts\%param1%.js
goto :updateIndex

:createModule
if "%param1%"=="" goto :usage
if "%param2%"=="" goto :usage

echo Creating module: %param1%
if not exist "D:\NexusAI\Modules\%param1%" mkdir "D:\NexusAI\Modules\%param1%"

echo // %param1% Module > "D:\NexusAI\Modules\%param1%\index.js"
echo // Created by NexusAI:AlfaZer0 on %date% at %time% >> "D:\NexusAI\Modules\%param1%\index.js"
echo // Description: %param2% >> "D:\NexusAI\Modules\%param1%\index.js"
echo. >> "D:\NexusAI\Modules\%param1%\index.js"

if "%param3%"=="" goto :noModuleContent
echo %param3% >> "D:\NexusAI\Modules\%param1%\index.js"
:noModuleContent

echo Module created: D:\NexusAI\Modules\%param1%
goto :updateIndex

:storeKnowledge
if "%param1%"=="" goto :usage
if "%param2%"=="" goto :usage

echo Storing knowledge: %param1%
echo // %param1% > "D:\NexusAI\Knowledge\%param1%.txt"
echo // Created by NexusAI:AlfaZer0 on %date% at %time% >> "D:\NexusAI\Knowledge\%param1%.txt"
echo. >> "D:\NexusAI\Knowledge\%param1%.txt"
echo %param2% >> "D:\NexusAI\Knowledge\%param1%.txt"

echo Knowledge stored: D:\NexusAI\Knowledge\%param1%.txt
goto :end

:executeAdmin
if "%param1%"=="" goto :usage

echo Executing administrative command: %param1%
%param1% %param2% %param3%
echo Command executed with administrator privileges.
goto :end

:updateIndex
echo Updating capabilities index...
if not exist "D:\NexusAI\index.json" (
    echo { "version": "1.0", "created": "%date% %time%", "scripts": [], "modules": [], "capabilities": [] } > "D:\NexusAI\index.json"
)

:: Use PowerShell to update the JSON file
powershell -Command "& {
    $indexPath = 'D:\NexusAI\index.json'
    $index = Get-Content $indexPath -Raw | ConvertFrom-Json
    
    # Update scripts list
    $scripts = @()
    Get-ChildItem 'D:\NexusAI\Scripts' -Filter *.js | ForEach-Object {
        $scriptName = $_.BaseName
        if ($index.scripts -notcontains $scriptName) {
            $index.scripts += $scriptName
        }
    }
    
    # Update modules list
    $modules = @()
    Get-ChildItem 'D:\NexusAI\Modules' -Directory | ForEach-Object {
        $moduleName = $_.Name
        if ($index.modules -notcontains $moduleName) {
            $index.modules += $moduleName
        }
    }
    
    # Add to capabilities if new
    if ('$param1' -ne '' -and $index.capabilities -notcontains '$param1') {
        $index.capabilities += '$param1'
    }
    
    # Update last modified
    $index.last_updated = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    
    # Save the updated index
    $index | ConvertTo-Json -Depth 4 | Set-Content $indexPath
}"

echo Index updated successfully.
goto :end

:usage
echo Usage:
echo.
echo NexusAI_Expander.bat createScript [name] [description] [content]
echo   - Creates a new script in the Scripts directory
echo.
echo NexusAI_Expander.bat createModule [name] [description] [content]
echo   - Creates a new module in the Modules directory
echo.
echo NexusAI_Expander.bat storeKnowledge [name] [content]
echo   - Stores knowledge in the Knowledge directory
echo.
echo NexusAI_Expander.bat executeAdmin [command] [params]
echo   - Executes a command with administrative privileges
echo.
echo NexusAI_Expander.bat updateIndex
echo   - Updates the capabilities index
echo.

:end
exit /b
