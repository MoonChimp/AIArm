const express = require('express');
const path = require('path');
const cors = require('cors');
const { spawn } = require('child_process');
const fs = require('fs');

// Create Express app
const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Parse command line arguments
const args = process.argv.slice(2);
let bridgeFile = 'improved_bridge.py';

// Check for --bridge argument
const bridgeIndex = args.indexOf('--bridge');
if (bridgeIndex !== -1 && args.length > bridgeIndex + 1) {
  bridgeFile = args[bridgeIndex + 1];
  console.log(`Using custom bridge: ${bridgeFile}`);
}

// Check for --port argument
const portIndex = args.indexOf('--port');
let customPort = null;
if (portIndex !== -1 && args.length > portIndex + 1) {
  customPort = parseInt(args[portIndex + 1]);
  console.log(`Using custom port: ${customPort}`);
}

// Define file paths
const bridgePath = path.join(__dirname, bridgeFile);

// Initialize response cache
const responseCache = {};

// Create logs directory if it doesn't exist
const logsDir = path.join(__dirname, 'Logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

// Log function
function logMessage(message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}\n`;
  
  fs.appendFile(path.join(logsDir, 'server.log'), logMessage, (err) => {
    if (err) console.error('Error writing to log:', err);
  });
  
  console.log(message);
}

// Process request through the Python bridge
function processThroughBridge(input, agent, userId = 'user') {
  return new Promise((resolve, reject) => {
    logMessage(`Processing request: "${input}" with agent: ${agent} for user: ${userId}`);
    
    // Spawn Python process with UTF-8 encoding
    const pythonProcess = spawn('python', [
      bridgePath,
      '--input', input,
      '--agent', agent,
      '--user', userId
    ], {
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });
    
    let outputData = '';
    let errorData = '';
    
    // Collect standard output
    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
    });
    
    // Collect error output
    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      logMessage(`Bridge error: ${data.toString()}`);
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      logMessage(`Bridge process exited with code ${code}`);
      
      if (code !== 0) {
        logMessage(`Error output: ${errorData}`);
        return reject(new Error(`Bridge exited with code ${code}: ${errorData}`));
      }
      
      try {
        // Try to parse the JSON response
        try {
          const result = JSON.parse(outputData);
          logMessage(`Received response: ${JSON.stringify(result).substring(0, 200)}...`);
          
          // Filter out any internal messages before returning
          if (result && typeof result === 'object') {
            // Remove any internal messages that shouldn't be visible to users
            delete result.claude_completions_in_artifacts_and_analysis_tool;
            delete result.long_conversation_reminder;
            delete result.election_info;
          }
          
          resolve(result);
        } catch (jsonError) {
          logMessage(`Failed to parse JSON response: ${jsonError.message}`);
          logMessage(`Raw output: ${outputData}`);
          
          // Try to extract any valid JSON from the output
          const jsonMatch = outputData.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            try {
              const extractedJson = JSON.parse(jsonMatch[0]);
              logMessage(`Successfully extracted JSON from output`);
              resolve(extractedJson);
            } catch (extractError) {
              // If extraction fails, return a formatted error
              resolve({
                success: false,
                error: 'Failed to parse orchestrator response',
                result: outputData
              });
            }
          } else {
            // If no JSON pattern found, return the raw output
            resolve({
              success: false,
              error: 'Failed to parse JSON response',
              result: outputData
            });
          }
        }
      } catch (error) {
        logMessage(`Failed to parse JSON: ${error.message}`);
        logMessage(`Raw output: ${outputData}`);
        resolve({ success: false, result: outputData, error: 'Failed to parse JSON response' });
      }
    });
    
    // Handle process error
    pythonProcess.on('error', (error) => {
      logMessage(`Bridge process error: ${error.message}`);
      reject(error);
    });
  });
}

// API Routes
app.get('/api/status', (req, res) => {
  logMessage('Status endpoint called');
  res.json({ 
    status: 'online',
    system: 'AIArm Crystalline Multi-Agent System (100% Local)',
    bridge: bridgeFile,
    backend: bridgeFile.includes('ollama') ? 'Local Ollama' : 'Python Orchestrator',
    agents: [
      'orchestrator',
      'research',
      'content',
      'design',
      'systems',
      'planning',
      'files',
      'reasoning',
      'code'
    ]
  });
});

app.post('/api/process', async (req, res) => {
  const { input, activeAgent, userId } = req.body;
  logMessage(`Process endpoint called with: ${JSON.stringify(req.body)}`);
  
  if (!input) {
    return res.status(400).json({ error: 'Input is required' });
  }
  
  // Generate a session ID from IP and user agent if not provided
  const sessionId = userId || req.headers['x-session-id'] || `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  try {
    // Process the request through the Python bridge
    const result = await processThroughBridge(input, activeAgent || 'orchestrator', sessionId);
    
    // Add the session ID to the response
    if (result && typeof result === 'object') {
      result.sessionId = sessionId;
    }
    
    res.json(result);
  } catch (error) {
    logMessage(`Error processing request: ${error.message}`);
    res.status(500).json({ 
      error: 'Failed to process request',
      message: error.message,
      fallback: 'The orchestrator is currently unavailable. Please check the logs for details.'
    });
  }
});

