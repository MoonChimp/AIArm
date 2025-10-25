/**
 * AIArm HRM System Monitor
 * Monitors system resources and health for the HRM architecture
 */

const os = require('os');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const config = require('./config');
const { logMessage } = require('./error_handler');

// System metrics
let metrics = {
  startTime: Date.now(),
  uptime: 0,
  memoryUsage: {
    rss: 0,
    heapTotal: 0,
    heapUsed: 0,
    external: 0,
    percentUsed: 0
  },
  cpuUsage: {
    user: 0,
    system: 0,
    percent: 0
  },
  requestStats: {
    total: 0,
    success: 0,
    error: 0,
    avgResponseTime: 0
  },
  bridgeStats: {
    surface: {
      requests: 0,
      success: 0,
      error: 0,
      avgResponseTime: 0
    },
    deep: {
      requests: 0,
      success: 0,
      error: 0,
      avgResponseTime: 0
    }
  },
  pendingRequests: {
    surface: 0,
    deep: 0
  },
  lastUpdate: Date.now()
};

// Previous CPU usage for calculating percentage
let previousCpuUsage = process.cpuUsage();
let previousOsCpuUsage = os.cpus().reduce(
  (acc, cpu) => {
    acc.user += cpu.times.user;
    acc.nice += cpu.times.nice;
    acc.sys += cpu.times.sys;
    acc.idle += cpu.times.idle;
    acc.irq += cpu.times.irq;
    return acc;
  },
  { user: 0, nice: 0, sys: 0, idle: 0, irq: 0 }
);

// Check if bridges are running
function checkBridgesRunning() {
  try {
    // Get Python processes running the bridges
    let surfaceRunning = false;
    let deepRunning = false;

    try {
      // This will work on Windows
      const processes = execSync('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH').toString();
      surfaceRunning = processes.includes(config.surfaceBridge);
      deepRunning = processes.includes(config.deepBridge);
    } catch (err) {
      try {
        // This will work on Linux/Mac
        const processes = execSync('ps aux | grep python').toString();
        surfaceRunning = processes.includes(config.surfaceBridge);
        deepRunning = processes.includes(config.deepBridge);
      } catch (err2) {
        // If both fail, assume bridges are running (we don't want to return false negatives)
        surfaceRunning = true;
        deepRunning = true;
      }
    }

    return {
      surface: surfaceRunning,
      deep: deepRunning
    };
  } catch (error) {
    logMessage(`Error checking bridge status: ${error.message}`, 'ERROR', { error });
    // Assume bridges are running if we can't check
    return {
      surface: true,
      deep: true
    };
  }
}

// Check inner life processor status
function checkInnerLifeStatus() {
  if (!config.innerLifeEnabled) {
    return { running: false, enabled: false };
  }

  try {
    // Check for the presence of a heartbeat file or process
    let running = false;

    try {
      // Check for process
      const processes = execSync('tasklist /FI "WINDOWTITLE eq Nexus Inner Life*" /FO CSV /NH').toString();
      running = processes.length > 0;
    } catch (err) {
      // Check for heartbeat file as fallback
      const heartbeatFile = path.join(config.innerLifeDirectory, 'heartbeat.txt');
      if (fs.existsSync(heartbeatFile)) {
        const heartbeatContent = fs.readFileSync(heartbeatFile, 'utf8');
        const heartbeatTime = parseInt(heartbeatContent, 10);
        if (!isNaN(heartbeatTime)) {
          // Check if heartbeat is within the last 2 minutes
          running = (Date.now() - heartbeatTime) < 120000;
        }
      }
    }

    return {
      running: running,
      enabled: true
    };
  } catch (error) {
    logMessage(`Error checking inner life status: ${error.message}`, 'WARNING', { error });
    return {
      running: false,
      enabled: true,
      error: error.message
    };
  }
}

