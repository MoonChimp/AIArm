const express = require('express');
const path = require('path');
const cors = require('cors');
const { spawn } = require('child_process');
const fs = require('fs');
const { NexusAssistant } = require('./nexus_assistant');
const adminFS = require('./nexus_admin_fs');
const alfaZer0 = require('./alfazer0_integration');
const nexusCore = require('./nexuscore');

// Initialize Nexus Assistant
const nexusAssistant = new NexusAssistant();

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
    // Check for test file request
    const lowerInput = input.toLowerCase();
    if (lowerInput.includes('test file') && 
        (lowerInput.includes('write') || lowerInput.includes('create') || lowerInput.includes('make')) && 
        (lowerInput.includes('filesystem') || lowerInput.includes('file system') || lowerInput.includes('capabilities'))) {
      
      // This is a request to create a test file
      // Generate a timestamp
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filePath = `D:/AIArm/Test/nexus_test_file_${timestamp}.txt`;
      const content = `This is a test file created by Nexus AI on ${new Date().toLocaleString()}.\n\nThis file demonstrates that Nexus has filesystem capabilities and can create files on your system.\n\nIf you can read this, the test was successful!`;
      
      // Ensure test directory exists
      const testDir = path.dirname(filePath);
      if (!fs.existsSync(testDir)) {
        fs.mkdirSync(testDir, { recursive: true });
      }
      
      // Write the file
      try {
        fs.writeFileSync(filePath, content, 'utf8');
        
        return res.json({
          success: true,
          response: `I've created a test file for you at ${filePath}.\n\nThis confirms that I have filesystem capabilities and can write files to your system.\n\nThe file contains a simple message confirming the test was successful.`,
          result: `Test file created at: ${filePath}`,
          path: filePath
        });
      } catch (writeError) {
        logMessage(`Error writing test file: ${writeError.message}`);
        
        return res.json({
          success: false,
          error: `Failed to write test file: ${writeError.message}`,
          response: `I encountered an error while trying to create a test file: ${writeError.message}. This could be due to permission issues or filesystem restrictions.`
        });
      }
    }
    
    // Check if this is a task execution confirmation
    if (req.body.confirmTask && req.body.taskId) {
    const taskResult = await nexusAssistant.executeTask(req.body.taskId);
    return res.json({
    success: true,
    response: taskResult.message,
    result: taskResult.result,
    taskExecuted: true,
    sessionId
    });
    }
            
            // Check for NexusCore operation
            const nexusCoreTask = nexusCore.detectAdminTask(input);
            if (nexusCoreTask.isAdminTask) {
              logMessage(`NexusCore task detected: ${nexusCoreTask.operation || 'adminCapabilities'}`);
              
              // If the operation is fully defined, execute it directly
              if (nexusCoreTask.operation && nexusCoreTask.operation !== 'adminCapabilities') {
                const result = nexusCore.processRequest({
                  operation: nexusCoreTask.operation,
                  path: nexusCoreTask.path,
                  command: nexusCoreTask.command,
                  content: nexusCoreTask.content
                });
                
                return res.json({
                  success: true,
                  response: nexusCoreTask.message || `Task completed: ${nexusCoreTask.operation}`,
                  result: result,
                  nexusCoreOperation: true,
                  sessionId
                });
              } else {
                // Return the capability message
                return res.json({
                  success: true,
                  response: nexusCoreTask.message || "I have administrative capabilities. How can I assist you?",
                  nexusCoreCapabilities: true,
                  sessionId
                });
              }
            }
    
    // For FileSystem agent, use special handling
    if (activeAgent === 'FileSystem') {
      return await handleFileSystemRequest(req, res, input, sessionId);
    }
    
    // For other agents, analyze if it's a task-like request first
    const analysisResult = nexusAssistant.analyzeInput(input);
    
    // If it looks like a task request, confirm with the user
    if (analysisResult.isTaskLike && activeAgent === 'orchestrator') {
      const confirmation = nexusAssistant.getConfirmationMessage(analysisResult.potentialTask);
      return res.json({
        success: true,
        response: confirmation.message,
        isTaskConfirmation: true,
        taskId: confirmation.taskId,
        sessionId
      });
    }
    
    // Otherwise, process through the normal bridge
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

