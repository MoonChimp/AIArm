const express = require('express');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;
const ALTERNATE_PORTS = [3001, 3002, 3003, 8080, 8000];

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname)));

// Serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API endpoint to process user input through the multi-agent system
app.post('/api/process', async (req, res) => {
    try {
        const { input, activeAgent } = req.body;
        
        // Log request to help with debugging
        console.log(`Received request: ${input} for agent: ${activeAgent}`);
        
        // Simulate processing with the multi-agent system
        // In a real implementation, this would connect to the enhanced_orchestrator.py
        // through a Python bridge or subprocess
        
        // For demo purposes, write the request to a file that could be picked up by a Python process
        fs.writeFileSync(
            path.join(__dirname, '..', 'TaskQueue', 'current_task.json'),
            JSON.stringify({ input, activeAgent, timestamp: new Date().toISOString() })
        );
        
        // Simulate agent responses
        const responses = [
            {
                id: Date.now(),
                content: `Processing your request: "${input}". Analyzing requirements and coordinating with specialized agents...`,
                agent: 'orchestrator',
                timestamp: new Date().toLocaleTimeString(),
                type: 'agent_response'
            },
            {
                id: Date.now() + 1,
                content: `Research phase initiated. Gathering relevant information and analyzing current trends related to your request.`,
                agent: 'research',
                timestamp: new Date().toLocaleTimeString(),
                type: 'agent_response'
            },
            {
                id: Date.now() + 2,
                content: `Strategic analysis complete. Identified key implementation phases and resource requirements for optimal execution.`,
                agent: 'planning',
                timestamp: new Date().toLocaleTimeString(),
                type: 'agent_response'
            }
        ];
        
        // Check if there's a response file from the actual agent system
        try {
            if (fs.existsSync(path.join(__dirname, 'response.json'))) {
                const agentResponse = JSON.parse(fs.readFileSync(
                    path.join(__dirname, 'response.json'), 
                    'utf8'
                ));
                
                if (agentResponse && agentResponse.responses) {
                    return res.json({ success: true, responses: agentResponse.responses });
                }
            }
        } catch (error) {
            console.error('Error reading agent response:', error);
        }
        
        // Return simulated responses if no actual responses are available
        return res.json({ success: true, responses });
        
    } catch (error) {
        console.error('Error processing request:', error);
        return res.status(500).json({ success: false, error: 'Internal server error' });
    }
});

// API endpoint to get system status
app.get('/api/status', (req, res) => {
    // Read status file if it exists
    try {
        if (fs.existsSync(path.join(__dirname, 'service_status.txt'))) {
            const status = fs.readFileSync(path.join(__dirname, 'service_status.txt'), 'utf8');
            return res.json({ success: true, status: status.trim() });
        }
    } catch (error) {
        console.error('Error reading status:', error);
    }
    
    // Default status if file doesn't exist
    return res.json({ 
        success: true, 
        status: 'online',
        metrics: {
            cpuUsage: Math.floor(Math.random() * 40) + 10,
            memoryUsage: Math.floor(Math.random() * 30) + 50,
            agentsOnline: 8,
            activeProcesses: Math.floor(Math.random() * 5) + 2
        }
    });
});

// Start the server
const startServer = (port) => {
    return new Promise((resolve, reject) => {
        const server = app.listen(port, () => {
            console.log(`AIArm Crystalline Interface server running on port ${port}`);
            console.log(`Open your browser and navigate to: http://localhost:${port}`);
            
            // Create service_status.txt if it doesn't exist
            const statusPath = path.join(__dirname, 'service_status.txt');
            if (!fs.existsSync(statusPath)) {
                fs.writeFileSync(statusPath, 'online');
            }
            
            // Ensure TaskQueue directory exists
            const taskQueueDir = path.join(__dirname, '..', 'TaskQueue');
            if (!fs.existsSync(taskQueueDir)) {
                fs.mkdirSync(taskQueueDir, { recursive: true });
            }
            
            resolve(server);
        });
        
        server.on('error', (err) => {
            reject(err);
        });
    });
};

// Try to start the server on the main port, fallback to alternatives if needed
async function attemptServerStart() {
    let currentPort = PORT;
    let error;
    
    try {
        await startServer(currentPort);
        return; // Server started successfully
    } catch (err) {
        console.error(`Failed to start server on port ${currentPort}:`, err.message);
        error = err;
        
        // If the port is already in use, try alternate ports
        if (err.code === 'EADDRINUSE') {
            console.log('Attempting to use alternate ports...');
            
            for (const port of ALTERNATE_PORTS) {
                try {
                    await startServer(port);
                    return; // Server started successfully on alternate port
                } catch (altErr) {
                    console.error(`Failed to start server on port ${port}:`, altErr.message);
                }
            }
        }
    }
    
    // If we get here, all ports failed
    console.error('Failed to start server on all attempted ports!');
    console.error('Please free up one of the following ports and try again:');
    console.error([PORT, ...ALTERNATE_PORTS].join(', '));
    console.error('\nRun D:\\AIArm\\free_port_3000.bat to help free up port 3000');
    
    // Throw the original error to exit with a non-zero code
    throw error;
}

attemptServerStart().catch(err => {
    console.error('Server start failed:', err.message);
    process.exit(1);
});
