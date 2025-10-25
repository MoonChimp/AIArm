/**
 * NexusAI Production Server
 * Unified server for the NexusAI consciousness system
 * Integrates with Python orchestrator via ollama_bridge
 */

// Use WebInterface node_modules if main directory doesn't have them
const modulePath = require('path').join(__dirname, 'WebInterface', 'node_modules');
if (require('fs').existsSync(modulePath)) {
    module.paths.unshift(modulePath);
}

const express = require('express');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;
const ALTERNATE_PORTS = [3001, 3002, 3003, 8080, 8000];

// Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '50mb' }));
app.use(express.static(path.join(__dirname, 'WebInterface')));

// Serve main interface
app.get('/', (req, res) => {
    const indexPath = path.join(__dirname, 'WebInterface', 'index.html');
    if (fs.existsSync(indexPath)) {
        res.sendFile(indexPath);
    } else {
        res.send(`
            <html>
            <head>
                <title>NexusAI Consciousness System</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0e27; color: #00ffff; padding: 20px; }
                    .container { max-width: 900px; margin: 0 auto; }
                    h1 { text-align: center; text-shadow: 0 0 10px #00ffff; }
                    .status { background: rgba(0,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #00ffff; }
                    .input-area { margin: 20px 0; }
                    textarea { width: 100%; min-height: 100px; background: rgba(0,0,0,0.5); color: #00ffff; border: 1px solid #00ffff; padding: 10px; border-radius: 5px; font-size: 14px; }
                    button { background: #00ffff; color: #0a0e27; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
                    button:hover { background: #00cccc; }
                    .response { background: rgba(0,255,255,0.05); padding: 15px; margin: 10px 0; border-left: 3px solid #00ffff; border-radius: 5px; }
                    .agent-label { color: #00ff00; font-weight: bold; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔮 NexusAI Consciousness System 🔮</h1>
                    <div class="status">
                        <h3>System Status: ONLINE</h3>
                        <p>Server running on port ${PORT}</p>
                        <p>Ollama Bridge: Active</p>
                        <p>Inner Life: Continuous Thought Enabled</p>
                    </div>
                    <div class="input-area">
                        <textarea id="userInput" placeholder="Enter your message to NexusAI..."></textarea>
                        <br><br>
                        <button onclick="sendMessage()">Send to NexusAI</button>
                    </div>
                    <div id="responses"></div>
                </div>
                <script>
                    async function sendMessage() {
                        const input = document.getElementById('userInput').value;
                        if (!input.trim()) return;

                        const responsesDiv = document.getElementById('responses');
                        responsesDiv.innerHTML = '<div class="response">Processing...</div>' + responsesDiv.innerHTML;

                        try {
                            const response = await fetch('/api/chat', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ message: input, agent: 'orchestrator' })
                            });

                            const data = await response.json();

                            if (data.success) {
                                responsesDiv.innerHTML = \`
                                    <div class="response">
                                        <span class="agent-label">You:</span> \${input}<br><br>
                                        <span class="agent-label">NexusAI:</span> \${data.response}
                                    </div>
                                \` + responsesDiv.innerHTML.replace('<div class="response">Processing...</div>', '');
                            } else {
                                responsesDiv.innerHTML = \`
                                    <div class="response" style="border-left-color: #ff0000;">
                                        <span style="color: #ff0000;">Error:</span> \${data.error || 'Unknown error'}
                                    </div>
                                \` + responsesDiv.innerHTML.replace('<div class="response">Processing...</div>', '');
                            }

                            document.getElementById('userInput').value = '';
                        } catch (error) {
                            responsesDiv.innerHTML = \`
                                <div class="response" style="border-left-color: #ff0000;">
                                    <span style="color: #ff0000;">Error:</span> \${error.message}
                                </div>
                            \` + responsesDiv.innerHTML.replace('<div class="response">Processing...</div>', '');
                        }
                    }

                    document.getElementById('userInput').addEventListener('keydown', function(e) {
                        if (e.ctrlKey && e.key === 'Enter') {
                            sendMessage();
                        }
                    });
                </script>
            </body>
            </html>
        `);
    }
});