// Update metrics
function updateMetrics() {
  try {
    // Update uptime
    metrics.uptime = process.uptime();

    // Update memory usage
    const memUsage = process.memoryUsage();
    metrics.memoryUsage = {
      rss: memUsage.rss,
      heapTotal: memUsage.heapTotal,
      heapUsed: memUsage.heapUsed,
      external: memUsage.external,
      percentUsed: Math.round((memUsage.heapUsed / memUsage.heapTotal) * 100)
    };

    // Update CPU usage
    const currentCpuUsage = process.cpuUsage(previousCpuUsage);
    const currentOsCpuUsage = os.cpus().reduce(
      (acc, cpu) => {
        acc.user += cpu.times.user;
        acc.nice += cpu.times.nice;
        acc.sys += cpu.times.sys;
        acc.idle += cpu.times.idle;
        acc.irq += cpu.times.irq;
        return acc;
      },
      { user: 0, nice: 0, sys: 0, idle: 0, irq: 0 }
    );

    // Calculate CPU usage percentage
    const userDiff = currentOsCpuUsage.user - previousOsCpuUsage.user;
    const sysDiff = currentOsCpuUsage.sys - previousOsCpuUsage.sys;
    const idleDiff = currentOsCpuUsage.idle - previousOsCpuUsage.idle;
    const totalDiff = userDiff + sysDiff + idleDiff;
    const cpuPercent = Math.round(((userDiff + sysDiff) / totalDiff) * 100);

    metrics.cpuUsage = {
      user: currentCpuUsage.user,
      system: currentCpuUsage.system,
      percent: cpuPercent
    };

    // Update previous CPU usage for next calculation
    previousCpuUsage = process.cpuUsage();
    previousOsCpuUsage = currentOsCpuUsage;

    // Check bridge status
    const bridgeStatus = checkBridgesRunning();
    metrics.bridgeStatus = bridgeStatus;

    // Check inner life status
    metrics.innerLifeStatus = checkInnerLifeStatus();

    // Update timestamp
    metrics.lastUpdate = Date.now();

    // Check for alerts
    checkAlerts();

    // Write metrics to file for external monitoring
    writeMetricsFile();

    return metrics;
  } catch (error) {
    logMessage(`Error updating metrics: ${error.message}`, 'ERROR', { error });
    return metrics;
  }
}

// Check for alert conditions
function checkAlerts() {
  const alertThresholds = config.monitoring?.alertThresholds || {
    cpuUsage: 80,
    memoryUsage: 80,
    responseTimeMs: 5000
  };

  let alerts = [];

  // Check CPU usage
  if (metrics.cpuUsage.percent > alertThresholds.cpuUsage) {
    alerts.push({
      type: 'CPU_USAGE',
      message: `CPU usage is high: ${metrics.cpuUsage.percent}%`,
      value: metrics.cpuUsage.percent,
      threshold: alertThresholds.cpuUsage
    });
  }

  // Check memory usage
  if (metrics.memoryUsage.percentUsed > alertThresholds.memoryUsage) {
    alerts.push({
      type: 'MEMORY_USAGE',
      message: `Memory usage is high: ${metrics.memoryUsage.percentUsed}%`,
      value: metrics.memoryUsage.percentUsed,
      threshold: alertThresholds.memoryUsage
    });
  }

  // Check bridge status
  if (!metrics.bridgeStatus.surface) {
    alerts.push({
      type: 'BRIDGE_DOWN',
      message: 'Surface bridge is not running',
      bridge: 'surface'
    });
  }

  if (!metrics.bridgeStatus.deep) {
    alerts.push({
      type: 'BRIDGE_DOWN',
      message: 'Deep bridge is not running',
      bridge: 'deep'
    });
  }

  // Check inner life status
  if (config.innerLifeEnabled && !metrics.innerLifeStatus.running) {
    alerts.push({
      type: 'INNER_LIFE_DOWN',
      message: 'Inner Life processor is not running'
    });
  }

  // Log alerts
  if (alerts.length > 0) {
    const alertsDir = path.join(config.logDirectory || 'D:/AIArm/Logs', 'Alerts');
    
    // Ensure alerts directory exists
    if (!fs.existsSync(alertsDir)) {
      fs.mkdirSync(alertsDir, { recursive: true });
    }
    
    // Write alerts to file
    const alertFile = path.join(alertsDir, `alert_${Date.now()}.json`);
    fs.writeFile(alertFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      alerts: alerts,
      metrics: metrics
    }, null, 2), (err) => {
      if (err) {
        logMessage(`Failed to write alert file: ${err.message}`, 'ERROR', { error: err });
      }
    });
    
    // Log alerts
    alerts.forEach(alert => {
      logMessage(alert.message, 'WARNING');
    });
  }

  return alerts;
}

