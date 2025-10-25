// health_check.js
// Provides detailed health checks for the Nexus HRM system

const http = require('http');
const os = require('os');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Configuration
const CONFIG = {
  port: 45680,                      // Health check server port
  checkIntervalMs: 60000,           // Check interval (1 minute)
  logDir: path.join(__dirname, 'logs'),
  logRotationDays: 7,               // Keep logs for 7 days
  componentEndpoints: {
    hrmServer: 'http://localhost:45678/health',
    memoryVisualizer: 'http://localhost:3000/health' // If applicable
  }
};

// Ensure log directory exists
if (!fs.existsSync(CONFIG.logDir)) {
  fs.mkdirSync(CONFIG.logDir, { recursive: true });
}

// Initialize logging
const logFile = path.join(CONFIG.logDir, `health_check_${new Date().toISOString().split('T')[0]}.log`);

function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] [${level}] ${message}`;
  
  console.log(logMessage);
  fs.appendFileSync(logFile, logMessage + '\n');
}

// Rotate logs (delete old log files)
function rotateLogs() {
  try {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - CONFIG.logRotationDays);
    
    const files = fs.readdirSync(CONFIG.logDir);
    for (const file of files) {
      if (file.startsWith('health_check_')) {
        const filePath = path.join(CONFIG.logDir, file);
        const stats = fs.statSync(filePath);
        const fileDate = new Date(stats.mtime);
        
        if (fileDate < cutoffDate) {
          fs.unlinkSync(filePath);
          log(`Rotated old log file: ${file}`, 'DEBUG');
        }
      }
    }
  } catch (error) {
    log(`Error rotating logs: ${error.message}`, 'ERROR');
  }
}

// Check system health
async function checkSystemHealth() {
  const health = {
    timestamp: new Date().toISOString(),
    status: 'healthy', // Will be changed to 'degraded' or 'critical' if issues found
    components: {},
    system: {
      uptime: os.uptime(),
      loadAvg: os.loadavg(),
      memory: {
        total: os.totalmem(),
        free: os.freemem(),
        usedPercent: (1 - (os.freemem() / os.totalmem())) * 100
      },
      cpu: {
        cores: os.cpus().length,
        model: os.cpus()[0].model
      },
      network: {},
      disk: {}
    }
  };
  
  // Check components
  let criticalIssues = 0;
  let degradedComponents = 0;
  
  // Check HRM Server
  try {
    const serverStatus = await checkEndpoint(CONFIG.componentEndpoints.hrmServer);
    health.components.hrmServer = serverStatus;
    
    if (!serverStatus.healthy) {
      degradedComponents++;
      if (serverStatus.critical) {
        criticalIssues++;
      }
    }
  } catch (error) {
    health.components.hrmServer = { 
      healthy: false, 
      critical: true, 
      error: error.message 
    };
    criticalIssues++;
  }
  
  // Check Memory Visualizer if configured
  if (CONFIG.componentEndpoints.memoryVisualizer) {
    try {
      const visualizerStatus = await checkEndpoint(CONFIG.componentEndpoints.memoryVisualizer);
      health.components.memoryVisualizer = visualizerStatus;
      
      if (!visualizerStatus.healthy) {
        degradedComponents++;
        if (visualizerStatus.critical) {
          criticalIssues++;
        }
      }
    } catch (error) {
      health.components.memoryVisualizer = { 
        healthy: false, 
        critical: false, // Memory visualizer is not critical
        error: error.message 
      };
      degradedComponents++;
    }
  }
  
  // Check Ollama availability
  try {
    const ollamaStatus = await checkOllama();
    health.components.ollama = ollamaStatus;
    
    if (!ollamaStatus.healthy) {
      degradedComponents++;
      if (ollamaStatus.critical) {
        criticalIssues++;
      }
    }
  } catch (error) {
    health.components.ollama = { 
      healthy: false, 
      critical: true, 
      error: error.message 
    };
    criticalIssues++;
  }
  
  // Check Python processes
  try {
    const pythonProcesses = await checkPythonProcesses();
    health.components.pythonProcesses = pythonProcesses;
    
    if (pythonProcesses.missing.length > 0) {
      degradedComponents++;
      if (pythonProcesses.criticalMissing) {
        criticalIssues++;
      }
    }
  } catch (error) {
    health.components.pythonProcesses = { 
      healthy: false, 
      error: error.message 
    };
    degradedComponents++;
  }
  
  // Check disk space
  try {
    const diskSpace = await checkDiskSpace();
    health.system.disk = diskSpace;
    
    if (diskSpace.criticalLow) {
      criticalIssues++;
      health.components.diskSpace = { 
        healthy: false, 
        critical: true, 
        message: 'Critical low disk space' 
      };
    } else if (diskSpace.warningLow) {
      degradedComponents++;
      health.components.diskSpace = { 
        healthy: false, 
        critical: false, 
        message: 'Low disk space warning' 
      };
    } else {
      health.components.diskSpace = { 
        healthy: true
      };
    }
  } catch (error) {
    health.components.diskSpace = { 
      healthy: false, 
      error: error.message 
    };
  }
  
  // Set overall status
  if (criticalIssues > 0) {
    health.status = 'critical';
  } else if (degradedComponents > 0) {
    health.status = 'degraded';
  }
  
  // Log health status
  const logLevel = health.status === 'healthy' ? 'INFO' : (health.status === 'degraded' ? 'WARN' : 'ERROR');
  log(`System health: ${health.status.toUpperCase()}`, logLevel);
  
  if (health.status !== 'healthy') {
    log(`Health check details: ${JSON.stringify(health, null, 2)}`, logLevel);
  }
  
  return health;
}

// Check endpoint
async function checkEndpoint(url) {
  return new Promise((resolve) => {
    const req = http.get(url, (res) => {
      res.resume();
      resolve({
        healthy: res.statusCode === 200,
        critical: true, // Most endpoints are critical
        statusCode: res.statusCode
      });
    });
    
    req.on('error', (error) => {
      resolve({
        healthy: false,
        critical: true,
        error: error.message
      });
    });
    
    req.setTimeout(5000, () => {
      req.abort();
      resolve({
        healthy: false,
        critical: true,
        error: 'Request timed out'
      });
    });
  });
}

// Check Ollama availability
async function checkOllama() {
  return new Promise((resolve) => {
    const req = http.get('http://localhost:11434/api/tags', (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          if (res.statusCode === 200) {
            const response = JSON.parse(data);
            resolve({
              healthy: true,
              models: response.models ? response.models.length : 0,
              modelNames: response.models ? response.models.map(m => m.name) : []
            });
          } else {
            resolve({
              healthy: false,
              critical: true,
              statusCode: res.statusCode,
              message: 'Ollama returned non-200 status code'
            });
          }
        } catch (error) {
          resolve({
            healthy: false,
            critical: true,
            error: `Error parsing Ollama response: ${error.message}`
          });
        }
      });
    });
    
    req.on('error', (error) => {
      resolve({
        healthy: false,
        critical: true,
        error: `Error connecting to Ollama: ${error.message}`
      });
    });
    
    req.setTimeout(5000, () => {
      req.abort();
      resolve({
        healthy: false,
        critical: true,
        error: 'Ollama request timed out'
      });
    });
  });
}

// Check Python processes
async function checkPythonProcesses() {
  return new Promise((resolve, reject) => {
    // Critical Python processes that must be running
    const criticalProcesses = [
      'inner_life_processor.py',
      'agent_integration.py'
    ];
    
    // Important but non-critical processes
    const importantProcesses = [
      'memory_visualizer.py',
      'agent_manager.py'
    ];
    
    const expectedProcesses = [...criticalProcesses, ...importantProcesses];
    
    // Command to list python processes
    const command = process.platform === 'win32'
      ? 'tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH'
      : 'ps aux | grep python';
    
    exec(command, (error, stdout) => {
      if (error) {
        reject(new Error(`Error checking Python processes: ${error.message}`));
        return;
      }
      
      const runningProcesses = [];
      const missing = [];
      
      // Check which expected processes are running
      for (const proc of expectedProcesses) {
        if (stdout.includes(proc)) {
          runningProcesses.push(proc);
        } else {
          missing.push(proc);
        }
      }
      
      // Check if any critical processes are missing
      const criticalMissing = missing.some(proc => criticalProcesses.includes(proc));
      
      resolve({
        healthy: missing.length === 0,
        runningProcesses,
        missing,
        criticalMissing
      });
    });
  });
}

// Check disk space
async function checkDiskSpace() {
  return new Promise((resolve, reject) => {
    const command = process.platform === 'win32'
      ? 'wmic logicaldisk get deviceid,freespace,size,volumename'
      : 'df -h';
    
    exec(command, (error, stdout) => {
      if (error) {
        reject(new Error(`Error checking disk space: ${error.message}`));
        return;
      }
      
      // Parse the output differently based on platform
      try {
        if (process.platform === 'win32') {
          // Windows parsing
          const lines = stdout.trim().split('\n').slice(1); // Skip header
          const drives = [];
          
          for (const line of lines) {
            const parts = line.trim().split(/\s+/);
            if (parts.length >= 3) {
              const driveLetter = parts[0];
              const freeSpace = parseInt(parts[1], 10);
              const totalSize = parseInt(parts[2], 10);
              
              if (driveLetter && !isNaN(freeSpace) && !isNaN(totalSize) && totalSize > 0) {
                const usedPercent = ((totalSize - freeSpace) / totalSize) * 100;
                drives.push({
                  drive: driveLetter,
                  freeSpace,
                  totalSize,
                  usedPercent,
                  volumeName: parts.slice(3).join(' ')
                });
              }
            }
          }
          
          // Check if any drive is critically low (< 5%) or warning low (< 10%)
          const criticalLow = drives.some(drive => (drive.freeSpace / drive.totalSize) < 0.05);
          const warningLow = drives.some(drive => (drive.freeSpace / drive.totalSize) < 0.1);
          
          resolve({
            drives,
            criticalLow,
            warningLow
          });
        } else {
          // Unix parsing
          const lines = stdout.trim().split('\n').slice(1); // Skip header
          const filesystems = [];
          
          for (const line of lines) {
            const parts = line.trim().split(/\s+/);
            if (parts.length >= 5) {
              const filesystem = parts[0];
              const size = parts[1];
              const used = parts[2];
              const available = parts[3];
              const usedPercent = parseInt(parts[4].replace('%', ''), 10);
              const mountPoint = parts[5];
              
              filesystems.push({
                filesystem,
                size,
                used,
                available,
                usedPercent,
                mountPoint
              });
            }
          }
          
          // Check if any filesystem is critically low (> 95%) or warning low (> 90%)
          const criticalLow = filesystems.some(fs => fs.usedPercent > 95);
          const warningLow = filesystems.some(fs => fs.usedPercent > 90);
          
          resolve({
            filesystems,
            criticalLow,
            warningLow
          });
        }
      } catch (error) {
        reject(new Error(`Error parsing disk space: ${error.message}`));
      }
    });
  });
}

// Create HTTP server for health checks
const server = http.createServer(async (req, res) => {
  if (req.url === '/health' || req.url === '/') {
    try {
      const health = await checkSystemHealth();
      
      // Set appropriate status code based on health
      if (health.status === 'critical') {
        res.statusCode = 503; // Service Unavailable
      } else if (health.status === 'degraded') {
        res.statusCode = 200; // Still OK but with warning
      } else {
        res.statusCode = 200;
      }
      
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(health));
    } catch (error) {
      log(`Error handling health check request: ${error.message}`, 'ERROR');
      
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({
        status: 'error',
        error: error.message
      }));
    }
  } else {
    res.statusCode = 404;
    res.end('Not Found');
  }
});

// Start server
server.listen(CONFIG.port, () => {
  log(`Health check server running at http://localhost:${CONFIG.port}`);
});

// Run initial health check
checkSystemHealth();

// Schedule regular health checks
setInterval(() => {
  checkSystemHealth();
}, CONFIG.checkIntervalMs);

// Schedule log rotation daily
const ROTATION_INTERVAL = 24 * 60 * 60 * 1000; // 24 hours
setInterval(() => {
  log('Performing scheduled log rotation', 'DEBUG');
  rotateLogs();
}, ROTATION_INTERVAL);

// Handle process signals
process.on('SIGINT', () => {
  log('Health check server shutting down (SIGINT)', 'INFO');
  server.close(() => {
    process.exit(0);
  });
});

process.on('SIGTERM', () => {
  log('Health check server shutting down (SIGTERM)', 'INFO');
  server.close(() => {
    process.exit(0);
  });
});

process.on('uncaughtException', (error) => {
  log(`Uncaught Exception: ${error.message}`, 'ERROR');
  log(error.stack, 'ERROR');
  // Keep running despite the error
});