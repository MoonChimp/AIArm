const fs = require('fs');
const path = require('path');
const os = require('os');
const http = require('http');
const { exec } = require('child_process');

// Configuration
const STATUS_FILE = path.join(__dirname, 'service_status.txt');
const LOGS_DIR = path.join(__dirname, 'Logs');
const CHECK_INTERVAL = 60000; // 1 minute
const RESTART_SCRIPT = path.join(__dirname, 'restart_hrm.bat');
const MAX_RESTARTS = 3; // Maximum number of automatic restarts per day

// Create logs directory if it doesn't exist
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR);
}

// Create log file
const LOG_FILE = path.join(LOGS_DIR, `monitor_${new Date().toISOString().replace(/:/g, '-')}.log`);

// Track restarts
let restartCount = 0;
let lastRestartDate = new Date().toDateString();

// Log function
function log(message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}\n`;
  
  console.log(message);
  
  try {
    fs.appendFileSync(LOG_FILE, logMessage);
  } catch (error) {
    console.error(`Error writing to log file: ${error.message}`);
  }
}

// Check if the HRM system is running
function checkSystemHealth() {
  log('Checking system health...');
  
  // Check if the status file exists and is recent
  let statusFileOk = false;
  try {
    if (fs.existsSync(STATUS_FILE)) {
      const stats = fs.statSync(STATUS_FILE);
      const fileAge = Date.now() - stats.mtime.getTime();
      
      // File should be updated at least every 5 minutes
      if (fileAge < 5 * 60 * 1000) {
        statusFileOk = true;
        log('Status file is recent and valid');
      } else {
        log(`Status file is too old: ${Math.floor(fileAge / 1000 / 60)} minutes`);
      }
    } else {
      log('Status file does not exist');
    }
  } catch (error) {
    log(`Error checking status file: ${error.message}`);
  }
  
  // Check if the server is responding
  checkServerHealth()
    .then(serverOk => {
      if (statusFileOk && serverOk) {
        log('System appears to be healthy');
      } else {
        log('System health check failed');
        
        // Check if we should restart
        const currentDate = new Date().toDateString();
        
        // Reset restart count if it's a new day
        if (currentDate !== lastRestartDate) {
          restartCount = 0;
          lastRestartDate = currentDate;
        }
        
        if (restartCount < MAX_RESTARTS) {
          log(`Initiating system restart (${restartCount + 1}/${MAX_RESTARTS} for today)`);
          restartSystem();
          restartCount++;
        } else {
          log(`Maximum restarts reached for today (${MAX_RESTARTS}). Manual intervention required.`);
        }
      }
    })
    .catch(error => {
      log(`Error in health check: ${error.message}`);
    });
}

// Check if the server is responding
function checkServerHealth() {
  return new Promise((resolve, reject) => {
    const req = http.get('http://localhost:45678/health', { timeout: 5000 }, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const status = JSON.parse(data);
            log(`Server health check: ${status.status}, uptime: ${Math.floor(status.uptime / 60)} minutes`);
            resolve(status.status === 'healthy');
          } catch (error) {
            log(`Error parsing server response: ${error.message}`);
            resolve(false);
          }
        } else {
          log(`Server returned non-200 status code: ${res.statusCode}`);
          resolve(false);
        }
      });
    });
    
    req.on('error', (error) => {
      log(`Server connection error: ${error.message}`);
      resolve(false);
    });
    
    req.on('timeout', () => {
      log('Server connection timed out');
      req.destroy();
      resolve(false);
    });
  });
}

// Restart the system
function restartSystem() {
  log('Executing restart script...');
  
  exec(`"${RESTART_SCRIPT}"`, (error, stdout, stderr) => {
    if (error) {
      log(`Error executing restart script: ${error.message}`);
      return;
    }
    
    if (stderr) {
      log(`Restart script stderr: ${stderr}`);
    }
    
    log(`Restart script output: ${stdout}`);
    log('System restart initiated');
  });
}

// Start monitoring
log('System monitor started');
log(`Checking system health every ${CHECK_INTERVAL / 1000} seconds`);
log(`Maximum automatic restarts per day: ${MAX_RESTARTS}`);

// Initial check
checkSystemHealth();

// Set up periodic checks
setInterval(checkSystemHealth, CHECK_INTERVAL);
