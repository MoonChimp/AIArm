const express = require('express');
const path = require('path');
const cors = require('cors');
const { spawn } = require('child_process');
const fs = require('fs');
const config = require('./config');
const errorHandler = require('./error_handler');
const systemMonitor = require('./system_monitor_module');

// Start system monitoring
systemMonitor.startMonitoring();

// Create Express app
const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Define bridge files for HRM architecture
let SURFACE_BRIDGE = 'improved_bridge.py'; // For improved surface interactions
let DEEP_BRIDGE = 'ollama_bridge.py';      // For deep thoughts and reasoning

// Parse command line arguments
const args = process.argv.slice(2);

// Check for --surface-bridge argument
const surfaceBridgeIndex = args.indexOf('--surface-bridge');
if (surfaceBridgeIndex !== -1 && args.length > surfaceBridgeIndex + 1) {
  SURFACE_BRIDGE = args[surfaceBridgeIndex + 1];
  console.log(`Using custom surface bridge: ${SURFACE_BRIDGE}`);
}

// Check for --deep-bridge argument
const deepBridgeIndex = args.indexOf('--deep-bridge');
if (deepBridgeIndex !== -1 && args.length > deepBridgeIndex + 1) {
  DEEP_BRIDGE = args[deepBridgeIndex + 1];
  console.log(`Using custom deep bridge: ${DEEP_BRIDGE}`);
}

// Check for --port argument
const portIndex = args.indexOf('--port');
let customPort = null;
if (portIndex !== -1 && args.length > portIndex + 1) {
  customPort = parseInt(args[portIndex + 1]);
  console.log(`Using custom port: ${customPort}`);
}

// Define file paths
const surfaceBridgePath = path.join(__dirname, SURFACE_BRIDGE);
const deepBridgePath = path.join(__dirname, DEEP_BRIDGE);

// Create logs directory if it doesn't exist
const logsDir = path.join(__dirname, 'Logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

// Log function - use the enhanced error handler
function logMessage(message, level = 'INFO', options = {}) {
  errorHandler.logMessage(message, level, options);
}

// Process request through the Surface bridge (improved_bridge.py)
function processThroughSurfaceBridge(input, agent, userId = 'user') {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    logMessage(`Processing through SURFACE bridge: "${input}" with agent: ${agent} for user: ${userId}`, 'INFO', { bridge: 'surface' });
    
    // Update pending requests count
    systemMonitor.updatePendingRequests('surface', systemMonitor.getMetrics().pendingRequests.surface + 1);
    
    // Set timeout for the bridge process
    const timeoutMs = config.timeoutMs || 120000;
    const timeoutId = setTimeout(() => {
      logMessage(`Surface bridge request timed out after ${timeoutMs/1000} seconds`, 'WARNING', { bridge: 'surface' });
      
      // If timeout strategy is 'graceful-degradation', we resolve with an error instead of rejecting
      if (config.requestTimeoutStrategy === 'graceful-degradation') {
        const timeoutResponse = {
          success: false,
          status: 'timeout',
          error: `Surface bridge request timed out after ${timeoutMs/1000} seconds`,
          result: 'The surface processing system took too long to respond.'
        };
        systemMonitor.trackRequest('surface', false, timeoutMs);
        systemMonitor.updatePendingRequests('surface', systemMonitor.getMetrics().pendingRequests.surface - 1);
        resolve(timeoutResponse);
      } else {
        // Otherwise, reject with timeout error
        systemMonitor.trackRequest('surface', false, timeoutMs);
        systemMonitor.updatePendingRequests('surface', systemMonitor.getMetrics().pendingRequests.surface - 1);
        reject(new Error(`Surface bridge request timed out after ${timeoutMs/1000} seconds`));
      }
      
      // Try to kill the process
      try {
        pythonProcess.kill();
      } catch (err) {
        // Ignore errors when killing the process
      }
    }, timeoutMs);
    
    // Prepare input as JSON for improved bridge compatibility
    const inputJson = JSON.stringify({
      input: input,
      agent: agent,
      user_id: userId
    });
    
    // Spawn Python process with UTF-8 encoding
    const pythonProcess = spawn('python', [
      surfaceBridgePath,
      '--input', inputJson,
      '--agent', agent,
      '--user', userId,
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
      logMessage(`Surface bridge error output: ${data.toString()}`, 'WARNING', { bridge: 'surface' });
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      // Clear the timeout
      clearTimeout(timeoutId);
      
      // Calculate response time
      const responseTime = Date.now() - startTime;
      
      // Update pending requests count
      systemMonitor.updatePendingRequests('surface', systemMonitor.getMetrics().pendingRequests.surface - 1);
      
      logMessage(`Surface bridge process exited with code ${code} in ${responseTime}ms`, 'INFO', { bridge: 'surface' });
      
      if (code !== 0) {
        logMessage(`Surface bridge error output: ${errorData}`, 'ERROR', { bridge: 'surface' });
        systemMonitor.trackRequest('surface', false, responseTime);
        return reject(new Error(`Surface bridge exited with code ${code}: ${errorData}`));
      }
      
      try {
        // Try to parse the JSON response
        try {
          const result = JSON.parse(outputData);
          logMessage(`Received surface response: ${JSON.stringify(result).substring(0, 200)}...`, 'INFO', { bridge: 'surface' });
          systemMonitor.trackRequest('surface', true, responseTime);
          resolve(result);
        } catch (jsonError) {
          logMessage(`Failed to parse surface JSON response: ${jsonError.message}`, 'ERROR', { bridge: 'surface', error: jsonError });
          logMessage(`Raw surface output: ${outputData}`, 'DEBUG', { bridge: 'surface' });
          
          // Try to extract any valid JSON from the output
          const jsonMatch = outputData.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            try {
              const extractedJson = JSON.parse(jsonMatch[0]);
              logMessage(`Successfully extracted JSON from surface output`, 'INFO', { bridge: 'surface' });
              systemMonitor.trackRequest('surface', true, responseTime);
              resolve(extractedJson);
            } catch (extractError) {
              // If extraction fails, return a formatted error
              logMessage(`Failed to extract JSON from surface output: ${extractError.message}`, 'ERROR', { bridge: 'surface', error: extractError });
              systemMonitor.trackRequest('surface', false, responseTime);
              resolve({
                success: false,
                error: 'Failed to parse surface bridge response',
                result: outputData
              });
            }
          } else {
            // If no JSON pattern found, return the raw output
            logMessage(`No JSON pattern found in surface output`, 'ERROR', { bridge: 'surface' });
            systemMonitor.trackRequest('surface', false, responseTime);
            resolve({
              success: false,
              error: 'Failed to parse surface JSON response',
              result: outputData
            });
          }
        }
      } catch (error) {
        logMessage(`Failed to process surface response: ${error.message}`, 'ERROR', { bridge: 'surface', error });
        logMessage(`Raw surface output: ${outputData}`, 'DEBUG', { bridge: 'surface' });
        systemMonitor.trackRequest('surface', false, responseTime);
        resolve({ 
          success: false, 
          result: outputData, 
          error: 'Failed to parse surface JSON response' 
        });
      }
    });
    
    // Handle process error
    pythonProcess.on('error', (error) => {
      // Clear the timeout
      clearTimeout(timeoutId);
      
      // Calculate response time
      const responseTime = Date.now() - startTime;
      
      // Update pending requests count
      systemMonitor.updatePendingRequests('surface', systemMonitor.getMetrics().pendingRequests.surface - 1);
      
      logMessage(`Surface bridge process error: ${error.message}`, 'ERROR', { bridge: 'surface', error });
      systemMonitor.trackRequest('surface', false, responseTime);
      reject(error);
    });
  });
}