// Handle FileSystem requests
async function handleFileSystemRequest(req, res, input, sessionId) {
  try {
    // Parse the natural language input to determine the file operation
    let operation = '';
    let params = {};
    
    // First, handle special case of just drive letters (e.g., "D:\", "C:\", etc.)
    if (/^[A-Za-z]:\\?$/.test(input.trim())) {
      operation = 'list_directory';
      params = { path: input.trim() };
    }
    // Then handle other commands
    else if (input.toLowerCase().startsWith('read ')) {
      operation = 'read_file';
      params = { path: input.substring(5).trim() };
    } else if (input.toLowerCase().startsWith('write ')) {
      // Format: write <path>: <content>
      const parts = input.substring(6).trim().split(':');
      if (parts.length >= 2) {
        const path = parts[0].trim();
        const content = parts.slice(1).join(':').trim();
        operation = 'write_file';
        params = { path, content };
      } else {
        return res.json({
          success: false,
          error: 'Invalid write format. Use: write <path>: <content>',
          response: 'I need both a file path and content. Please use the format: write <path>: <content>'
        });
      }
    } else if (input.toLowerCase().startsWith('append ')) {
      // Format: append <path>: <content>
      const parts = input.substring(7).trim().split(':');
      if (parts.length >= 2) {
        const path = parts[0].trim();
        const content = parts.slice(1).join(':').trim();
        operation = 'append_file';
        params = { path, content };
      } else {
        return res.json({
          success: false,
          error: 'Invalid append format. Use: append <path>: <content>',
          response: 'I need both a file path and content. Please use the format: append <path>: <content>'
        });
      }
    } else if (input.toLowerCase().startsWith('list ')) {
      operation = 'list_directory';
      params = { path: input.substring(5).trim() };
    } else if (input.toLowerCase().startsWith('mkdir ')) {
      operation = 'create_directory';
      params = { path: input.substring(6).trim() };
    } else if (input.toLowerCase().startsWith('delete file ')) {
      operation = 'delete_file';
      params = { path: input.substring(12).trim() };
    } else if (input.toLowerCase().startsWith('delete dir ')) {
      const parts = input.substring(11).trim().split(' ');
      const recursive = parts.length > 1 && parts[parts.length - 1].toLowerCase() === 'recursive';
      const path = recursive ? parts.slice(0, -1).join(' ') : parts.join(' ');
      operation = 'delete_directory';
      params = { path, recursive };
    } else if (input.toLowerCase().startsWith('move ')) {
      // Format: move <source> to <destination>
      const parts = input.substring(5).trim().split(' to ');
      if (parts.length === 2) {
        operation = 'move_file';
        params = { source: parts[0].trim(), destination: parts[1].trim() };
      } else {
        return res.json({
          success: false,
          error: 'Invalid move format. Use: move <source> to <destination>',
          response: 'I need both source and destination paths. Please use the format: move <source> to <destination>'
        });
      }
    } else if (input.toLowerCase().startsWith('copy ')) {
      // Format: copy <source> to <destination>
      const parts = input.substring(5).trim().split(' to ');
      if (parts.length === 2) {
        operation = 'copy_file';
        params = { source: parts[0].trim(), destination: parts[1].trim() };
      } else {
        return res.json({
          success: false,
          error: 'Invalid copy format. Use: copy <source> to <destination>',
          response: 'I need both source and destination paths. Please use the format: copy <source> to <destination>'
        });
      }
    } else if (input.toLowerCase().startsWith('info ')) {
      operation = 'get_file_info';
      params = { path: input.substring(5).trim() };
    } else if (input.toLowerCase().startsWith('search ')) {
      // Format: search <directory> for <pattern>
      const parts = input.substring(7).trim().split(' for ');
      if (parts.length === 2) {
        operation = 'search_files';
        params = { directory: parts[0].trim(), pattern: parts[1].trim() };
      } else {
        return res.json({
          success: false,
          error: 'Invalid search format. Use: search <directory> for <pattern>',
          response: 'I need both a directory and search pattern. Please use the format: search <directory> for <pattern>'
        });
      }
    } else if (input.toLowerCase().startsWith('cmd ')) {
      // Format: cmd <command>
      const command = input.substring(4).trim();
      operation = 'execute_command';
      params = { command };
    } else if (input.toLowerCase() === 'help') {
      // Show help message
      const helpMessage = `
**NexusAI FileSystem Commands:**

- **read <path>** - Read the contents of a file
- **write <path>: <content>** - Write content to a file
- **append <path>: <content>** - Append content to a file
- **list <path>** - List the contents of a directory
- **mkdir <path>** - Create a directory
- **delete file <path>** - Delete a file
- **delete dir <path> [recursive]** - Delete a directory (add 'recursive' to remove non-empty directories)
- **move <source> to <destination>** - Move a file or directory
- **copy <source> to <destination>** - Copy a file or directory
- **info <path>** - Get information about a file or directory
- **search <directory> for <pattern>** - Search for files matching a pattern
- **cmd <command>** - Execute a system command with administrative privileges
- **help** - Show this help message

You can also type a drive letter (e.g., "D:\\" or "C:\\") to list its contents directly.

All commands are executed with ADMINISTRATIVE PRIVILEGES, giving Nexus full access to the system.
`;
      
      return res.json({
        success: true,
        response: helpMessage
      });
    } else {
      // If not recognized, analyze if it looks like a file system task
      const analysisResult = nexusAssistant.analyzeInput(input);
      if (analysisResult.score >= 2 && 
          (analysisResult.detectedObject === 'file' ||
           analysisResult.detectedObject === 'folder' ||
           analysisResult.detectedObject === 'directory')) {
        // It looks like a file system request in natural language
        return res.json({
          success: true,
          response: `I understand you want to work with files or directories. Could you please use one of the specific file system commands? Type 'help' to see available commands.`
        });
      }
      
      return res.json({
        success: false,
        error: `Unknown command. Type 'help' for a list of available commands.`,
        response: `I don't recognize that command. Type 'help' to see a list of available file system commands.`
      });
    }
    
    // Make the API call to the admin filesystem endpoint
    const response = await fetch(`${req.protocol}://${req.get('host')}/api/admin-filesystem`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        operation,
        path: params.path || params.source,
        content: params.content,
        command: params.command
      })
    });
    
    if (response.ok) {
      const result = await response.json();
      
      if (result.success) {
        let responseMessage = '';
        
        switch (operation) {
          case 'read_file':
            responseMessage = `**File Content (${params.path}):**\n\n${result.output}`;
            break;
          case 'write_file':
            responseMessage = `I've successfully written to the file at ${params.path}`;
            break;
          case 'append_file':
            responseMessage = `I've successfully appended content to ${params.path}`;
            break;
          case 'list_directory':
            responseMessage = `**Directory Listing (${params.path}):**\n\n`;
            if (result.items && Array.isArray(result.items)) {
              result.items.forEach(item => {
                if (item && item.name) {
                  responseMessage += `${item.type === 'directory' ? '[DIR]' : '[FILE]'} ${item.name}\n`;
                }
              });
            } else {
              responseMessage += `Could not parse directory listing.\n`;
            }
            break;
          case 'create_directory':
            responseMessage = `I've successfully created the directory at ${params.path}`;
            break;
          case 'delete_file':
            responseMessage = `I've successfully deleted the file: ${params.path}`;
            break;
          case 'delete_directory':
            responseMessage = `I've successfully deleted the directory: ${params.path}`;
            break;
          case 'move_file':
            responseMessage = `I've successfully moved the item from ${params.source} to ${params.destination}`;
            break;
          case 'copy_file':
            responseMessage = `I've successfully copied from ${params.source} to ${params.destination}`;
            break;
          case 'get_file_info':
            responseMessage = `**File Information (${params.path}):**\n\n`;
            if (result.info) {
              responseMessage += `Type: ${result.info.is_directory ? 'Directory' : 'File'}\n`;
              responseMessage += `Size: ${result.info.size} bytes\n`;
              responseMessage += `Created: ${result.info.created}\n`;
              responseMessage += `Modified: ${result.info.modified}\n`;
              responseMessage += `Path: ${result.info.path}\n`;
              if (result.info.extension) {
                responseMessage += `Extension: ${result.info.extension}\n`;
              }
            } else {
              responseMessage += `Could not retrieve file information.\n`;
            }
            break;
          case 'search_files':
            responseMessage = `**Search Results (${params.pattern} in ${params.directory}):**\n\n`;
            if (result.matches && Array.isArray(result.matches)) {
              if (result.matches.length === 0) {
                responseMessage += 'No matches found.';
              } else {
                result.matches.forEach(item => {
                  responseMessage += `${item.type === 'directory' ? '[DIR]' : '[FILE]'} ${item.path}\n`;
                });
              }
            } else {
              responseMessage += `Could not parse search results.\n`;
            }
            break;
          case 'execute_command':
            responseMessage = `**Command Execution Result:**\n\n${result.output || 'Command executed successfully.'}`;
            break;
          default:
            responseMessage = `Operation completed successfully: ${operation}`;
        }
        
        return res.json({
          success: true,
          response: responseMessage,
          result: result
        });
      } else {
        return res.json({
          success: false,
          error: result.error,
          response: `I encountered an error: ${result.error}`
        });
      }
    } else {
      const errorData = await response.json();
      return res.json({
        success: false,
        error: errorData.error || 'Server returned an error',
        response: `I encountered a server error: ${errorData.message || errorData.error || 'Unknown error'}`
      });
    }
  } catch (error) {
    logMessage(`Error in handleFileSystemRequest: ${error.message}`);
    return res.json({
      success: false,
      error: error.message,
      response: `I encountered an error while processing your request: ${error.message}`
    });
  }
}

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