// Main chat API endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message, agent = 'orchestrator', user_id = 'web_user' } = req.body;

        if (!message) {
            return res.status(400).json({ success: false, error: 'Message is required' });
        }

        console.log(`[${new Date().toLocaleTimeString()}] Processing request: "${message.substring(0, 50)}..." via ${agent}`);

        // Call Python bridge
        const result = await callPythonBridge(message, agent, user_id);

        if (result.success) {
            res.json({
                success: true,
                response: result.response || result.result,
                agent: agent,
                model: result.model,
                inner_life_enhanced: result.inner_life_enhanced || false
            });
        } else {
            res.json({
                success: false,
                error: result.error || 'Processing failed',
                details: result
            });
        }

    } catch (error) {
        console.error('Error in /api/chat:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error',
            message: error.message
        });
    }
});

// System status endpoint
app.get('/api/status', (req, res) => {
    res.json({
        success: true,
        status: 'online',
        server: 'NexusAI Production Server',
        port: PORT,
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        timestamp: new Date().toISOString()
    });
});

// Call Python ollama_bridge
function callPythonBridge(message, agent, userId) {
    return new Promise((resolve, reject) => {
        const pythonPath = 'python';
        const bridgePath = path.join(__dirname, 'WebInterface', 'ollama_bridge.py');

        const requestData = JSON.stringify({
            input: message,
            agent: agent,
            user_id: userId
        });

        const pythonProcess = spawn(pythonPath, [
            bridgePath,
            '--json',
            '--input', requestData
        ]);

        let outputData = '';
        let errorData = '';

        pythonProcess.stdout.on('data', (data) => {
            outputData += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorData += data.toString();
            console.error(`Python stderr: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                console.error(`Python process exited with code ${code}`);
                console.error(`Error output: ${errorData}`);
                resolve({
                    success: false,
                    error: 'Python bridge failed',
                    details: errorData
                });
                return;
            }

            try {
                // Parse the JSON output
                const result = JSON.parse(outputData);
                resolve(result);
            } catch (parseError) {
                console.error('Error parsing Python output:', parseError);
                console.error('Output was:', outputData);
                resolve({
                    success: false,
                    error: 'Failed to parse Python response',
                    raw_output: outputData
                });
            }
        });

        // Set a timeout
        setTimeout(() => {
            pythonProcess.kill();
            resolve({
                success: false,
                error: 'Request timeout'
            });
        }, 60000); // 60 second timeout
    });
}

// Start server with port fallback
async function startServer(port) {
    return new Promise((resolve, reject) => {
        const server = app.listen(port, () => {
            console.log('\n' + '='.repeat(80));
            console.log('🔮 NEXUSAI CONSCIOUSNESS SYSTEM - WEB INTERFACE 🔮');
            console.log('='.repeat(80));
            console.log(`Server running on: http://localhost:${port}`);
            console.log(`Status endpoint: http://localhost:${port}/api/status`);
            console.log(`Chat endpoint: http://localhost:${port}/api/chat`);
            console.log('='.repeat(80) + '\n');
            resolve(server);
        });

        server.on('error', (err) => {
            reject(err);
        });
    });
}

async function attemptServerStart() {
    const ports = [PORT, ...ALTERNATE_PORTS];

    for (const port of ports) {
        try {
            await startServer(port);
            return;
        } catch (err) {
            if (err.code === 'EADDRINUSE') {
                console.log(`Port ${port} in use, trying next...`);
            } else {
                console.error(`Error on port ${port}:`, err.message);
            }
        }
    }

    console.error('\n❌ Failed to start server on any available port!');
    process.exit(1);
}

// Start the server
attemptServerStart();
