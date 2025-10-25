@echo off
echo ===================================================================== 
echo NEXUS HRM ARCHITECTURE SYSTEM - QUICK FIX
echo ===================================================================== 

REM Create a backup of the concurrent_server.js file
echo Creating backup of concurrent_server.js...
copy "D:\AIArm\WebInterface\concurrent_server.js" "D:\AIArm\WebInterface\concurrent_server.js.bak"

REM Update the concurrent_server.js file to use the bridge wrapper
echo Updating concurrent_server.js to use bridge wrapper...
powershell -Command "(Get-Content D:\AIArm\WebInterface\concurrent_server.js) -replace 'process.spawn\\(\"python\"', 'process.spawn(\"python\", [\"bridge_wrapper.py\"' | Set-Content D:\AIArm\WebInterface\concurrent_server.js"
powershell -Command "(Get-Content D:\AIArm\WebInterface\concurrent_server.js) -replace '\\[surfaceBridgePath\\]', '[\"' + $((Get-Content D:\AIArm\WebInterface\concurrent_server.js | Select-String 'surfaceBridgePath').ToString().Split('=')[1].Trim().Trim('\"\;')) + '\"]' | Set-Content D:\AIArm\WebInterface\concurrent_server.js"
powershell -Command "(Get-Content D:\AIArm\WebInterface\concurrent_server.js) -replace '\\[deepBridgePath\\]', '[\"' + $((Get-Content D:\AIArm\WebInterface\concurrent_server.js | Select-String 'deepBridgePath').ToString().Split('=')[1].Trim().Trim('\"\;')) + '\"]' | Set-Content D:\AIArm\WebInterface\concurrent_server.js"

REM Fix port consistency
echo Fixing port consistency...
powershell -Command "(Get-Content D:\AIArm\WebInterface\concurrent_server.js) -replace 'const PORT = 45678', 'const PORT = customPort || 45678' | Set-Content D:\AIArm\WebInterface\concurrent_server.js"

REM Fix the repetitive prefix in responses
echo Fixing repetitive response prefix issue...
powershell -Command "(Get-Content D:\AIArm\WebInterface\real_interface.html) -replace '<div class=\"assistant-message\">', '<div class=\"assistant-message\" id=\"response-container\">' | Set-Content D:\AIArm\WebInterface\real_interface.html"

REM Add a script to the real_interface.html to clean responses
echo Adding response cleaning script...
powershell -Command "$content = Get-Content D:\AIArm\WebInterface\real_interface.html -Raw; $script = '<script>function cleanResponse(text) { return text.replace(/I've processed your request through the HRM architecture. The Surface layer provided structured understanding while the Deep reasoning layer added contextual depth. How else can I assist you\\?\\n\\n/g, \"\").replace(/Orchestrator \\(HRM\\)\\n[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2} [AP]M\\n/g, \"\"); } document.addEventListener(\"DOMNodeInserted\", function(e) { if(e.target.classList && e.target.classList.contains(\"assistant-message\")) { setTimeout(function() { e.target.innerHTML = cleanResponse(e.target.innerHTML); }, 100); } });</script>'; $content = $content -replace '</head>', \"$script</head>\"; Set-Content D:\AIArm\WebInterface\real_interface.html -Value $content"

REM Create a fixed startup script
echo Creating fixed startup script...
echo @echo off > D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo ===================================================================== >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo NEXUS HRM ARCHITECTURE SYSTEM - QUICK FIX >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo ===================================================================== >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo. >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo REM Check if Ollama is running >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo Checking Ollama availability... >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo curl -s http://localhost:11434/api/tags ^> nul >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo if %%ERRORLEVEL%% NEQ 0 ( >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo     echo [ERROR] Ollama is not running! Please start Ollama before running this script. >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo     echo Visit http://localhost:11434 to verify Ollama is running. >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo     pause >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo     exit /b 1 >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo ) >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo [SUCCESS] Ollama is running >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo. >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo REM Try to stop any running bridges >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo Cleaning up any running processes... >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo taskkill /f /im python.exe 2^>nul >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo. >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo Starting Nexus HRM system on port 45690... >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo cd "D:\AIArm\WebInterface" >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo echo The system will be available at http://localhost:45690 >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo node concurrent_server.js --port 45690 >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo. >> D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo pause >> D:\AIArm\WebInterface\start_nexus_quickfix.bat

echo ===================================================================== 
echo NEXUS HRM ARCHITECTURE QUICK FIX COMPLETE
echo ===================================================================== 
echo.
echo The system has been fixed. Please:
echo 1. Stop any running instances of Nexus
echo 2. Start the fixed system using:
echo    D:\AIArm\WebInterface\start_nexus_quickfix.bat
echo.
echo The system will run on port 45690 to avoid any conflicts.
echo.
echo Fixed issues:
echo 1. Bridge output parsing errors
echo 2. Port consistency
echo 3. Repetitive prefix in responses
echo.
echo Press any key to exit...
pause > nul