// Process request through the Deep bridge (ollama_bridge.py)
function processThroughDeepBridge(input, agent, userId = 'user') {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    logMessage(`Processing through DEEP bridge: "${input}" with agent: ${agent} for user: ${userId}`, 'INFO', { bridge: 'deep' });
    
    // Update pending requests count
    systemMonitor.updatePendingRequests('deep', systemMonitor.getMetrics().pendingRequests.deep + 1);
    
    // Set timeout for the bridge process
    const timeoutMs = config.timeoutMs || 120000;
    const timeoutId = setTimeout(() => {
      logMessage(`Deep bridge request timed out after ${timeoutMs/1000} seconds`, 'WARNING', { bridge: 'deep' });
      
      // If timeout strategy is 'graceful-degradation', we resolve with an error instead of rejecting
      if (config.requestTimeoutStrategy === 'graceful-degradation') {
        const timeoutResponse = {
          success: false,
          status: 'timeout',
          error: `Deep bridge request timed out after ${timeoutMs/1000} seconds`,
          result: 'The deep reasoning system took too long to respond.'
        };
        systemMonitor.trackRequest('deep', false, timeoutMs);
        systemMonitor.updatePendingRequests('deep', systemMonitor.getMetrics().pendingRequests.deep - 1);
        resolve(timeoutResponse);
      } else {
        // Otherwise, reject with timeout error
        systemMonitor.trackRequest('deep', false, timeoutMs);
        systemMonitor.updatePendingRequests('deep', systemMonitor.getMetrics().pendingRequests.deep - 1);
        reject(new Error(`Deep bridge request timed out after ${timeoutMs/1000} seconds`));
      }
      
      // Try to kill the process
      try {
        pythonProcess.kill();
      } catch (err) {
        // Ignore errors when killing the process
      }
    }, timeoutMs);
    
    // Prepare input as JSON for improved bridge compatibility
    const inputJson = JSON.stringify({
      input: input,
      agent: agent,
      user_id: userId
    });
    
    // Spawn Python process with UTF-8 encoding
    const pythonProcess = spawn('python', [
      deepBridgePath,
      '--input', inputJson,
      '--agent', agent,
      '--user', userId,
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
      logMessage(`Deep bridge error output: ${data.toString()}`, 'WARNING', { bridge: 'deep' });
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      // Clear the timeout
      clearTimeout(timeoutId);
      
      // Calculate response time
      const responseTime = Date.now() - startTime;
      
      // Update pending requests count
      systemMonitor.updatePendingRequests('deep', systemMonitor.getMetrics().pendingRequests.deep - 1);
      
      logMessage(`Deep bridge process exited with code ${code} in ${responseTime}ms`, 'INFO', { bridge: 'deep' });
      
      if (code !== 0) {
        logMessage(`Deep bridge error output: ${errorData}`, 'ERROR', { bridge: 'deep' });
        systemMonitor.trackRequest('deep', false, responseTime);
        return reject(new Error(`Deep bridge exited with code ${code}: ${errorData}`));
      }
      
      try {
        // Try to parse the JSON response
        try {
          const result = JSON.parse(outputData);
          logMessage(`Received deep response: ${JSON.stringify(result).substring(0, 200)}...`, 'INFO', { bridge: 'deep' });
          systemMonitor.trackRequest('deep', true, responseTime);
          resolve(result);
        } catch (jsonError) {
          logMessage(`Failed to parse deep JSON response: ${jsonError.message}`, 'ERROR', { bridge: 'deep', error: jsonError });
          logMessage(`Raw deep output: ${outputData}`, 'DEBUG', { bridge: 'deep' });
          
          // Try to extract any valid JSON from the output
          const jsonMatch = outputData.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            try {
              const extractedJson = JSON.parse(jsonMatch[0]);
              logMessage(`Successfully extracted JSON from deep output`, 'INFO', { bridge: 'deep' });
              systemMonitor.trackRequest('deep', true, responseTime);
              resolve(extractedJson);
            } catch (extractError) {
              // If extraction fails, return a formatted error
              logMessage(`Failed to extract JSON from deep output: ${extractError.message}`, 'ERROR', { bridge: 'deep', error: extractError });
              systemMonitor.trackRequest('deep', false, responseTime);
              resolve({
                success: false,
                error: 'Failed to parse deep bridge response',
                result: outputData
              });
            }
          } else {
            // If no JSON pattern found, return the raw output
            logMessage(`No JSON pattern found in deep output`, 'ERROR', { bridge: 'deep' });
            systemMonitor.trackRequest('deep', false, responseTime);
            resolve({
              success: false,
              error: 'Failed to parse deep JSON response',
              result: outputData
            });
          }
        }
      } catch (error) {
        logMessage(`Failed to process deep response: ${error.message}`, 'ERROR', { bridge: 'deep', error });
        logMessage(`Raw deep output: ${outputData}`, 'DEBUG', { bridge: 'deep' });
        systemMonitor.trackRequest('deep', false, responseTime);
        resolve({ 
          success: false, 
          result: outputData, 
          error: 'Failed to parse deep JSON response' 
        });
      }
    });
    
    // Handle process error
    pythonProcess.on('error', (error) => {
      // Clear the timeout
      clearTimeout(timeoutId);
      
      // Calculate response time
      const responseTime = Date.now() - startTime;
      
      // Update pending requests count
      systemMonitor.updatePendingRequests('deep', systemMonitor.getMetrics().pendingRequests.deep - 1);
      
      logMessage(`Deep bridge process error: ${error.message}`, 'ERROR', { bridge: 'deep', error });
      systemMonitor.trackRequest('deep', false, responseTime);
      reject(error);
    });
  });
}

