@echo off
echo =====================================================================
echo                   AIARM WEB INTERFACE LAUNCHER
echo =====================================================================
echo.

echo Starting ONLY the web interface without any background services...
echo.

cd /D "D:\AIArm\WebInterface"

:: Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed. Please install Node.js and try again.
    pause
    exit /b 1
)

:: Create simple server to serve the interface
(
echo const express = require('express');
echo const path = require('path');
echo const { spawn } = require('child_process');
echo const app = express();
echo const PORT = 3333;
echo.
echo // Serve static files
echo app.use(express.static(path.join(__dirname)));
echo.
echo // Serve the interface
echo app.get('/', (req, res) =^> {
echo   res.sendFile(path.join(__dirname, 'real_interface.html'));
echo });
echo.
echo // API endpoint for processing
echo app.post('/api/process', (req, res) =^> {
echo   // Just pass through to the existing real_server
echo   const proc = spawn('node', ['real_server.js', '--one-shot'], {
echo     stdio: ['pipe', 'pipe', 'pipe']
echo   });
echo.
echo   // Forward the request body
echo   proc.stdin.write(JSON.stringify(req.body));
echo   proc.stdin.end();
echo.
echo   let data = '';
echo   proc.stdout.on('data', (chunk) =^> {
echo     data += chunk;
echo   });
echo.
echo   proc.on('close', () =^> {
echo     try {
echo       const result = JSON.parse(data);
echo       res.json(result);
echo     } catch (e) {
echo       res.json({ 
echo         success: false, 
echo         status: 'error',
echo         result: 'Error processing request. Please try again.'
echo       });
echo     }
echo   });
echo });
echo.
echo // Status endpoint
echo app.get('/api/status', (req, res) =^> {
echo   res.json({ 
echo     success: true, 
echo     status: 'online',
echo     message: 'Web interface active'
echo   });
echo });
echo.
echo app.listen(PORT, () =^> {
echo   console.log(`Web interface running at http://localhost:${PORT}`);
echo   console.log('Press Ctrl+C to stop');
echo });
) > web_interface_only.js

echo Installing any missing dependencies...
if not exist "node_modules\express" (
    npm install express --no-fund --no-audit --silent
)

echo.
echo Starting web interface on port 3333...
echo.
echo =====================================================================
echo     IMPORTANT: Open your browser to http://localhost:3333
echo =====================================================================
echo.
echo This window must remain open while using the interface.
echo Press Ctrl+C to stop the server when you're done.
echo.

node web_interface_only.js

pause
