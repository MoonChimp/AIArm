const express = require('express');
const path = require('path');
const fs = require('fs');

// Initialize Express app
const app = express();
const PORT = 3050;

// Middleware
app.use(express.static(path.join(__dirname)));
app.use(express.json());

// Simple status endpoint
app.get('/api/status', (req, res) => {
    console.log('Status endpoint called');
    res.json({ 
        success: true, 
        status: 'online', 
        message: 'Minimal test server running',
        timestamp: new Date().toISOString()
    });
});

// Simple process endpoint
app.post('/api/process', (req, res) => {
    console.log('Process endpoint called with:', req.body);
    
    // Echo back the request with some minimal processing
    const response = {
        success: true,
        responses: [
            {
                id: Date.now(),
                content: `Received: "${req.body.input}"`,
                agent: 'test-server',
                timestamp: new Date().toLocaleTimeString(),
                type: 'agent_response'
            }
        ]
    };
    
    res.json(response);
});

// Start the server
app.listen(PORT, () => {
    console.log(`Minimal test server running on port ${PORT}`);
    console.log(`Open http://localhost:${PORT}/simple_interface.html to test`);
});
