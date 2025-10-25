// Production-ready concurrent bridge server for AIArm HRM architecture
const express = require('express');
const path = require('path');
const cors = require('cors');
const { spawn } = require('child_process');
const fs = require('fs');
const winston = require('winston');
const http = require('http');

// Use the winston logger if available, otherwise fall back to console logging
let logger;
try {
  logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
      winston.format.timestamp(),
      winston.format.json()
    ),
    defaultMeta: { service: 'concurrent-server' },
    transports: [
      new winston.transports.File({ filename: 'error.log', level: 'error' }),
      new winston.transports.File({ filename: 'combined.log' }),
      new winston.transports.Console({
        format: winston.format.combine(
          winston.format.colorize(),
          winston.format.simple()
        )
      })
    ]
  });
  console.log('Winston logger initialized');
} catch (error) {
  // Winston not available, create a simple logger
  console.log('Winston logger not available, using console logging');
  logger = {
    info: console.log,
    warn: console.warn,
    error: console.error,
    debug: console.debug
  };
}

// Load configuration
let config;
try {
  config = require('./config');
  logger.info('Configuration loaded successfully');
} catch (error) {
  logger.warn('Failed to load configuration file, using defaults:', error.message);
  config = {
    port: process.env.PORT || 45678,
    surfaceBridge: 'improved_bridge.py',
    deepBridge: 'ollama_bridge.py',
    timeoutMs: 60000, // 1 minute timeout
    maxConcurrentRequests: 10,
    errorRetryCount: 3
  };
}

// Create Express app
const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use(express.static(path.join(__dirname)));

// Define a route for the root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'real_interface.html'));
});

// Track active requests for proper shutdown
let activeRequests = 0;
const requestQueue = [];
let isProcessingQueue = false;

// Define bridge files - using both bridges concurrently
const BRIDGES = {
  SURFACE: config.surfaceBridge || 'improved_bridge.py',  // For improved surface interactions
  DEEP: config.deepBridge || 'ollama_bridge.py'           // For deep thoughts and reasoning
};

// Check for custom bridge overrides via command line arguments
const args = process.argv.slice(2);
const surfaceBridgeIndex = args.indexOf('--surface-bridge');
if (surfaceBridgeIndex !== -1 && args.length > surfaceBridgeIndex + 1) {
  BRIDGES.SURFACE = args[surfaceBridgeIndex + 1];
  logger.info(`Using custom surface bridge: ${BRIDGES.SURFACE}`);
}

const deepBridgeIndex = args.indexOf('--deep-bridge');
if (deepBridgeIndex !== -1 && args.length > deepBridgeIndex + 1) {
  BRIDGES.DEEP = args[deepBridgeIndex + 1];
  logger.info(`Using custom deep bridge: ${BRIDGES.DEEP}`);
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    uptime: process.uptime(),
    activeRequests,
    queuedRequests: requestQueue.length,
    bridges: {
      surface: BRIDGES.SURFACE,
      deep: BRIDGES.DEEP
    },
    timestamp: new Date().toISOString()
  });
});

// Surface bridge request function
function processSurfaceBridgeRequest(input, userId = 'default', agentName = 'orchestrator') {
  return new Promise((resolve, reject) => {
    logger.info(`Processing surface bridge request for user ${userId}, agent ${agentName}`);
    
    const start = Date.now();
    const python = spawn('python', [BRIDGES.SURFACE]);
    let responseData = '';
    let errorData = '';
    
    const timeout = setTimeout(() => {
      logger.error('Surface bridge request timed out');
      python.kill();
      reject(new Error('Surface bridge request timed out'));
    }, config.timeoutMs);
    
    python.stdout.on('data', (data) => {
      responseData += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      errorData += data.toString();
      logger.warn(`Surface bridge error output: ${data.toString()}`);
    });
    
    python.on('close', (code) => {
      clearTimeout(timeout);
      if (code !== 0) {
        logger.error(`Surface bridge process exited with code ${code}`);
        logger.error(`Error data: ${errorData}`);
        reject(new Error(`Surface bridge process exited with code ${code}: ${errorData}`));
        return;
      }
      
      try {
        const result = JSON.parse(responseData);
        logger.info(`Surface bridge request completed in ${Date.now() - start}ms`);
        resolve(result);
      } catch (error) {
        logger.error('Failed to parse surface bridge response:', error);
        logger.error(`Raw response: ${responseData}`);
        reject(new Error(`Failed to parse surface bridge response: ${error.message}`));
      }
    });
    
    python.on('error', (error) => {
      clearTimeout(timeout);
      logger.error('Failed to start surface bridge process:', error);
      reject(error);
    });
    
    // Send the request to the Python bridge
    const requestData = JSON.stringify({
      agent: agentName,
      input: input,
      user_id: userId
    });
    
    python.stdin.write(requestData);
    python.stdin.end();
  });
}

