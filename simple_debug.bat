@echo off
echo =====================================================================
echo                   AIArm Debug Launcher - Simple Version
echo =====================================================================
echo.

:: Set debug flag for more output
set DEBUG_MODE=true

echo Starting in DEBUG mode with verbose output...
echo.

:: Create necessary directories
echo Checking directories...
if not exist "D:\AIArm\WebInterface\Logs" (
    echo Creating Logs directory...
    mkdir "D:\AIArm\WebInterface\Logs" 
)
if not exist "D:\AIArm\TaskQueue" (
    echo Creating TaskQueue directory...
    mkdir "D:\AIArm\TaskQueue"
)

:: Set the status to online
echo Setting status to online...
echo online > "D:\AIArm\WebInterface\service_status.txt"

:: Check Node.js version
echo Checking Node.js version...
node --version

:: Change to WebInterface directory
echo Changing to WebInterface directory...
cd /d "D:\AIArm\WebInterface"

:: Ensure we have required dependencies
echo Checking for node_modules directory...
if not exist "node_modules" (
    echo Installing dependencies (this may take a minute)...
    call npm install
    if %errorlevel% neq 0 (
        echo Failed to install dependencies!
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
) else (
    echo node_modules directory exists.
)

:: Create a simplified HTML file for testing
echo Creating simplified test interface...
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
echo Creating debug server...
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
echo Starting debug server on port 3030...
start "AIArm Debug Server" cmd /c "node debug_server.js"

:: Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak > nul

echo Debug server should be running now.
echo Open your browser and navigate to: http://localhost:3030/simple_test.html
echo.
echo This is a simplified test interface to verify basic connectivity.
echo If this works, the issue is likely with the React UI component or the Python bridge.
echo.
echo Press any key to continue with normal server startup (or CTRL+C to exit)...
pause > nul

:: Run the normal server with debugging info
echo Starting normal server with debug output...
echo This will show any JavaScript errors...
node --trace-warnings server.js

pause