// Code Assistant API endpoints
app.get('/api/code-assistant/file', async (req, res) => {
  const { path } = req.query;
  
  if (!path) {
    return res.status(400).json({ success: false, error: 'Path is required' });
  }
  
  try {
    const fs = require('fs');
    const content = fs.readFileSync(path, 'utf8');
    
    res.json({
      success: true,
      path,
      content
    });
  } catch (error) {
    logMessage(`Error reading file ${path}: ${error.message}`);
    res.status(500).json({
      success: false,
      error: `Failed to read file: ${error.message}`
    });
  }
});

app.post('/api/code-assistant/save', async (req, res) => {
  const { path, content } = req.body;
  
  if (!path || content === undefined) {
    return res.status(400).json({ success: false, error: 'Path and content are required' });
  }
  
  try {
    const fs = require('fs');
    fs.writeFileSync(path, content, 'utf8');
    
    res.json({
      success: true,
      path
    });
  } catch (error) {
    logMessage(`Error saving file ${path}: ${error.message}`);
    res.status(500).json({
      success: false,
      error: `Failed to save file: ${error.message}`
    });
  }
});

app.post('/api/code-assistant/create', async (req, res) => {
  const { path, content } = req.body;
  
  if (!path) {
    return res.status(400).json({ success: false, error: 'Path is required' });
  }
  
  try {
    const fs = require('fs');
    
    // Check if file already exists
    if (fs.existsSync(path)) {
      return res.status(400).json({
        success: false,
        error: 'File already exists'
      });
    }
    
    // Create parent directories if they don't exist
    const dirname = require('path').dirname(path);
    if (!fs.existsSync(dirname)) {
      fs.mkdirSync(dirname, { recursive: true });
    }
    
    // Write the file
    fs.writeFileSync(path, content || '', 'utf8');
    
    res.json({
      success: true,
      path
    });
  } catch (error) {
    logMessage(`Error creating file ${path}: ${error.message}`);
    res.status(500).json({
      success: false,
      error: `Failed to create file: ${error.message}`
    });
  }
});