// Process request through both bridges and combine the results
async function processConcurrently(input, agent, userId = 'user') {
  const startTime = Date.now();
  logMessage(`Processing request concurrently through both bridges: "${input}" with agent: ${agent} for user: ${userId}`, 'INFO');
  
  try {
    // Call both bridges concurrently
    const [surfaceResult, deepResult] = await Promise.all([
      processThroughSurfaceBridge(input, agent, userId)
        .catch(error => {
          logMessage(`Surface bridge error: ${error.message}`, 'ERROR', { bridge: 'surface', error });
          return { 
            success: false, 
            status: "error", 
            error: `Surface bridge error: ${error.message}`,
            result: "The surface processing system encountered an issue."
          };
        }),
      processThroughDeepBridge(input, agent, userId)
        .catch(error => {
          logMessage(`Deep bridge error: ${error.message}`, 'ERROR', { bridge: 'deep', error });
          return { 
            success: false, 
            status: "error", 
            error: `Deep bridge error: ${error.message}`,
            result: "The deep reasoning system encountered an issue."
          };
        })
    ]);
    
    // Calculate total response time
    const responseTime = Date.now() - startTime;
    
    logMessage(`Received responses from both bridges in ${responseTime}ms, combining results`, 'INFO');
    
    // If both bridges failed, return a combined error
    if (!surfaceResult.success && !deepResult.success) {
      logMessage(`Both bridges failed to process the request`, 'ERROR');
      return {
        success: false,
        status: "error",
        error: "Both bridges failed to process the request",
        surface_error: surfaceResult.error,
        deep_error: deepResult.error,
        result: "I apologize, but both processing systems encountered issues. Please try again."
      };
    }
    
    // Get the configured combination method
    const combinationMethod = config.responseConfig?.combinationMethod || 'augment-surface';
    const similarityThreshold = config.responseConfig?.similarityThreshold || 0.5;
    const preferDeepDomains = config.responseConfig?.preferDeepForDomains || [];
    
    // Check if we should prefer deep reasoning for this type of query
    const shouldPreferDeep = preferDeepDomains.some(domain => {
      return input.toLowerCase().includes(domain.toLowerCase());
    });
    
    // Combine the results
    let combinedResult = {
      success: true,
      status: "completed",
      bridge_type: "concurrent_hrm",
      surface_success: surfaceResult.success || false,
      deep_success: deepResult.success || false,
      response_time_ms: responseTime
    };
    
    // Add surface result details
    if (surfaceResult.success) {
      combinedResult.surface_result = surfaceResult.result;
      combinedResult.surface_thought_id = surfaceResult.thought_id;
    } else {
      combinedResult.surface_error = surfaceResult.error;
    }
    
    // Add deep result details
    if (deepResult.success) {
      combinedResult.deep_result = deepResult.result;
      combinedResult.deep_thought_id = deepResult.thought_id;
    } else {
      combinedResult.deep_error = deepResult.error;
    }
    
    // Combine the responses for the user based on the configured method
    if (surfaceResult.success && !deepResult.success) {
      logMessage(`Using surface response only (deep bridge failed)`, 'INFO');
      combinedResult.result = surfaceResult.result;
      combinedResult.combination_method = 'surface-only';
    } else if (!surfaceResult.success && deepResult.success) {
      logMessage(`Using deep response only (surface bridge failed)`, 'INFO');
      combinedResult.result = deepResult.result;
      combinedResult.combination_method = 'deep-only';
    } else if (surfaceResult.success && deepResult.success) {
      // If both succeeded, use the configured combination method
      if (shouldPreferDeep) {
        logMessage(`Preferring deep response for domain-specific query`, 'INFO');
        combinationMethod = 'prefer-deep';
      }
      
      logMessage(`Using combination method: ${combinationMethod}`, 'INFO');
      combinedResult.combination_method = combinationMethod;
      
      if (combinationMethod === 'prefer-surface') {
        // Use surface result with minimal deep integration
        combinedResult.result = surfaceResult.result;
      } else if (combinationMethod === 'prefer-deep') {
        // Use deep result with minimal surface integration
        combinedResult.result = deepResult.result;
      } else if (combinationMethod === 'augment-surface') {
        // For user interaction, emphasize the structured surface response
        // but incorporate deep insights from the deep reasoning system
        const surfaceResult1 = surfaceResult.result || surfaceResult.response || '';
        const deepResult1 = deepResult.result || deepResult.response || '';
        
        const surfaceLines = typeof surfaceResult1 === 'string' ? surfaceResult1.split("\n") : [];
        const deepLines = typeof deepResult1 === 'string' ? deepResult1.split("\n") : [];
        
        // Get the first paragraph from surface (structured response)
        let surfaceIntro = "";
        for (let i = 0; i < surfaceLines.length && surfaceIntro.length < 500; i++) {
          if (surfaceLines[i].trim()) {
            surfaceIntro += surfaceLines[i] + "\n";
          }
        }
        
        // Get insights from deep reasoning
        let deepInsights = "";
        let insightFound = false;
        for (let i = 0; i < deepLines.length; i++) {
          const line = deepLines[i];
          if (line.includes("insight") || line.includes("analysis") || line.includes("consider") || 
              line.includes("perspective") || line.includes("approach") || line.includes("thinking")) {
            insightFound = true;
            deepInsights += line + "\n";
            
            // Get the next few lines of context
            for (let j = 1; j <= 3 && i + j < deepLines.length; j++) {
              if (deepLines[i + j].trim()) {
                deepInsights += deepLines[i + j] + "\n";
              }
            }
          }
        }
        
        // If no specific insights were found, take a portion of the deep response
        if (!insightFound) {
          deepInsights = deepLines.slice(0, Math.min(5, deepLines.length)).join("\n");
        }
        
        // Combine the results
        combinedResult.result = `${surfaceIntro.trim()}\n\n${deepInsights.trim()}`;
      } else if (combinationMethod === 'augment-deep') {
        // Emphasize deep reasoning but incorporate structured info from surface
        const surfaceResult1 = surfaceResult.result || surfaceResult.response || '';
        const deepResult1 = deepResult.result || deepResult.response || '';
        
        const surfaceLines = typeof surfaceResult1 === 'string' ? surfaceResult1.split("\n") : [];
        const deepLines = typeof deepResult1 === 'string' ? deepResult1.split("\n") : [];
        
        // Use the deep response as the primary content
        let combinedContent = deepResult1;
        
        // Try to extract structured information from the surface response
        const structuredInfo = [];
        let inStructuredSection = false;
        
        for (let i = 0; i < surfaceLines.length; i++) {
          const line = surfaceLines[i].trim();
          
          // Look for lists, technical details, or structured content
          if (line.startsWith('-') || line.startsWith('*') || line.startsWith('#') ||
              line.startsWith('|') || line.startsWith('1.') || 
              line.includes(':') || line.includes('=')) {
            
            structuredInfo.push(line);
            inStructuredSection = true;
          } else if (inStructuredSection && line) {
            // Continue capturing the current structured section
            structuredInfo.push(line);
          } else {
            inStructuredSection = false;
          }
        }
        
        // If we found structured content, append it
        if (structuredInfo.length > 0) {
          combinedContent += "\n\nAdditional Information:\n" + structuredInfo.join("\n");
        }
        
        combinedResult.result = combinedContent;
      } else {
        // Default to simple concatenation
        combinedResult.result = `${surfaceResult.result}\n\n${deepResult.result}`;
      }
    } else {
      // This should never happen since we checked for both failing above
      logMessage(`Unexpected condition: both bridges reported failure but didn't trigger error handler`, 'ERROR');
      combinedResult.result = "I apologize, but I encountered an issue processing your request.";
    }
    
    return combinedResult;
    
  } catch (error) {
    logMessage(`Error in concurrent processing: ${error.message}`, 'ERROR', { error });
    
    // Use errorHandler to properly handle the error
    const errorResponse = errorHandler.handleBridgeError('concurrent', error, { input, agent, userId });
    errorResponse.result = "I apologize, but I encountered an unexpected issue while processing your request. Please try again.";
    
    return errorResponse;
  }
}

