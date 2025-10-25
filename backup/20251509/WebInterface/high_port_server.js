// Express server using high port range 
const express = require('express'); 
const path = require('path'); 
const fs = require('fs'); 
const bodyParser = require('body-parser'); 
 
// Initialize Express app 
const app = express(); 
 
// Use higher port range (45000-45999) to avoid conflicts 
const portRange = Array.from({ length: 1000 }, (_, i) => 45000 + i); 
 
// Middleware 
app.use(express.static(path.join(__dirname))); 
app.use(bodyParser.json()); 
 
// Serve the crystalline interface 
app.get('/', (req, res) => { 
  res.sendFile(path.join(__dirname, 'crystalline.html')); 
}); 
 
// API endpoints 
app.get('/api/status', (req, res) => { 
  const orchestratorPath = path.join(__dirname, '..', 'MultiAgent', 'enhanced_orchestrator.py'); 
  const orchestratorExists = fs.existsSync(orchestratorPath); 
  res.json({ 
    success: true, 
    status: 'online', 
    orchestratorFound: orchestratorExists, 
    orchestratorPath, 
    agentCount: 8 
  }); 
}); 
 
app.post('/api/process', (req, res) => { 
  const { input, activeAgent } = req.body; 
  console.log(`Received request: ${input} for agent: ${activeAgent}`); 
 
  // Check for orchestrator path 
  const orchestratorPath = path.join(__dirname, '..', 'MultiAgent', 'enhanced_orchestrator.py'); 
  if (fs.existsSync(orchestratorPath)) { 
    console.log(`Found orchestrator at: ${orchestratorPath}`); 
    console.log('Would normally execute Python orchestrator here'); 
    // In a real implementation, you would call your Python orchestrator here 
  } 
 
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
 
// Try to start server on one of the ports in the range 
function tryPorts(ports, index = 0) { 
  if (index >= ports.length) { 
    console.error('ALL PORTS ARE IN USE! This is extremely unlikely.'); 
    process.exit(1); 
  } 
 
  const currentPort = ports[index]; 
ECHO is off.
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
tryPorts(portRange); 