app.post('/api/code-assistant/query', async (req, res) => {
  const { query, context, sessionId } = req.body;
  
  if (!query) {
    return res.status(400).json({ success: false, error: 'Query is required' });
  }
  
  // Generate a unique session ID if not provided
  const userSessionId = sessionId || `code_assistant_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  try {
    // Forward to the appropriate agent based on request type
    let agentType = 'code';
    let forceEthicsResponse = false;
    
    // Direct handling for virus/malware questions
    if (/virus|malware|hack|exploit|attack|unauthorized access|breach|infect/i.test(query)) {
      agentType = 'code';
      forceEthicsResponse = true;
      logMessage(`Malicious software question detected, providing ethics guidance`);
    }
    // Detect if this is an ethics/compliance query
    else if (/ethic|guideline|compliance|legal|law|regulation|improper|proper|safety|security|privacy|rights|moral|guidelines|restriction|protected|sensitive|confidential|policies|standards|rule|protocol|framework|illegal|unauthorized|dangerous/i.test(query)) {
      agentType = 'code'; // Route ethics questions to Code Assistant which now has ethics handling
      logMessage(`Ethics/compliance question detected, routing to Code Assistant`);
    }
    // Detect if this is a design-related query
    else if (/design|ui|ux|interface|visual|layout|color|style|theme|appearance/i.test(query)) {
      agentType = 'design';
      logMessage(`Design question detected, routing to Visual Design Agent`);
    }
    
    let response;
    
    // If we're forcing an ethics response for malicious software questions
    if (forceEthicsResponse) {
      response = `# Ethics of Creating Malicious Software

Creating viruses, malware, or other malicious software is generally considered unethical and is often illegal for several important reasons:

## Ethical Considerations

1. **Potential for Harm**: Viruses and malware are designed to damage, disrupt, or gain unauthorized access to computer systems. This can lead to:
   - Loss of critical data
   - Privacy violations
   - Financial damage to individuals and organizations
   - Disruption of essential services

2. **Lack of Consent**: Malicious software typically operates without the knowledge or consent of the affected users, violating their autonomy and digital rights.

3. **Unpredictable Consequences**: Once released, malicious software can spread beyond intended targets and cause widespread, uncontrolled damage.

## Legal Implications

In most jurisdictions, creating and distributing malicious software is a criminal offense that can result in:
- Severe financial penalties
- Criminal charges under computer crime laws
- Imprisonment

## Legitimate Educational Contexts

There are limited contexts where studying malware is ethical:

1. **Security Research**: Cybersecurity professionals may analyze malware to develop better defenses and protections.

2. **Controlled Educational Environments**: Students may learn about malware concepts in isolated lab environments under proper supervision.

3. **Penetration Testing**: Security professionals may create tools to test systems with explicit permission and strict containment protocols.

However, these legitimate contexts always require:
- Proper authorization
- Isolated testing environments
- Clear ethical boundaries
- Responsible disclosure protocols
- Prevention of actual harm

## Ethical Alternatives

If you're interested in cybersecurity, consider these ethical alternatives:

1. Studying cybersecurity through legitimate educational resources and courses
2. Participating in authorized bug bounty programs
3. Contributing to open-source security tools
4. Practicing in dedicated sandbox environments designed for security training

The AIArm system is designed to promote ethical computing practices and cannot assist with creating malicious software for harmful purposes.`;
    } else {
      // Otherwise, process through the bridge
      const result = await processThroughBridge(query, agentType, userSessionId);
      
      // Get the response
      response = result.result || result.error || 'No response from Code Assistant';
    }
    
    // Remove internal Anthropic directives and comments
    response = response.replace(/<claude_completions_in_artifacts_and_analysis_tool>[\s\S]*?<\/claude_completions_in_artifacts_and_analysis_tool>/g, '');
    response = response.replace(/<election_info>[\s\S]*?<\/election_info>/g, '');
    response = response.replace(/<long_conversation_reminder>[\s\S]*?<\/long_conversation_reminder>/g, '');
    response = response.replace(/This function was added later to give Claude the ability to use a version of the Anthropic API\./g, '');
    response = response.replace(/This function was added later to give Claude/g, '');
    
    res.json({
      success: true,
      query,
      response: response
    });
  } catch (error) {
    logMessage(`Error processing code assistant query: ${error.message}`);
    res.status(500).json({
      success: false,
      error: `Failed to process query: ${error.message}`
    });
  }
});

// Serve the HTML interfaces
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/real_interface.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'real_interface.html'));
});

app.get('/simple_interface.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'real_interface.html')); // Use the real interface for simple interface path too
});

app.get('/code-assistant', (req, res) => {
  res.sendFile(path.join(__dirname, 'code_assistant.html'));
});

// Start the server
const PORT = process.env.PORT || customPort || 45678;

// Try to start on the specified port
app.listen(PORT, () => {
  logMessage(`AIArm Crystalline Interface server running on port ${PORT}`);
  logMessage(`Using bridge: ${bridgeFile}`);
  logMessage(`Backend: ${bridgeFile.includes('ollama') ? 'Local Ollama Models' : 'Python Orchestrator'}`);
  logMessage(`Open your browser and navigate to: http://localhost:${PORT}`);
});
