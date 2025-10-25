const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const bodyParser = require('body-parser');

// Initialize Express app
const app = express();
const PORT = 45678; // Using a high port number to avoid conflicts

// Path to Python orchestrator
const ORCHESTRATOR_PATH = path.join(__dirname, '..', 'MultiAgent', 'enhanced_orchestrator.py');
const BRIDGE_PATH = path.join(__dirname, 'orchestrator_bridge.py');

// Middleware
app.use(express.static(path.join(__dirname)));
app.use(bodyParser.json());

// Serve the frontend interface
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'crystalline.html'));
});

// API endpoint to process requests through the actual AI orchestrator
app.post('/api/process', (req, res) => {
    const { input, activeAgent } = req.body;
    console.log(`Forwarding request to AI orchestrator: ${input} (Agent: ${activeAgent})`);
    
    // Create Python bridge command that uses the correct process_request method
    const pythonProcess = spawn('python', [
        BRIDGE_PATH,
        '--input', input,
        '--agent', activeAgent
    ]);
    
    let responseData = '';
    let errorData = '';
    
    // Collect data from the orchestrator
    pythonProcess.stdout.on('data', (data) => {
        responseData += data.toString();
        console.log(`Python output: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
        console.error(`Python error: ${data}`);
    });
    
    // Process has completed
    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
        
        if (code === 0 && responseData) {
            try {
                // Try to parse the orchestrator's output as JSON
                const parsedResponse = JSON.parse(responseData);
                
                if (parsedResponse.success) {
                    // Format the response for the frontend
                    const responses = [];
                    
                    if (parsedResponse.response) {
                        // Single response format
                        responses.push({
                            id: Date.now(),
                            content: parsedResponse.response,
                            agent: activeAgent,
                            timestamp: new Date().toLocaleTimeString(),
                            type: 'agent_response'
                        });
                    } else if (parsedResponse.responses) {
                        // Multiple response format
                        parsedResponse.responses.forEach((resp, index) => {
                            responses.push({
                                id: Date.now() + index,
                                content: resp.content || resp,
                                agent: resp.agent || activeAgent,
                                timestamp: resp.timestamp || new Date().toLocaleTimeString(),
                                type: 'agent_response'
                            });
                        });
                    }
                    
                    res.json({ success: true, responses });
                } else {
                    // Return error from Python
                    res.status(500).json({
                        success: false,
                        error: parsedResponse.error || 'Unknown error',
                        responses: [{
                            id: Date.now(),
                            content: parsedResponse.error || 'Error processing request',
                            agent: 'orchestrator',
                            timestamp: new Date().toLocaleTimeString(),
                            type: 'agent_response'
                        }]
                    });
                }
            } catch (error) {
                console.error('Failed to parse orchestrator response:', error);
                // Return raw output if parsing fails
                res.json({
                    success: true,
                    responses: [{
                        id: Date.now(),
                        content: responseData,
                        agent: 'orchestrator',
                        timestamp: new Date().toLocaleTimeString(),
                        type: 'agent_response'
                    }]
                });
            }
        } else {
            // Return error
            res.status(500).json({
                success: false,
                error: errorData || 'Unknown error',
                responses: [{
                    id: Date.now(),
                    content: errorData || 'Error processing request',
                    agent: 'orchestrator',
                    timestamp: new Date().toLocaleTimeString(),
                    type: 'agent_response'
                }]
            });
        }
    });
});

// Get system status by checking if orchestrator is accessible
app.get('/api/status', (req, res) => {
    // Create Python command to get orchestrator status
    const pythonProcess = spawn('python', [
        BRIDGE_PATH  // No args means just check if it loads
    ]);
    
    let statusData = '';
    let errorData = '';
    
    pythonProcess.stdout.on('data', (data) => {
        statusData += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
        if (code === 0 && statusData) {
            try {
                // Parse status JSON
                const parsedStatus = JSON.parse(statusData);
                res.json(parsedStatus);
            } catch (error) {
                // Return simple status if parsing fails
                res.json({
                    success: true,
                    status: 'online',
                    error: 'Failed to parse status response'
                });
            }
        } else {
            res.json({
                success: false,
                status: 'error',
                error: errorData || 'Unknown error checking orchestrator status'
            });
        }
    });
});

// Start the server
console.log('Starting AIArm Crystalline Interface server...');
console.log(`Using orchestrator at: ${ORCHESTRATOR_PATH}`);
console.log(`Using bridge script at: ${BRIDGE_PATH}`);

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Open your browser and navigate to: http://localhost:${PORT}`);
}).on('error', (err) => {
    console.error('Server error:', err);
    process.exit(1);
});