// API Routes
app.get('/api/status', (req, res) => {
  logMessage('Status endpoint called', 'INFO', { endpoint: '/api/status' });
  
  // Get system metrics
  const metrics = systemMonitor.getMetrics();
  const health = systemMonitor.getHealthStatus();
  
  res.json({ 
    status: health.healthy ? 'online' : 'degraded',
    system: 'AIArm HRM Architecture (Human-Robot-Machine)',
    architecture: 'concurrent_bridges',
    environment: config.environment,
    uptime: metrics.uptime,
    started_at: new Date(metrics.startTime).toISOString(),
    timestamp: new Date().toISOString(),
    surface_bridge: {
      name: SURFACE_BRIDGE,
      status: health.bridgeStatus.surface ? 'running' : 'not_running',
      backend: 'Python Orchestrator'
    },
    deep_bridge: {
      name: DEEP_BRIDGE,
      status: health.bridgeStatus.deep ? 'running' : 'not_running',
      backend: 'Local Ollama Models'
    },
    inner_life: {
      enabled: config.innerLifeEnabled,
      status: health.innerLifeStatus.running ? 'running' : 'not_running'
    },
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
    ],
    specialized_agents: [
      'WebSearch',
      'PhotoGeneration',
      'VideoGeneration',
      'WebsiteCreation'
    ],
    metrics: {
      pendingRequests: metrics.pendingRequests,
      requestStats: metrics.requestStats,
      memoryUsage: metrics.memoryUsage,
      cpuUsage: metrics.cpuUsage
    },
    alerts: health.alerts
  });
});