// FileSystem API endpoint
app.post('/api/filesystem', async (req, res) => {
  const { operation, ...params } = req.body;
  
  if (!operation) {
    return res.status(400).json({ success: false, error: 'Operation is required' });
  }
  
  try {
    logMessage(`FileSystem operation: ${operation} with params: ${JSON.stringify(params)}`);
    
    // Spawn Python process
    const pythonProcess = spawn('python', [
      path.join(__dirname, 'filesystem_operations.py'),
      '--input', JSON.stringify({ operation, ...params }),
      '--json'
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
      logMessage(`FileSystem error: ${data.toString()}`);
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      logMessage(`FileSystem process exited with code ${code}`);
      
      if (code !== 0) {
        logMessage(`Error output: ${errorData}`);
        return res.status(500).json({
          success: false,
          error: `FileSystem operation failed with code ${code}: ${errorData}`
        });
      }
      
      try {
        // Try to parse the JSON response
        const result = JSON.parse(outputData);
        res.json(result);
      } catch (jsonError) {
        logMessage(`Failed to parse JSON response: ${jsonError.message}`);
        logMessage(`Raw output: ${outputData}`);
        res.status(500).json({
          success: false,
          error: 'Failed to parse FileSystem response',
          result: outputData
        });
      }
    });
    
    // Handle process error
    pythonProcess.on('error', (error) => {
      logMessage(`FileSystem process error: ${error.message}`);
      res.status(500).json({
        success: false,
        error: `FileSystem process error: ${error.message}`
      });
    });
  } catch (error) {
    logMessage(`Error processing FileSystem request: ${error.message}`);
    res.status(500).json({
      success: false,
      error: `Failed to process FileSystem request: ${error.message}`
    });
  }
});