// Deep reasoning bridge request function
function processDeepBridgeRequest(input, userId = 'default', agentName = 'reasoning') {
  return new Promise((resolve, reject) => {
    logger.info(`Processing deep bridge request for user ${userId}, agent ${agentName}`);
    
    const start = Date.now();
    const python = spawn('python', [BRIDGES.DEEP]);
    let responseData = '';
    let errorData = '';
    
    const timeout = setTimeout(() => {
      logger.error('Deep bridge request timed out');
      python.kill();
      reject(new Error('Deep bridge request timed out'));
    }, config.timeoutMs);
    
    python.stdout.on('data', (data) => {
      responseData += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      errorData += data.toString();
      logger.warn(`Deep bridge error output: ${data.toString()}`);
    });
    
    python.on('close', (code) => {
      clearTimeout(timeout);
      if (code !== 0) {
        logger.error(`Deep bridge process exited with code ${code}`);
        logger.error(`Error data: ${errorData}`);
        reject(new Error(`Deep bridge process exited with code ${code}: ${errorData}`));
        return;
      }
      
      try {
        const result = JSON.parse(responseData);
        logger.info(`Deep bridge request completed in ${Date.now() - start}ms`);
        resolve(result);
      } catch (error) {
        logger.error('Failed to parse deep bridge response:', error);
        logger.error(`Raw response: ${responseData}`);
        reject(new Error(`Failed to parse deep bridge response: ${error.message}`));
      }
    });
    
    python.on('error', (error) => {
      clearTimeout(timeout);
      logger.error('Failed to start deep bridge process:', error);
      reject(error);
    });
    
    // Send the request to the Python bridge
    const requestData = JSON.stringify({
      agent: agentName,
      input: input,
      user_id: userId
    });
    
    python.stdin.write(requestData);
    python.stdin.end();
  });
}

// Combine responses from both bridges
function combineResponses(surfaceResponse, deepResponse) {
  // If either response failed, use the successful one
  if (!surfaceResponse.success && deepResponse.success) {
    logger.warn('Using only deep bridge response due to surface bridge failure');
    return deepResponse;
  }
  
  if (surfaceResponse.success && !deepResponse.success) {
    logger.warn('Using only surface bridge response due to deep bridge failure');
    return surfaceResponse;
  }
  
  if (!surfaceResponse.success && !deepResponse.success) {
    logger.error('Both bridges failed to process the request');
    return {
      success: false,
      status: 'error',
      error: 'Both processing systems failed to handle the request',
      result: 'I apologize, but I encountered an issue processing your request. Please try again.'
    };
  }
  
  // Handle the case where both were successful
  try {
    // Create a combined response with surface structure but deep insights
    const combinedResponse = {
      success: true,
      status: 'completed',
      result: surfaceResponse.result || ''
    };
    
    // If deep reasoning provided additional thought process, include it
    if (deepResponse.thought_process) {
      combinedResponse.thought_process = deepResponse.thought_process;
    }
    
    // If deep response contains insights not in surface response, augment the result
    if (deepResponse.result && typeof deepResponse.result === 'string' && 
        deepResponse.result.length > 0 && deepResponse.result !== surfaceResponse.result) {
      
      // Check if we need to enrich the surface response
      if (!surfaceResponse.result || surfaceResponse.result.length < deepResponse.result.length * 0.5) {
        // Deep response has substantially more content
        combinedResponse.result = deepResponse.result;
      } else {
        // Intelligently combine the responses when appropriate
        const surfaceLines = surfaceResponse.result.split('\n');
        const deepLines = deepResponse.result.split('\n');
        
        // Keep track of whether we've already inserted deep insights
        let deepInsightsAdded = false;
        
        // If deep reasoning starts with a distinct insight not in surface, prepend it
        if (deepLines[0] && !surfaceResponse.result.includes(deepLines[0])) {
          combinedResponse.result = `${deepLines[0]}\n\n${surfaceResponse.result}`;
          deepInsightsAdded = true;
        }
        
        // If we didn't add the deep insights yet and there are substantive differences
        if (!deepInsightsAdded && deepResponse.result.length > 100 && 
            !surfaceResponse.result.includes(deepResponse.result.substring(0, 100))) {
          
          combinedResponse.result = `${surfaceResponse.result}\n\n**Additional Insights:**\n${deepResponse.result}`;
        }
      }
    }
    
    return combinedResponse;
  } catch (error) {
    logger.error('Error combining responses:', error);
    // Fallback to surface response if combination fails
    return surfaceResponse;
  }
}