app.post('/api/process', async (req, res) => {
  const { input, activeAgent, userId } = req.body;
  logMessage(`Process endpoint called with: ${JSON.stringify(req.body)}`, 'INFO', { endpoint: '/api/process' });
  
  if (!input) {
    return res.status(400).json({ error: 'Input is required' });
  }
  
  // Generate a session ID from IP and user agent if not provided
  const sessionId = userId || req.headers['x-session-id'] || `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  // Apply rate limiting if enabled
  if (config.rateLimiting?.enabled) {
    // Simple IP-based rate limiting - in a production system you'd use a proper rate limiter middleware
    const clientIp = req.ip || req.connection.remoteAddress;
    const ipKey = `ratelimit:${clientIp}`;
    const currentRequests = req.app.locals[ipKey] || 0;
    
    if (currentRequests >= (config.rateLimiting.maxRequests || 100)) {
      logMessage(`Rate limit exceeded for IP: ${clientIp}`, 'WARNING', { endpoint: '/api/process' });
      return res.status(429).json({ 
        error: 'Too many requests',
        message: 'Rate limit exceeded. Please try again later.',
        retry_after: 60 // seconds
      });
    }
    
    // Increment request count
    req.app.locals[ipKey] = currentRequests + 1;
    
    // Reset after window
    setTimeout(() => {
      req.app.locals[ipKey] = Math.max(0, (req.app.locals[ipKey] || 0) - 1);
    }, config.rateLimiting.windowMs || 15 * 60 * 1000);
  }
  
  try {
    // Process the request through both bridges concurrently
    const result = await processConcurrently(input, activeAgent || 'orchestrator', sessionId);
    
    // Add the session ID and timestamp to the response
    if (result && typeof result === 'object') {
      result.sessionId = sessionId;
      result.timestamp = new Date().toISOString();
    }
    
    // Cache result if caching is enabled and successful
    if (config.caching?.enabled && result.success) {
      // In a real implementation, you'd use a proper cache like Redis
      // This is a simplified in-memory cache
      const cacheKey = `cache:${input}:${activeAgent || 'orchestrator'}`;
      app.locals[cacheKey] = {
        result: result,
        timestamp: Date.now(),
        ttl: config.caching.ttl || 3600 // seconds
      };
    }
    
    res.json(result);
  } catch (error) {
    // Use the error handler to properly handle the error
    errorHandler.handleApiError(req, res, error, {
      statusCode: 500,
      publicMessage: 'Failed to process request',
      context: { input, activeAgent, userId: sessionId }
    });
  }
});

// Agent API Routes
app.post('/api/agent', async (req, res) => {
  const { agent, action, data, userId } = req.body;
  logMessage(`Agent endpoint called with: ${JSON.stringify(req.body)}`);
  
  if (!agent || !action) {
    return res.status(400).json({ error: 'Agent and action are required' });
  }
  
  // Generate a session ID if not provided
  const sessionId = userId || req.headers['x-session-id'] || `agent_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  try {
    // For specialized agent operations, we route directly to the deep bridge (ollama)
    // which has access to the agent manager
    const agentRequest = {
      agent: agent,
      action: action,
      data: data || {}
    };
    
    // Convert to JSON string and send to the deep bridge
    const result = await processThroughDeepBridge(
      JSON.stringify(agentRequest), 
      'agent_manager', 
      sessionId
    );
    
    // Add the session ID to the response
    if (result && typeof result === 'object') {
      result.sessionId = sessionId;
    }
    
    res.json(result);
  } catch (error) {
    logMessage(`Error processing agent request: ${error.message}`);
    res.status(500).json({ 
      error: 'Failed to process agent request',
      message: error.message,
      fallback: 'The agent system is currently unavailable. Please check the logs for details.'
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

// Website Creation Agent endpoints
app.post('/api/website-creation', async (req, res) => {
  const { specification, options, userId } = req.body;
  logMessage(`Website Creation endpoint called with specification length: ${specification?.length || 0}`);
  
  if (!specification) {
    return res.status(400).json({ error: 'Website specification is required' });
  }
  
  // Generate a session ID if not provided
  const sessionId = userId || req.headers['x-session-id'] || `website_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  try {
    // Create agent request
    const agentRequest = {
      agent: "WebsiteCreation",
      action: "process",
      data: {
        input: specification,
        options: options || {}
      }
    };
    
    // Send to the deep bridge
    const result = await processThroughDeepBridge(
      JSON.stringify(agentRequest), 
      'agent_manager', 
      sessionId
    );
    
    // Add the session ID to the response
    if (result && typeof result === 'object') {
      result.sessionId = sessionId;
    }
    
    res.json(result);
  } catch (error) {
    logMessage(`Error processing website creation request: ${error.message}`);
    res.status(500).json({ 
      error: 'Failed to process website creation request',
      message: error.message,
      fallback: 'The website creation system is currently unavailable. Please check the logs for details.'
    });
  }
});

// Photo Generation Agent endpoints
app.post('/api/photo-generation', async (req, res) => {
  const { prompt, options, userId } = req.body;
  logMessage(`Photo Generation endpoint called with prompt: ${prompt}`);
  
  if (!prompt) {
    return res.status(400).json({ error: 'Image prompt is required' });
  }
  
  // Generate a session ID if not provided
  const sessionId = userId || req.headers['x-session-id'] || `photo_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  try {
    // Use dedicated photo_generation_bridge for better image generation
    const photoBridgePath = path.join(__dirname, 'photo_generation_bridge.py');
    
    // Prepare input as JSON
    const inputJson = JSON.stringify({
      input: prompt,
      options: options || {}
    });
    
    logMessage(`Running photo generation bridge with prompt: ${prompt}`);
    
    // Spawn Python process with UTF-8 encoding
    const pythonProcess = spawn('python', [
      photoBridgePath,
      '--input', inputJson,
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
      logMessage(`Photo generation bridge error: ${data.toString()}`, 'WARNING');
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      logMessage(`Photo generation bridge process exited with code ${code}`);
      
      if (code !== 0) {
        logMessage(`Photo generation bridge error: ${errorData}`, 'ERROR');
        return res.status(500).json({ 
          error: 'Failed to process photo generation request',
          message: errorData,
          success: false
        });
      }
      
      try {
        // Parse the JSON response
        const result = JSON.parse(outputData);
        logMessage(`Received photo generation result: ${JSON.stringify(result).substring(0, 200)}...`);
        
        // Add the session ID to the response
        if (result && typeof result === 'object') {
          result.sessionId = sessionId;
        }
        
        res.json(result);
      } catch (jsonError) {
        logMessage(`Failed to parse photo generation JSON response: ${jsonError.message}`, 'ERROR');
        logMessage(`Raw output: ${outputData}`, 'DEBUG');
        res.status(500).json({ 
          error: 'Failed to parse photo generation response',
          message: jsonError.message,
          raw: outputData,
          success: false
        });
      }
    });
    
    // Handle process error
    pythonProcess.on('error', (error) => {
      logMessage(`Photo generation bridge process error: ${error.message}`, 'ERROR');
      res.status(500).json({ 
        error: 'Failed to start photo generation process',
        message: error.message,
        success: false
      });
    });
  } catch (error) {
    logMessage(`Error processing photo generation request: ${error.message}`, 'ERROR');
    res.status(500).json({ 
      error: 'Failed to process photo generation request',
      message: error.message,
      success: false
    });
  }
});

// Video Generation Agent endpoints
app.post('/api/video-generation', async (req, res) => {
  const { script, options, userId } = req.body;
  logMessage(`Video Generation endpoint called with script length: ${script?.length || 0}`);
  
  if (!script) {
    return res.status(400).json({ error: 'Video script is required' });
  }
  
  // Generate a session ID if not provided
  const sessionId = userId || req.headers['x-session-id'] || `video_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  try {
    // Create agent request
    const agentRequest = {
      agent: "VideoGeneration",
      action: "process",
      data: {
        input: script,
        options: options || {}
      }
    };
    
    // Send to the deep bridge
    const result = await processThroughDeepBridge(
      JSON.stringify(agentRequest), 
      'agent_manager', 
      sessionId
    );
    
    // Add the session ID to the response
    if (result && typeof result === 'object') {
      result.sessionId = sessionId;
    }
    
    res.json(result);
  } catch (error) {
    logMessage(`Error processing video generation request: ${error.message}`);
    res.status(500).json({ 
      error: 'Failed to process video generation request',
      message: error.message,
      fallback: 'The video generation system is currently unavailable. Please check the logs for details.'
    });
  }
});

// Web Search Agent endpoints
app.post('/api/web-search', async (req, res) => {
  const { query, options, userId } = req.body;
  logMessage(`Web Search endpoint called with query: ${query}`);
  
  if (!query) {
    return res.status(400).json({ error: 'Search query is required' });
  }
  
  // Generate a session ID if not provided
  const sessionId = userId || req.headers['x-session-id'] || `search_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  
  try {
    // Create agent request
    const agentRequest = {
      agent: "WebSearch",
      action: "process",
      data: {
        input: query,
        options: options || {}
      }
    };
    
    // Send to the deep bridge
    const result = await processThroughDeepBridge(
      JSON.stringify(agentRequest), 
      'agent_manager', 
      sessionId
    );
    
    // Add the session ID to the response
    if (result && typeof result === 'object') {
      result.sessionId = sessionId;
    }
    
    res.json(result);
  } catch (error) {
    logMessage(`Error processing web search request: ${error.message}`);
    res.status(500).json({ 
      error: 'Failed to process web search request',
      message: error.message,
      fallback: 'The web search system is currently unavailable. Please check the logs for details.'
    });
  }
});

// Filesystem API endpoints
app.post('/api/filesystem', async (req, res) => {
  const request = req.body;
  logMessage(`Filesystem endpoint called with operation: ${request.operation}`);
  
  try {
    // Use filesystem_operations.py to handle the request
    const fsOperationsPath = path.join(__dirname, 'filesystem_operations.py');
    
    // Prepare input as JSON
    const inputJson = JSON.stringify(request);
    
    logMessage(`Running filesystem operations with request: ${JSON.stringify(request)}`);
    
    // Spawn Python process with UTF-8 encoding
    const pythonProcess = spawn('python', [
      fsOperationsPath,
      '--input', inputJson,
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
      logMessage(`Filesystem operations error: ${data.toString()}`, 'WARNING');
    });
    
    // Handle process completion
    pythonProcess.on('close', (code) => {
      logMessage(`Filesystem operations process exited with code ${code}`);
      
      if (code !== 0) {
        logMessage(`Filesystem operations error: ${errorData}`, 'ERROR');
        return res.status(500).json({ 
          success: false,
          error: 'Failed to process filesystem operation',
          message: errorData
        });
      }
      
      try {
        // Parse the JSON response
        const result = JSON.parse(outputData);
        logMessage(`Received filesystem operation result: ${JSON.stringify(result).substring(0, 200)}...`);
        
        res.json(result);
      } catch (jsonError) {
        logMessage(`Failed to parse filesystem operations JSON response: ${jsonError.message}`, 'ERROR');
        logMessage(`Raw output: ${outputData}`, 'DEBUG');
        res.status(500).json({ 
          success: false,
          error: 'Failed to parse filesystem operations response',
          message: jsonError.message,
          raw: outputData
        });
      }
    });
    
    // Handle process error
    pythonProcess.on('error', (error) => {
      logMessage(`Filesystem operations process error: ${error.message}`, 'ERROR');
      res.status(500).json({ 
        success: false,
        error: 'Failed to start filesystem operations process',
        message: error.message
      });
    });
  } catch (error) {
    logMessage(`Error processing filesystem operation request: ${error.message}`, 'ERROR');
    res.status(500).json({ 
      success: false,
      error: 'Failed to process filesystem operation request',
      message: error.message
    });
  }
});

// Filesystem capabilities endpoints
app.get('/api/filesystem/capabilities', (req, res) => {
  res.json({
    success: true,
    capabilities: [
      'read_file',
      'write_file',
      'append_file',
      'list_directory',
      'create_directory',
      'delete_file',
      'delete_directory',
      'move_file',
      'copy_file',
      'get_file_info',
      'search_files'
    ]
  });
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

// Health check endpoint
app.get('/health', (req, res) => {
  logMessage('Health check endpoint called', 'INFO', { endpoint: '/health' });
  
  // Get system health status
  const health = systemMonitor.getHealthStatus();
  
  // Set appropriate HTTP status code
  const statusCode = health.healthy ? 200 : 503; // 503 Service Unavailable
  
  res.status(statusCode).json(health);
});

// System monitor endpoint for detailed status
app.get('/api/system-monitor', (req, res) => {
  logMessage('System monitor endpoint called', 'INFO', { endpoint: '/api/system-monitor' });
  
  // Get comprehensive system metrics
  const metrics = systemMonitor.getMetrics();
  const health = systemMonitor.getHealthStatus();
  const errorStats = errorHandler.getErrorStats();
  
  // Get system status
  const status = {
    status: health.healthy ? 'online' : 'degraded',
    system: 'AIArm HRM Architecture (Human-Robot-Machine)',
    architecture: 'concurrent_bridges',
    environment: config.environment,
    surface_bridge: {
    name: SURFACE_BRIDGE,
    status: health.bridgeStatus.surface ? 'running' : 'not_running',
    backend: 'Python Orchestrator',
    stats: metrics.bridgeStats.surface
    },
    deep_bridge: {
    name: DEEP_BRIDGE,
    status: health.bridgeStatus.deep ? 'running' : 'not_running',
    backend: 'Local Ollama Models',
    stats: metrics.bridgeStats.deep
    },
    inner_life: {
      enabled: config.innerLifeEnabled,
      status: health.innerLifeStatus.running ? 'running' : 'not_running',
      directory: config.innerLifeDirectory
    },
    server: {
      uptime: metrics.uptime,
      started_at: new Date(metrics.startTime).toISOString(),
      memory_usage: metrics.memoryUsage,
      cpu_usage: metrics.cpuUsage,
      node_version: process.version,
      platform: process.platform,
      pending_requests: metrics.pendingRequests,
      request_stats: metrics.requestStats
    },
    error_stats: errorStats,
    alerts: health.alerts,
    configuration: {
      environment: config.environment,
      logging: {
        level: config.logLevel,
        file_logging: config.logToFile,
        directory: config.logDirectory
      },
      memory: {
        enabled: config.memoryEnabled,
        directory: config.memoryDirectory
      },
      caching: {
        enabled: config.caching?.enabled,
        ttl: config.caching?.ttl
      },
      timeout_ms: config.timeoutMs,
      rate_limiting: config.rateLimiting?.enabled
    },
    timestamp: new Date().toISOString()
  };
  
  // Save status to file for external monitoring
  try {
    fs.writeFileSync(path.join(__dirname, 'service_status.txt'), JSON.stringify(status, null, 2));
  } catch (error) {
    logMessage(`Error writing status file: ${error.message}`, 'ERROR', { error });
  }
  
  res.json(status);
});

// Add the /api/errors endpoint for authorized users to view error statistics
app.get('/api/errors', (req, res) => {
  // Add basic auth check for production
  if (config.isProd) {
    const auth = req.headers.authorization;
    if (!auth || auth !== 'Bearer admin-token') { // In production, use a proper auth mechanism
      return res.status(401).json({ error: 'Unauthorized' });
    }
  }
  
  const errorStats = errorHandler.getErrorStats();
  res.json(errorStats);
});

// Add error handling middleware
app.use((err, req, res, next) => {
  errorHandler.handleApiError(req, res, err, {
    statusCode: 500,
    publicMessage: 'Internal server error'
  });
});

// Add a 404 handler
app.use((req, res) => {
  logMessage(`404 Not Found: ${req.method} ${req.path}`, 'WARNING', { endpoint: req.path });
  res.status(404).json({
    error: 'Not Found',
    message: `The requested endpoint ${req.path} does not exist.`
  });
});

// Start the server
const PORT = process.env.PORT || config.port || customPort || 45678;

// Try to start on the specified port
const server = app.listen(PORT, () => {
  logMessage(`AIArm HRM Architecture server running on port ${PORT}`, 'INFO');
  logMessage(`Surface Bridge: ${SURFACE_BRIDGE}`, 'INFO');
  logMessage(`Deep Bridge: ${DEEP_BRIDGE}`, 'INFO');
  logMessage(`Environment: ${config.environment}`, 'INFO');
  logMessage(`Open your browser and navigate to: http://localhost:${PORT}`, 'INFO');
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
  logMessage('SIGTERM received, shutting down gracefully', 'INFO');
  server.close(() => {
    logMessage('Server closed', 'INFO');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  logMessage('SIGINT received, shutting down gracefully', 'INFO');
  server.close(() => {
    logMessage('Server closed', 'INFO');
    process.exit(0);
  });
});