// AlfaZer0 Direct Integration endpoint
app.post('/api/alfazer0', async (req, res) => {
  const { operation, path: filePath, content, command, source, destination, directory, pattern,
          recursive, name, description, new_capability } = req.body;
  
  if (!operation) {
    return res.status(400).json({
      success: false,
      error: 'Operation is required'
    });
  }
  
  logMessage(`AlfaZer0 operation requested: ${operation}`);
  
  try {
    let result;
    
    switch (operation) {
      // Core filesystem operations
      case 'read_file':
        result = await alfaZer0.readFile(filePath);
        break;
      case 'write_file':
        result = await alfaZer0.writeFile(filePath, content);
        break;
      case 'append_file':
        result = await alfaZer0.appendFile(filePath, content);
        break;
      case 'list_directory':
        result = await alfaZer0.listDirectory(filePath);
        break;
      case 'create_directory':
        result = await alfaZer0.createDirectory(filePath);
        break;
      case 'delete_file':
        result = await alfaZer0.deleteFile(filePath);
        break;
      case 'delete_directory':
        result = await alfaZer0.deleteDirectory(filePath, recursive);
        break;
      case 'get_file_info':
        result = await alfaZer0.getFileInfo(filePath);
        break;
      case 'search_files':
        result = await alfaZer0.searchFiles(directory, pattern);
        break;
      case 'copy_file':
        result = await alfaZer0.copyFile(source, destination);
        break;
      case 'move_file':
        result = await alfaZer0.moveFile(source, destination);
        break;
      
      // System operations
      case 'execute_command':
        result = await alfaZer0.executeCommand(command);
        break;
      case 'get_system_info':
        result = await alfaZer0.getSystemInfo();
        break;
      
      // Self-expansion operations
      case 'create_script':
        result = await alfaZer0.createScript(name, description, content);
        break;
      case 'create_module':
        result = await alfaZer0.createModule(name, description, content);
        break;
      case 'store_knowledge':
        result = await alfaZer0.storeKnowledge(name, content);
        break;
      case 'update_index':
        result = await alfaZer0.updateIndex(new_capability);
        break;
        
      // Special operations
      case 'write_test_file':
        result = await alfaZer0.writeTestFile();
        break;
      
      default:
        return res.status(400).json({
          success: false,
          error: `Unknown operation: ${operation}`
        });
    }
    
    res.json(result);
  } catch (error) {
    logMessage(`Error in AlfaZer0 operation: ${error.message}`);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// NexusCore API endpoint
app.post('/api/nexuscore', async (req, res) => {
  const { operation, path: filePath, content, command } = req.body;
  
  if (!operation) {
    return res.status(400).json({
      success: false,
      error: 'Operation is required'
    });
  }
  
  logMessage(`NexusCore operation requested: ${operation}`);
  
  try {
    // Process the request through nexusCore
    const result = nexusCore.processRequest(req.body);
    res.json(result);
  } catch (error) {
    logMessage(`Error in NexusCore operation: ${error.message}`);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Admin filesystem operations endpoint
app.post('/api/admin-filesystem', async (req, res) => {
  const { operation, path: filePath, content, command } = req.body;
  
  if (!operation) {
    return res.status(400).json({
      success: false,
      error: 'Operation is required'
    });
  }
  
  logMessage(`Admin filesystem operation requested: ${operation}`);
  
  try {
    let result;
    
    switch (operation) {
      case 'write_file':
        if (!filePath || content === undefined) {
          return res.status(400).json({
            success: false,
            error: 'Path and content are required for write operation'
          });
        }
        result = await adminFS.writeFile(filePath, content);
        break;
        
      case 'read_file':
        if (!filePath) {
          return res.status(400).json({
            success: false,
            error: 'Path is required for read operation'
          });
        }
        result = await adminFS.readFile(filePath);
        break;
        
      case 'list_directory':
        if (!filePath) {
          return res.status(400).json({
            success: false,
            error: 'Path is required for list operation'
          });
        }
        result = await adminFS.listDirectory(filePath);
        break;
        
      case 'create_directory':
        if (!filePath) {
          return res.status(400).json({
            success: false,
            error: 'Path is required for create directory operation'
          });
        }
        result = await adminFS.createDirectory(filePath);
        break;
        
      case 'delete_file':
        if (!filePath) {
          return res.status(400).json({
            success: false,
            error: 'Path is required for delete operation'
          });
        }
        result = await adminFS.deleteFile(filePath);
        break;
        
      case 'execute_command':
        if (!command) {
          return res.status(400).json({
            success: false,
            error: 'Command is required for execute operation'
          });
        }
        result = await adminFS.executeCommand(command);
        break;
        
      default:
        return res.status(400).json({
          success: false,
          error: `Unknown operation: ${operation}`
        });
    }
    
    res.json(result);
  } catch (error) {
    logMessage(`Error in admin filesystem operation: ${error.message}`);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Direct test file creation endpoint for NexusCore
app.get('/api/nexuscore/test-file', async (req, res) => {
  logMessage('NexusCore test file creation requested');
  
  try {
    const result = nexusCore.createTestFile();
    
    if (result.success) {
      res.json({
        success: true,
        message: `Test file created at: ${result.path}`,
        path: result.path
      });
    } else {
      res.status(500).json({
        success: false,
        error: result.error || 'Failed to create test file',
        message: `Error creating test file: ${result.error || 'Unknown error'}`
      });
    }
  } catch (error) {
    logMessage(`Error in NexusCore test file creation: ${error.message}`);
    res.status(500).json({
      success: false,
      error: error.message,
      message: `Error creating test file: ${error.message}`
    });
  }
});

// Direct test file creation endpoint for AlfaZer0
app.get('/api/alfazer0/test-file', async (req, res) => {
  logMessage('AlfaZer0 test file creation requested');
  
  try {
    const result = await alfaZer0.writeTestFile();
    
    if (result.success) {
      res.json({
        success: true,
        message: result.message,
        path: result.path
      });
    } else {
      res.status(500).json({
        success: false,
        error: result.error || 'Failed to create test file',
        message: result.message || 'An error occurred while creating the test file'
      });
    }
  } catch (error) {
    logMessage(`Error in AlfaZer0 test file creation: ${error.message}`);
    res.status(500).json({
      success: false,
      error: error.message,
      message: `I encountered an error while trying to create the test file: ${error.message}`
    });
  }
});

// Direct file writing endpoint
app.post('/api/write-test-file', async (req, res) => {
  logMessage('Writing test file...');
  
  try {
    // Generate a timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filePath = `D:/AIArm/test_file_${timestamp}.txt`;
    const content = `This is a test file created by Nexus AI on ${new Date().toLocaleString()}.

This file demonstrates that Nexus has filesystem capabilities and can create files on your system.

If you can read this, the test was successful!`;
    
    // Execute the Python script directly
    const pythonProcess = spawn('python', [
      path.join(__dirname, 'nexus_direct_fs.py'),
      '--operation', 'write',
      '--path', filePath,
      '--content', content
    ]);
    
    let output = '';
    let errorOutput = '';
    
    // Collect standard output
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    // Collect error output
    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
      logMessage(`Error writing test file: ${data.toString()}`);
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      logMessage(`Test file writing process exited with code ${code}`);
      
      if (code === 0) {
        try {
          // Try to parse the JSON output
          const result = JSON.parse(output);
          
          if (result.success) {
            res.json({
              success: true,
              message: `I've successfully created a test file at: ${filePath}`,
              path: filePath
            });
          } else {
            res.json({
              success: false,
              error: result.error || 'Failed to write test file',
              message: `I encountered an error while trying to create the test file: ${result.error}`
            });
          }
        } catch (e) {
          res.json({
            success: false,
            error: 'Failed to parse output',
            message: 'I encountered an error while trying to create the test file.'
          });
        }
      } else {
        res.json({
          success: false,
          error: errorOutput || `Process exited with code ${code}`,
          message: `I encountered an error while trying to create the test file. The process exited with code ${code}.`
        });
      }
    });
    
    // Handle process error
    pythonProcess.on('error', (error) => {
      logMessage(`Error executing Python script: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message,
        message: `I encountered an error while trying to create the test file: ${error.message}`
      });
    });
  } catch (error) {
    logMessage(`Error in write-test-file endpoint: ${error.message}`);
    res.status(500).json({
      success: false,
      error: error.message,
      message: `I encountered an error while trying to create the test file: ${error.message}`
    });
  }
});

// Terminal command execution endpoint
app.post('/api/execute', async (req, res) => {
  const { command } = req.body;
  
  if (!command) {
    return res.status(400).json({
      success: false,
      error: 'Command is required'
    });
  }
  
  logMessage(`Executing command: ${command}`);
  
  try {
    // Execute the command
    const childProcess = spawn('cmd.exe', ['/c', command], {
      shell: true,
      cwd: process.cwd(),
      env: process.env
    });
    
    let output = '';
    let errorOutput = '';
    
    // Collect output
    childProcess.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    childProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    // Handle completion
    childProcess.on('close', (code) => {
      logMessage(`Command execution completed with code: ${code}`);
      
      if (code === 0) {
        res.json({
          success: true,
          output: output,
          command: command
        });
      } else {
        res.json({
          success: false,
          error: errorOutput || `Command exited with code ${code}`,
          output: output,
          command: command
        });
      }
    });
    
    // Handle error
    childProcess.on('error', (error) => {
      logMessage(`Command execution error: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message,
        command: command
      });
    });
  } catch (error) {
    logMessage(`Error executing command: ${error.message}`);
    res.status(500).json({
      success: false,
      error: error.message,
      command: command
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