// Process queue to limit concurrent requests
function processQueue() {
  if (isProcessingQueue || requestQueue.length === 0 || activeRequests >= config.maxConcurrentRequests) {
    return;
  }
  
  isProcessingQueue = true;
  
  const nextRequest = requestQueue.shift();
  if (nextRequest) {
    activeRequests++;
    
    handleRequest(nextRequest.req, nextRequest.res)
      .catch(error => {
        logger.error('Error processing queued request:', error);
        nextRequest.res.status(500).json({
          success: false,
          status: 'error',
          error: 'Failed to process request',
          result: 'I apologize, but I encountered an issue processing your request. Please try again.'
        });
      })
      .finally(() => {
        activeRequests--;
        isProcessingQueue = false;
        // Process next item in queue
        processQueue();
      });
  } else {
    isProcessingQueue = false;
  }
}

// Main request handler
async function handleRequest(req, res) {
  const { input, agent_name = 'orchestrator', user_id = 'default' } = req.body;
  
  if (!input) {
    return res.status(400).json({
      success: false,
      status: 'error',
      error: 'No input provided',
      result: 'Please provide input to process.'
    });
  }
  
  logger.info(`Processing request for user ${user_id}, agent ${agent_name}`);
  const startTime = Date.now();
  
  try {
    // Process both bridges concurrently
    const [surfaceResponse, deepResponse] = await Promise.allSettled([
      processSurfaceBridgeRequest(input, user_id, agent_name),
      processDeepBridgeRequest(input, user_id, agent_name === 'reasoning' ? agent_name : 'reasoning')
    ]);
    
    // Extract results or errors
    const surface = surfaceResponse.status === 'fulfilled' 
      ? surfaceResponse.value 
      : { success: false, error: surfaceResponse.reason?.message || 'Surface bridge failed' };
    
    const deep = deepResponse.status === 'fulfilled'
      ? deepResponse.value
      : { success: false, error: deepResponse.reason?.message || 'Deep bridge failed' };
    
    // Combine the responses
    const combinedResponse = combineResponses(surface, deep);
    
    // Log response time
    logger.info(`Request processed in ${Date.now() - startTime}ms`);
    
    // Send response
    return res.json(combinedResponse);
  } catch (error) {
    logger.error('Error processing request:', error);
    return res.status(500).json({
      success: false,
      status: 'error',
      error: error.message || 'Unknown error',
      result: 'I apologize, but I encountered an issue processing your request. Please try again.'
    });
  }
}

// Main API endpoint
app.post('/api/process', (req, res) => {
  if (activeRequests >= config.maxConcurrentRequests) {
    // Queue request if we're at capacity
    requestQueue.push({ req, res });
    logger.info(`Request queued. Active: ${activeRequests}, Queued: ${requestQueue.length}`);
  } else {
    activeRequests++;
    handleRequest(req, res)
      .catch(error => {
        logger.error('Error in request handler:', error);
        res.status(500).json({
          success: false,
          status: 'error',
          error: 'Failed to process request',
          result: 'I apologize, but I encountered an issue processing your request. Please try again.'
        });
      })
      .finally(() => {
        activeRequests--;
        // Process next item in queue if any
        processQueue();
      });
  }
});

// Status API endpoint
app.get('/api/status', (req, res) => {
  res.json({
    success: true,
    status: {
      uptime: process.uptime(),
      timestamp: new Date().toISOString(),
      activeRequests,
      queuedRequests: requestQueue.length,
      bridges: {
        surface: BRIDGES.SURFACE,
        deep: BRIDGES.DEEP
      }
    }
  });
});

// Create HTTP server
const server = http.createServer(app);

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    logger.info('HTTP server closed');
    process.exit(0);
  });
  
  // Force close after timeout if still open
  setTimeout(() => {
    logger.error('Could not close connections in time, forcefully shutting down');
    process.exit(1);
  }, 10000);
});

// Start server
const PORT = config.port || 45678;
server.listen(PORT, () => {
  logger.info(`=======================================================`);
  logger.info(`  AIArm HRM System Server Running on Port ${PORT}`);
  logger.info(`  Surface Bridge: ${BRIDGES.SURFACE}`);
  logger.info(`  Deep Bridge: ${BRIDGES.DEEP}`);
  logger.info(`=======================================================`);
});
