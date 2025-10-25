/**
 * AIArm HRM System Configuration
 * This file contains configuration options for the concurrent bridge server
 * PRODUCTION-READY Version with enhanced error handling and monitoring
 */

// Load environment-specific settings from config.json
const fs = require('fs');
const path = require('path');
let jsonConfig = {};

try {
  const configPath = path.join(__dirname, 'config.json');
  if (fs.existsSync(configPath)) {
    jsonConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    console.log('Loaded configuration from config.json');
  }
} catch (error) {
  console.error('Error loading config.json:', error.message);
  console.log('Using default configuration');
}

// Determine environment
const NODE_ENV = process.env.NODE_ENV || 'production';
const isProd = NODE_ENV === 'production';

module.exports = {
  // Environment
  environment: NODE_ENV,
  isProd: isProd,
  
  // Server configuration
  port: process.env.PORT || jsonConfig.port || 45678,
  
  // Bridge files
  surfaceBridge: process.env.SURFACE_BRIDGE || jsonConfig.surfaceBridge || 'improved_bridge.py',
  deepBridge: process.env.DEEP_BRIDGE || jsonConfig.deepBridge || 'ollama_bridge.py',
  
  // Bridge failover settings
  bridgeFailover: {
    enabled: true,
    maxFailures: 3,
    recoverAfterMs: 60000, // 1 minute recovery time
    fallbackStrategy: jsonConfig.fallbackStrategy || 'prefer-surface' // 'prefer-surface', 'prefer-deep', 'surface-only', 'deep-only'
  },
  
  // Request handling
  timeoutMs: jsonConfig.timeoutMs || 120000, // 2 minute timeout for production workloads
  maxConcurrentRequests: jsonConfig.maxConcurrentRequests || 10,
  errorRetryCount: jsonConfig.retryAttempts || 3,
  requestTimeoutStrategy: 'graceful-degradation', // Return partial results if one bridge times out
  
  // Memory settings
  memoryEnabled: true,
  memoryDirectory: process.env.MEMORY_DIR || 'D:/AIArm/Memory',
  memoryBackupEnabled: true,
  memoryBackupInterval: 3600000, // 1 hour
  
  // Logging
  logLevel: isProd ? (jsonConfig.logLevel || 'info') : 'debug', // 'debug', 'info', 'warn', 'error'
  logToConsole: true,
  logToFile: true,
  logDirectory: 'D:/AIArm/Logs',
  logRotationSize: '10M', // Rotate logs at 10MB
  logRetentionDays: jsonConfig.logging?.logRotationDays || 7,
  
  // Inner Life settings
  innerLifeEnabled: true,
  innerLifeDirectory: process.env.INNER_LIFE_DIR || 'D:/AIArm/InnerLife',
  innerLifeMonitoring: true,
  innerLifeHeartbeatInterval: 30000, // 30 second heartbeat check
  
  // Security settings
  rateLimiting: {
    enabled: isProd,
    windowMs: 15 * 60 * 1000, // 15 minutes
    maxRequests: 100, // 100 requests per windowMs
    trustProxy: true
  },
  
  // Error handling
  errorHandling: {
    retryOnTimeout: true,
    gracefulShutdown: true,
    logErrors: true,
    monitorErrors: true,
    errorThresholdForAlert: 5 // Number of errors before triggering an alert
  },
  
  // System monitoring
  monitoring: {
    enabled: true,
    metricsEnabled: jsonConfig.monitoring?.enableMetrics || true,
    healthCheckEnabled: jsonConfig.monitoring?.enableHealthCheck || true,
    intervalMs: jsonConfig.monitoring?.statusCheckIntervalMs || 300000, // 5 minutes
    alertThresholds: {
      cpuUsage: 80, // Alert if CPU usage exceeds 80%
      memoryUsage: 80, // Alert if memory usage exceeds 80%
      responseTimeMs: 5000 // Alert if response time exceeds 5 seconds
    }
  },
  
  // Performance settings
  caching: {
    enabled: true,
    ttl: 3600, // 1 hour cache TTL
    maxSize: 1000, // Maximum number of cached items
    excludedRoutes: ['/api/system-monitor', '/health']
  },
  
  // HRM response configuration
  responseConfig: jsonConfig.responseConfiguration || {
    similarityThreshold: 0.5,
    combinationMethod: 'augment-surface',
    preferDeepForDomains: ['reasoning', 'philosophy', 'creativity']
  },
  
  // System recovery
  recovery: {
    enabled: true,
    autoRestart: true,
    maxRestarts: 5,
    backoffMs: 5000, // Wait 5 seconds before restarting, doubles each retry
    persistentStorage: true
  }
};
