/**
 * AIArm HRM Error Handler
 * Provides robust error handling and logging for production environments
 */

const fs = require('fs');
const path = require('path');
const config = require('./config');

// Ensure log directory exists
const logDir = path.resolve(config.logDirectory || 'D:/AIArm/Logs');
const errorLogDir = path.join(logDir, 'Errors');

try {
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  if (!fs.existsSync(errorLogDir)) {
    fs.mkdirSync(errorLogDir, { recursive: true });
  }
} catch (err) {
  console.error(`Failed to create log directories: ${err.message}`);
}

// Error counts for monitoring
const errorCounts = {
  total: 0,
  byType: {},
  byBridge: {
    surface: 0,
    deep: 0
  },
  byEndpoint: {},
  lastReset: Date.now()
};

// Reset error counts periodically
setInterval(() => {
  const now = Date.now();
  const hoursSinceReset = (now - errorCounts.lastReset) / (1000 * 60 * 60);
  
  if (hoursSinceReset >= 24) {
    errorCounts.total = 0;
    errorCounts.byType = {};
    errorCounts.byBridge = { surface: 0, deep: 0 };
    errorCounts.byEndpoint = {};
    errorCounts.lastReset = now;
    
    logMessage('Error counts reset', 'INFO');
  }
}, 60 * 60 * 1000); // Check every hour

/**
 * Log a message to the appropriate log file
 */
