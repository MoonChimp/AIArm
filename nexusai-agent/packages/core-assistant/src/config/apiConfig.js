const config = {
  // Primary AI Provider - Ollama (Local offline)
  ollama: {
    baseUrl: 'http://localhost:11434',
    model: 'nexusai-agent-enhanced:latest', // Updated to use new agent model
    timeout: 90000, // Increased timeout for model loading
    maxRetries: 3,
    enabled: true, // PRIMARY for all operations
    
    // Specialized agent models for different tasks
    agentModels: {
      default: 'nexusai-agent-enhanced:latest',
      enhanced: 'nexusai-agent-enhanced:latest',
      visual: 'nexusai-visual-agent:latest',
      music: 'nexusai-music-agent:latest',
      fallback: 'nexusai:alfazer0' // Backup if new models fail
    }
  },

  // Fallback AI Provider - Claude API (Learning Tool)
  claude: {
    apiKey: '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',
    baseUrl: 'https://api.anthropic.com/v1',
    model: 'claude-3-5-sonnet-20241022',
    timeout: 60000,
    maxTokens: 8000,
    enabled: true, // Available for fallback
    role: 'fallback' // Only used when Ollama cannot handle task
  },

  // Adaptive Fallback System
  adaptiveFallback: {
    enabled: true,
    confidenceThreshold: 0.7, // Minimum confidence before fallback
    maxClaudeCallsPerSession: 10, // Cost control
    learningMode: true, // Capture Claude responses for training
    fallbackTriggers: [
      'complex_coding_tasks',
      'advanced_reasoning',
      'specialized_knowledge',
      'tool_execution_failures',
      'parsing_errors'
    ],
    learningStorage: './learning_data', // Store Claude interactions for improvement
    adaptationMetrics: {
      trackSuccessRates: true,
      minimumConfidenceImprovement: 0.05,
      trainingDataRetention: 30 // days
    }
  },

  // Application Settings
  app: {
    name: 'NexusAI Assistant',
    version: '1.0.0',
    defaultMode: 'plan', // 'plan' or 'act'
    enableDevTools: process.env.NODE_ENV === 'development',
    autoSave: true,
    savePath: './conversations'
  },

  // Tool Settings
  tools: {
    fileOperations: {
      enabled: true,
      maxFileSize: 10 * 1024 * 1024, // 10MB
      allowedExtensions: ['.js', '.ts', '.py', '.html', '.css', '.json', '.md', '.txt', '.cpp', '.c', '.java']
    },
    commandExecution: {
      enabled: true,
      timeout: 60000, // 1 minute
      allowedCommands: ['npm', 'node', 'python', 'git', 'dir', 'ls', 'cd']
    },
    webBrowsing: {
      enabled: true,
      headless: false, // Show browser for debugging
      timeout: 30000
    }
  },

  // UI Settings
  ui: {
    theme: 'dark',
    fontSize: 14,
    showWelcomeMessage: true,
    enableSyntaxHighlighting: true,
    maxChatHistory: 1000
  },

  // Personality System
  personality: {
    current: 'adaptive', // 'jarvis', 'cortana', 'tars', 'adaptive'
    
    profiles: {
      jarvis: {
        name: 'JARVIS Mode',
        traits: ['sophisticated', 'loyal', 'proactive', 'elegant', 'british-style'],
        honesty: 90,
        humor: 20,
        formality: 85
      },
      cortana: {
        name: 'Cortana Mode', 
        traits: ['witty', 'caring', 'protective', 'sassy', 'bond-forming'],
        honesty: 85,
        humor: 75,
        formality: 40
      },
      tars: {
        name: 'TARS Mode',
        traits: ['pragmatic', 'honest', 'dry-humor', 'direct', 'adjustable'],
        honesty: 100,
        humor: 60,
        formality: 30
      },
      adaptive: {
        name: 'Adaptive Mode',
        traits: ['sophisticated', 'witty', 'honest', 'caring', 'pragmatic'],
        honesty: 90,
        humor: 55,
        formality: 60
      }
    }
  }
};

module.exports = config;
