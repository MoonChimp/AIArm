/**
 * AIArm HRM System Configuration
 * This file contains configuration options for the concurrent bridge server
 */

module.exports = {
  // Server configuration
  port: process.env.PORT || 45678,
  
  // Bridge files
  surfaceBridge: 'improved_bridge.py',
  deepBridge: 'ollama_bridge.py',
  
  // Request handling
  timeoutMs: 120000, // 2 minute timeout for production workloads
  maxConcurrentRequests: 10,
  errorRetryCount: 3,
  
  // Memory settings
  memoryEnabled: true,
  memoryDirectory: 'D:/AIArm/Memory',
  
  // Logging
  logLevel: 'info', // 'debug', 'info', 'warn', 'error'
  logToConsole: true,
  logToFile: true,
  
  // Inner Life settings
  innerLifeEnabled: true,
  innerLifeDirectory: 'D:/AIArm/InnerLife',
  
  // Security settings
  rateLimiting: {
    enabled: true,
    windowMs: 15 * 60 * 1000, // 15 minutes
    maxRequests: 100 // 100 requests per windowMs
  },
  
  // Performance settings
  caching: {
    enabled: true,
    ttl: 3600 // 1 hour cache TTL
  }
};