function logMessage(message, level = 'INFO', options = {}) {
  const { bridge, endpoint, error } = options;
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] [${level}] ${bridge ? `[${bridge.toUpperCase()}] ` : ''}${message}\n`;
  
  // Determine log file
  const dateStr = new Date().toISOString().split('T')[0];
  let logFile;
  
  if (level === 'ERROR' || level === 'CRITICAL') {
    logFile = path.join(errorLogDir, `error_${dateStr}.log`);
  } else {
    logFile = path.join(logDir, `hrm_system_${dateStr}.log`);
  }
  
  // Log to console if enabled
  if (config.logToConsole) {
    let consoleMethod = console.log;
    if (level === 'ERROR' || level === 'CRITICAL') {
      consoleMethod = console.error;
    } else if (level === 'WARNING') {
      consoleMethod = console.warn;
    }
    
    consoleMethod(logMessage.trim());
  }
  
  // Log to file if enabled
  if (config.logToFile) {
    fs.appendFile(logFile, logMessage, (err) => {
      if (err) {
        console.error(`Failed to write to log file: ${err.message}`);
      }
    });
  }
  
  // Update error counts for monitoring
  if (level === 'ERROR' || level === 'CRITICAL') {
    errorCounts.total++;
    
    // Track by error type
    const errorType = error ? error.name || 'UnknownError' : 'UnknownError';
    errorCounts.byType[errorType] = (errorCounts.byType[errorType] || 0) + 1;
    
    // Track by bridge
    if (bridge) {
      errorCounts.byBridge[bridge.toLowerCase()] = (errorCounts.byBridge[bridge.toLowerCase()] || 0) + 1;
    }
    
    // Track by endpoint
    if (endpoint) {
      errorCounts.byEndpoint[endpoint] = (errorCounts.byEndpoint[endpoint] || 0) + 1;
    }
    
    // Trigger alert if threshold exceeded
    const errorThreshold = config.errorHandling?.errorThresholdForAlert || 5;
    if (errorCounts.total >= errorThreshold) {
      // Create alert file
      const alertFile = path.join(errorLogDir, `ALERT_${Date.now()}.json`);
      fs.writeFile(alertFile, JSON.stringify({
        timestamp: new Date().toISOString(),
        message: `Error threshold exceeded: ${errorCounts.total} errors`,
        errorCounts: errorCounts,
        lastError: {
          message: error ? error.message : message,
          stack: error ? error.stack : null
        }
      }, null, 2), (err) => {
        if (err) {
          console.error(`Failed to write alert file: ${err.message}`);
        }
      });
    }
  }
}

/**
 * Handle uncaught exceptions
 */
process.on('uncaughtException', (error) => {
  logMessage(`Uncaught exception: ${error.message}`, 'CRITICAL', { error });
  
  // Write error details to file
  const errorFile = path.join(errorLogDir, `fatal_${Date.now()}.json`);
  fs.writeFileSync(errorFile, JSON.stringify({
    timestamp: new Date().toISOString(),
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack
    }
  }, null, 2));
  
  // Exit with error code if in production
  if (config.isProd && config.errorHandling?.gracefulShutdown) {
    logMessage('Performing graceful shutdown due to uncaught exception', 'CRITICAL');
    
    // Give time for logs to be written
    setTimeout(() => {
      process.exit(1);
    }, 1000);
  }
});

/**
 * Handle unhandled rejections
 */
process.on('unhandledRejection', (reason, promise) => {
  const error = reason instanceof Error ? reason : new Error(String(reason));
  logMessage(`Unhandled rejection: ${error.message}`, 'ERROR', { error });
});

/**
 * Handle bridge errors
 */
function handleBridgeError(bridge, error, info = {}) {
  const { input, agent, userId } = info;
  logMessage(
    `${bridge} bridge error: ${error.message}${input ? ` (Input: "${input.substring(0, 50)}${input.length > 50 ? '...' : ''}")` : ''}`, 
    'ERROR', 
    { bridge, error, endpoint: 'bridge' }
  );
  
  // Log detailed information
  const errorDetailsFile = path.join(errorLogDir, `${bridge}_${Date.now()}.json`);
  fs.writeFile(errorDetailsFile, JSON.stringify({
    timestamp: new Date().toISOString(),
    bridge: bridge,
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack
    },
    context: {
      input: input,
      agent: agent,
      userId: userId
    }
  }, null, 2), (err) => {
    if (err) {
      console.error(`Failed to write error details file: ${err.message}`);
    }
  });
  
  // Return standardized error response
  return {
    success: false,
    status: 'error',
    error: `${bridge} bridge error: ${error.message}`,
    errorType: error.name || 'Error',
    timestamp: new Date().toISOString()
  };
}

/**
 * Handle API errors
 */
function handleApiError(req, res, error, errorInfo = {}) {
  const endpoint = req.path || 'unknown';
  const method = req.method || 'unknown';
  const ip = req.ip || req.connection.remoteAddress || 'unknown';
  
  logMessage(
    `API error at ${method} ${endpoint}: ${error.message}`, 
    'ERROR', 
    { endpoint, error }
  );
  
  // Log detailed information
  const errorDetailsFile = path.join(errorLogDir, `api_${Date.now()}.json`);
  fs.writeFile(errorDetailsFile, JSON.stringify({
    timestamp: new Date().toISOString(),
    request: {
      path: endpoint,
      method: method,
      ip: ip,
      headers: req.headers,
      body: req.body
    },
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack
    },
    info: errorInfo
  }, null, 2), (err) => {
    if (err) {
      console.error(`Failed to write error details file: ${err.message}`);
    }
  });
  
  // Send error response
  res.status(errorInfo.statusCode || 500).json({
    error: errorInfo.publicMessage || 'Internal server error',
    message: config.isProd ? 'An error occurred while processing your request' : error.message,
    errorId: Date.now().toString(36),
    timestamp: new Date().toISOString()
  });
}

/**
 * Get error statistics
 */
function getErrorStats() {
  return {
    total: errorCounts.total,
    byType: errorCounts.byType,
    byBridge: errorCounts.byBridge,
    byEndpoint: errorCounts.byEndpoint,
    lastReset: new Date(errorCounts.lastReset).toISOString()
  };
}

module.exports = {
  logMessage,
  handleBridgeError,
  handleApiError,
  getErrorStats
};
