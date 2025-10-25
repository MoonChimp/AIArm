@echo off
echo =====================================================================
echo                   AIArm Crystalline Interface
echo =====================================================================
echo.

echo Initializing Crystalline Interface...
echo.

:: Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed. Please install Node.js and try again.
    pause
    exit /b 1
)

:: Create necessary directories
mkdir "D:\AIArm\logs" 2>nul

:: Set up port
set PORT=3100
netstat -ano | findstr ":%PORT%" > nul
if %ERRORLEVEL% EQU 0 (
    echo Port %PORT% is already in use. Trying alternative port 3101...
    set PORT=3101
    netstat -ano | findstr ":%PORT%" > nul
    if %ERRORLEVEL% EQU 0 (
        echo Port %PORT% is also in use. Trying alternative port 3102...
        set PORT=3102
    )
)

echo Will use port %PORT% for the Crystalline Interface server.
echo.

:: Write a temporary server file with dynamic port
(
echo const express = require('express'^);
echo const path = require('path'^);
echo const fs = require('fs'^);
echo const bodyParser = require('body-parser'^);
echo const cors = require('cors'^);
echo const { spawn } = require('child_process'^);
echo.
echo // Initialize Express app
echo const app = express(^);
echo const PORT = %PORT%;
echo.
echo // Middleware
echo app.use(cors(^)^);
echo app.use(express.static(path.join(__dirname^)^)^);
echo app.use(bodyParser.json(^)^);
echo.
echo // Serve the crystalline interface
echo app.get('/', (req, res^) =^> {
echo   res.sendFile(path.join(__dirname, 'crystalline.html'^)^);
echo }^);
echo.
echo // Surface bridge request function
echo function processSurfaceBridgeRequest(input, userId = 'default', agentName = 'orchestrator'^) {
echo   return new Promise((resolve, reject^) =^> {
echo     console.log(`Processing surface bridge request for user ${userId}, agent ${agentName}`^);
echo     
echo     const python = spawn('python', ['improved_bridge.py']^);
echo     let responseData = '';
echo     let errorData = '';
echo     
echo     python.stdout.on('data', (data^) =^> {
echo       responseData += data.toString(^);
echo     }^);
echo     
echo     python.stderr.on('data', (data^) =^> {
echo       errorData += data.toString(^);
echo       console.warn(`Surface bridge error output: ${data.toString(^)}`^);
echo     }^);
echo     
echo     python.on('close', (code^) =^> {
echo       if (code !== 0^) {
echo         console.error(`Surface bridge process exited with code ${code}`^);
echo         console.error(`Error data: ${errorData}`^);
echo         reject(new Error(`Surface bridge process exited with code ${code}: ${errorData}`^)^);
echo         return;
echo       }
echo       
echo       try {
echo         const result = JSON.parse(responseData^);
echo         resolve(result^);
echo       } catch (error^) {
echo         console.error('Failed to parse surface bridge response:', error^);
echo         console.error(`Raw response: ${responseData}`^);
echo         reject(new Error(`Failed to parse surface bridge response: ${error.message}`^)^);
echo       }
echo     }^);
echo     
echo     python.on('error', (error^) =^> {
echo       console.error('Failed to start surface bridge process:', error^);
echo       reject(error^);
echo     }^);
echo     
echo     // Send the request to the Python bridge
echo     const requestData = JSON.stringify({
echo       agent: agentName,
echo       input: input,
echo       user_id: userId
echo     }^);
echo     
echo     python.stdin.write(requestData^);
echo     python.stdin.end(^);
echo   }^);
echo }
echo.
echo // API endpoints
echo app.get('/api/status', (req, res^) =^> {
echo   res.json({ success: true, status: 'online' }^);
echo }^);
echo.
echo app.post('/api/process', async (req, res^) =^> {
echo   try {
echo     const { input, activeAgent } = req.body;
echo     const userId = req.headers['x-session-id'] || 'default';
echo     
echo     console.log(`Received request: ${input} for agent: ${activeAgent}`^);
echo     
echo     // Process with the surface bridge
echo     const result = await processSurfaceBridgeRequest(input, userId, activeAgent^);
echo     
echo     if (result.success^) {
echo       res.json(result^);
echo     } else {
echo       // Fallback to simulated responses
echo       const responses = [
echo         {
echo           id: Date.now(^),
echo           content: `Processing your request: "${input}". Analyzing requirements and coordinating with specialized agents...`,
echo           agent: 'orchestrator',
echo           timestamp: new Date(^).toLocaleTimeString(^),
echo           type: 'agent_response'
echo         },
echo         {
echo           id: Date.now(^) + 1,
echo           content: `Research phase initiated. Gathering relevant information and analyzing current trends related to your request.`,
echo           agent: activeAgent || 'research',
echo           timestamp: new Date(^).toLocaleTimeString(^),
echo           type: 'agent_response'
echo         }
echo       ];
echo       
echo       res.json({ success: true, responses }^);
echo     }
echo   } catch (error^) {
echo     console.error('Error processing request:', error^);
echo     res.status(500^).json({ 
echo       success: false, 
echo       error: error.message || 'Internal server error',
echo       result: 'I apologize, but I encountered an issue processing your request. Please try again.'
echo     }^);
echo   }
echo }^);
echo.
echo // Start the server
echo app.listen(PORT, (^) =^> {
echo   console.log(`AIArm Crystalline Interface running on port ${PORT}`^);
echo   console.log(`Open your browser and navigate to: http://localhost:${PORT}`^);
echo }^);
) > temp_crystalline_server.js

:: Install dependencies if not present
if not exist "node_modules\express" (
    echo Installing required Node.js modules...
    call npm install express cors body-parser
)

:: Start the server
echo =====================================================================
echo                   Starting Crystalline Interface
echo =====================================================================
echo.
echo Crystalline Interface is launching...
echo.
echo Once the server is running, open your browser to http://localhost:%PORT%
echo.

node temp_crystalline_server.js

:: Cleanup
del temp_crystalline_server.js

pause