// Write metrics to file for external monitoring
function writeMetricsFile() {
  try {
    const metricsFile = path.join(config.logDirectory || 'D:/AIArm/Logs', 'Monitor', 'metrics.json');
    
    // Ensure directory exists
    const metricsDir = path.dirname(metricsFile);
    if (!fs.existsSync(metricsDir)) {
      fs.mkdirSync(metricsDir, { recursive: true });
    }
    
    fs.writeFile(metricsFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      metrics: metrics
    }, null, 2), (err) => {
      if (err) {
        logMessage(`Failed to write metrics file: ${err.message}`, 'WARNING', { error: err });
      }
    });
  } catch (error) {
    logMessage(`Error writing metrics file: ${error.message}`, 'WARNING', { error });
  }
}

// Track request stats
function trackRequest(bridge, success, responseTime) {
  try {
    // Update total stats
    metrics.requestStats.total++;
    if (success) {
      metrics.requestStats.success++;
    } else {
      metrics.requestStats.error++;
    }
    
    // Update average response time
    const currentTotal = metrics.requestStats.avgResponseTime * (metrics.requestStats.total - 1);
    metrics.requestStats.avgResponseTime = (currentTotal + responseTime) / metrics.requestStats.total;
    
    // Update bridge-specific stats
    if (bridge) {
      const bridgeKey = bridge.toLowerCase();
      if (metrics.bridgeStats[bridgeKey]) {
        metrics.bridgeStats[bridgeKey].requests++;
        if (success) {
          metrics.bridgeStats[bridgeKey].success++;
        } else {
          metrics.bridgeStats[bridgeKey].error++;
        }
        
        // Update average response time for this bridge
        const currentBridgeTotal = metrics.bridgeStats[bridgeKey].avgResponseTime * 
                                 (metrics.bridgeStats[bridgeKey].requests - 1);
        metrics.bridgeStats[bridgeKey].avgResponseTime = 
          (currentBridgeTotal + responseTime) / metrics.bridgeStats[bridgeKey].requests;
      }
    }
  } catch (error) {
    logMessage(`Error tracking request: ${error.message}`, 'WARNING', { error });
  }
}

// Update pending requests count
function updatePendingRequests(bridge, count) {
  try {
    if (bridge && metrics.pendingRequests[bridge.toLowerCase()] !== undefined) {
      metrics.pendingRequests[bridge.toLowerCase()] = count;
    }
  } catch (error) {
    logMessage(`Error updating pending requests: ${error.message}`, 'WARNING', { error });
  }
}

// Start monitoring
function startMonitoring() {
  if (config.monitoring?.enabled) {
    logMessage('Starting system monitoring', 'INFO');
    
    // Initial metrics update
    updateMetrics();
    
    // Schedule regular updates
    const intervalMs = config.monitoring?.intervalMs || 60000; // Default to 1 minute
    setInterval(updateMetrics, intervalMs);
    
    return true;
  }
  
  return false;
}

// Get current metrics
function getMetrics() {
  return metrics;
}

// Get system health status
function getHealthStatus() {
  updateMetrics();
  
  const alerts = checkAlerts();
  const healthy = alerts.length === 0 && 
                 metrics.bridgeStatus.surface && 
                 metrics.bridgeStatus.deep &&
                 (!config.innerLifeEnabled || metrics.innerLifeStatus.running);
  
  return {
    healthy: healthy,
    status: healthy ? 'healthy' : 'unhealthy',
    uptime: metrics.uptime,
    alerts: alerts,
    bridgeStatus: metrics.bridgeStatus,
    innerLifeStatus: metrics.innerLifeStatus,
    requestStats: metrics.requestStats,
    memoryUsage: metrics.memoryUsage,
    cpuUsage: metrics.cpuUsage,
    timestamp: new Date().toISOString()
  };
}

module.exports = {
  startMonitoring,
  updateMetrics,
  getMetrics,
  getHealthStatus,
  trackRequest,
  updatePendingRequests
};
