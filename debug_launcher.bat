@echo off
echo [1;36m=====================================================================[0m
echo [1;36m        AIArm Debug Launcher - Verbose Output[0m
echo [1;36m=====================================================================[0m
echo.

:: Set debug flag for more output
set DEBUG_MODE=true

echo [1;33mStarting in DEBUG mode with verbose output...[0m
echo.

:: Create necessary directories
echo [1;33mChecking directories...[0m
if not exist "D:\AIArm\WebInterface\Logs" (
    echo Creating Logs directory...
    mkdir "D:\AIArm\WebInterface\Logs" 
)
if not exist "D:\AIArm\TaskQueue" (
    echo Creating TaskQueue directory...
    mkdir "D:\AIArm\TaskQueue"
)

:: Set the status to online
echo [1;33mSetting status to online...[0m
echo online > "D:\AIArm\WebInterface\service_status.txt"

:: Check Node.js version
echo [1;33mChecking Node.js version...[0m
node --version

:: Change to WebInterface directory
echo [1;33mChanging to WebInterface directory...[0m
cd /d "D:\AIArm\WebInterface"

:: Ensure we have required dependencies
echo [1;33mChecking for node_modules directory...[0m
if not exist "node_modules" (
    echo [1;33mInstalling dependencies (this may take a minute)...[0m
    call npm install
    if %errorlevel% neq 0 (
        echo [1;31mFailed to install dependencies![0m
        pause
        exit /b 1
    )
    echo [1;32mDependencies installed successfully.[0m
) else (
    echo [1;32mnode_modules directory exists.[0m
)

:: Create a simplified HTML file for testing
echo [1;33mCreating simplified test interface...[0m
echo ^<!DOCTYPE html^> > simple_test.html
echo ^<html^> >> simple_test.html
echo ^<head^> >> simple_test.html
echo ^<title^>AIArm Simple Test^</title^> >> simple_test.html
echo ^<style^>body{font-family:sans-serif;margin:20px;} .status{padding:10px;background:#eee;}^</style^> >> simple_test.html
echo ^</head^> >> simple_test.html
echo ^<body^> >> simple_test.html
echo ^<h1^>AIArm Simple Test Interface^</h1^> >> simple_test.html
echo ^<div class="status" id="status"^>Checking server status...^</div^> >> simple_test.html
echo ^<script^> >> simple_test.html
echo fetch('/api/status').then(r=^>r.json()).then(data=^>{document.getElementById('status').innerHTML = 'Server is running! Status: ' + data.status;}).catch(err=^>{document.getElementById('status').innerHTML = 'Error connecting to server: ' + err.message;}); >> simple_test.html
echo ^</script^> >> simple_test.html
echo ^</body^> >> simple_test.html
echo ^</html^> >> simple_test.html

:: Create a simple debug server script
echo [1;33mCreating debug server...[0m
echo const express = require('express'); > debug_server.js
echo const path = require('path'); >> debug_server.js
echo const app = express(); >> debug_server.js
echo const PORT = 3030; >> debug_server.js
echo. >> debug_server.js
echo // Serve static files >> debug_server.js
echo app.use(express.static(path.join(__dirname))); >> debug_server.js
echo. >> debug_server.js
echo // Status endpoint >> debug_server.js
echo app.get('/api/status', (req, res) =^> { >> debug_server.js
echo   console.log('Status endpoint called'); >> debug_server.js
echo   res.json({ success: true, status: 'debug_mode' }); >> debug_server.js
echo }); >> debug_server.js
echo. >> debug_server.js
echo // Start server >> debug_server.js
echo const server = app.listen(PORT, () =^> { >> debug_server.js
echo   console.log(`Debug server running on port ${PORT}`); >> debug_server.js
echo }); >> debug_server.js

:: Run the debug server
echo [1;33mStarting debug server on port 3030...[0m
start "AIArm Debug Server" cmd /c "node debug_server.js"

:: Wait for server to start
echo [1;33mWaiting for server to start...[0m
timeout /t 3 /nobreak > nul

echo [1;32mDebug server should be running now.[0m
echo [1;32mOpen your browser and navigate to: http://localhost:3030/simple_test.html[0m
echo.
echo [1;33mThis is a simplified test interface to verify basic connectivity.[0m
echo [1;33mIf this works, the issue is likely with the React UI component or the Python bridge.[0m
echo.
echo [1;36mPress any key to continue with normal server startup (or CTRL+C to exit)...[0m
pause > nul

:: Run the normal server with debugging info
echo [1;33mStarting normal server with debug output...[0m
echo [1;33mThis will show any JavaScript errors...[0m
node --trace-warnings server.js

pause
