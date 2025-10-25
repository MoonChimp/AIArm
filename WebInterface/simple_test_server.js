// Simple server to test interface
const express = require('express');
const path = require('path');
const http = require('http');

const app = express();
const port = 45679; // Using a different port for testing

// Serve static files
app.use(express.static(path.join(__dirname)));

// Serve interface on root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'real_interface.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// API endpoint for status
app.get('/api/status', (req, res) => {
  res.json({
    success: true,
    status: 'Online',
    message: 'Simple test server running',
    timestamp: new Date().toISOString()
  });
});

// API endpoint for processing
app.post('/api/process', (req, res) => {
  // Just echo back what was received with a simple response
  const { input, activeAgent, userId } = req.body;
  
  res.json({
    success: true,
    status: 'completed',
    result: `Test server received: "${input}"\nAgent: ${activeAgent}\nUser ID: ${userId}\n\nThis is a test server response.`,
    source: 'simple_test_server'
  });
});

// Create server
const server = http.createServer(app);

// Start server
server.listen(port, () => {
  console.log(`Simple test server running on port ${port}`);
  console.log(`Access interface at http://localhost:${port}`);
});
