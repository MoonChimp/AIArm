const express = require('express');
const path = require('path');
const fs = require('fs');
const bodyParser = require('body-parser');

// Initialize Express app
const app = express();
const portList = [8080, 8888, 9000, 9090, 9999, 7777, 6666, 5555];

// Middleware
app.use(express.static(path.join(__dirname)));
app.use(bodyParser.json());

// Serve the crystalline interface
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'crystalline.html'));
});

// API endpoints
app.get('/api/status', (req, res) => {
  res.json({ success: true, status: 'online' });
});

app.post('/api/process', (req, res) => {
  const { input, activeAgent } = req.body;
  console.log(`Received request: ${input} for agent: ${activeAgent}`);

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

  res.json({ success: true, responses });
});

// Try starting the server on different ports
function tryPorts(ports, index = 0) {
  if (index >= ports.length) {
    console.error('All ports are in use! Please free up a port and try again.');
    process.exit(1);
  }

  const currentPort = ports[index];
  
  const server = app.listen(currentPort, () => {
    console.log(`AIArm Crystalline Interface running on port ${currentPort}`);
    console.log(`Open your browser and navigate to: http://localhost:${currentPort}`);
  }).on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.log(`Port ${currentPort} is in use, trying next port...`);
      tryPorts(ports, index + 1);
    } else {
      console.error('Server error:', err);
      process.exit(1);
    }
  });
}

// Start the server by trying each port in sequence
tryPorts(portList);
