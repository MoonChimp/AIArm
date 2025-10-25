const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const OllamaClient = require('./src/api/ollamaClient');
const config = require('./src/config/apiConfig');

// Keep a global reference of the window object
let mainWindow;
let ollamaClient;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    },
    icon: path.join(__dirname, 'assets', 'NexusLogo.gif'),
    title: 'NexusAI Assistant',
    show: false // Don't show until ready
  });

  // Load the index.html of the app
  mainWindow.loadFile('src/index.html');

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  // Emitted when the window is closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function initializeAI() {
  // Initialize Ollama client
  ollamaClient = new OllamaClient();
  console.log('NexusAI Assistant initialized with Ollama client');
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
  createWindow();
  initializeAI();
});

// Quit when all windows are closed
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// On macOS, re-create window when dock icon is clicked
app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// IPC handlers for communication with renderer process
ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

// Test Ollama connection
ipcMain.handle('test-ollama-connection', async () => {
  try {
    const result = await ollamaClient.testConnection();
    return result;
  } catch (error) {
    return {
      success: false,
      available: false,
      error: error.message,
      message: 'Failed to test Ollama connection'
    };
  }
});

// Get available models
ipcMain.handle('get-available-models', async () => {
  try {
    const result = await ollamaClient.getAvailableModels();
    return result;
  } catch (error) {
    return {
      success: false,
      error: error.message,
      models: []
    };
  }
});

// Process message from user
ipcMain.handle('process-message', async (event, data) => {
  const { message, mode, history } = data;
  
  try {
    console.log(`Processing ${mode} mode message:`, message.substring(0, 100) + '...');
    
    // Build context from conversation history
    let contextualMessage = message;
    if (history && history.length > 0) {
      const recentHistory = history.slice(-10); // Last 10 messages for context
      const contextString = recentHistory
        .map(msg => `${msg.type}: ${msg.content}`)
        .join('\n');
      
      contextualMessage = `Previous conversation:\n${contextString}\n\nCurrent message: ${message}`;
    }
    
    // Add mode-specific instructions
    const modeInstructions = mode === 'plan' 
      ? '\n\nYou are in PLAN mode. Focus on analyzing the task, breaking it down into steps, and providing a detailed plan before execution.'
      : '\n\nYou are in ACT mode. Execute tasks directly and provide concrete results.';
    
    contextualMessage += modeInstructions;
    
    // Send to AI
    const aiResponse = await ollamaClient.sendMessage(contextualMessage, {
      temperature: 0.7,
      max_tokens: 2000
    });
    
    if (aiResponse.success) {
      return {
        success: true,
        response: aiResponse.response,
        provider: aiResponse.provider,
        model: aiResponse.model
      };
    } else {
      // Fallback to a basic response if AI fails
      return {
        success: true,
        response: `I apologize, but I'm having trouble connecting to the AI model. Please ensure Ollama is running with the nexusai-agent-enhanced:latest model loaded.\n\nError: ${aiResponse.error}`,
        provider: 'fallback',
        model: 'none'
      };
    }
  } catch (error) {
    console.error('Error processing message:', error);
    return {
      success: false,
      error: error.message,
      response: `I encountered an error while processing your message: ${error.message}`
    };
  }
});

// Update settings
ipcMain.handle('update-settings', async (event, settings) => {
  try {
    // Update config with new settings
    if (settings.ollamaUrl) {
      config.ollama.baseUrl = settings.ollamaUrl;
    }
    if (settings.modelName) {
      config.ollama.model = settings.modelName;
    }
    if (typeof settings.enableFallback === 'boolean') {
      config.claude.enabled = settings.enableFallback;
    }
    
    // Reinitialize Ollama client with new settings
    ollamaClient = new OllamaClient();
    
    console.log('Settings updated:', settings);
    return { success: true };
  } catch (error) {
    console.error('Error updating settings:', error);
    return { success: false, error: error.message };
  }
});

// Load conversation from file - REAL IMPLEMENTATION
ipcMain.handle('load-conversation', async (event, filePath) => {
  const fs = require('fs').promises;
  const path = require('path');
  
  try {
    console.log('📂 Loading conversation from:', filePath);
    
    // Ensure the conversation directory exists
    const conversationDir = path.join(__dirname, 'conversations');
    await fs.mkdir(conversationDir, { recursive: true });
    
    // If filePath is relative, make it absolute to the conversations directory
    const absolutePath = path.isAbsolute(filePath) 
      ? filePath 
      : path.join(conversationDir, filePath);
    
    const content = await fs.readFile(absolutePath, 'utf8');
    const conversation = JSON.parse(content);
    
    console.log('✅ Conversation loaded successfully');
    return {
      success: true,
      conversation: conversation,
      path: absolutePath
    };
  } catch (error) {
    console.error('❌ Failed to load conversation:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
});

// Save conversation to file - REAL IMPLEMENTATION
ipcMain.handle('save-conversation', async (event, conversationData) => {
  const fs = require('fs').promises;
  const path = require('path');
  
  try {
    console.log('💾 Saving conversation...');
    
    // Ensure the conversation directory exists
    const conversationDir = path.join(__dirname, 'conversations');
    await fs.mkdir(conversationDir, { recursive: true });
    
    // Generate filename if not provided
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = conversationData.filename || `conversation_${timestamp}.json`;
    const filePath = path.join(conversationDir, filename);
    
    // Create conversation object
    const conversation = {
      conversation_id: conversationData.id || timestamp,
      timestamp: new Date().toISOString(),
      messages: conversationData.messages || [],
      metadata: {
        version: "2.0",
        model_used: conversationData.model || config.ollama.model,
        total_messages: conversationData.messages?.length || 0,
        ...conversationData.metadata
      }
    };
    
    await fs.writeFile(filePath, JSON.stringify(conversation, null, 2), 'utf8');
    
    console.log('✅ Conversation saved to:', filePath);
    return {
      success: true,
      path: filePath,
      filename: filename
    };
  } catch (error) {
    console.error('❌ Failed to save conversation:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
});

// List available conversations - REAL IMPLEMENTATION
ipcMain.handle('list-conversations', async (event) => {
  const fs = require('fs').promises;
  const path = require('path');
  
  try {
    console.log('📋 Listing conversations...');
    
    const conversationDir = path.join(__dirname, 'conversations');
    await fs.mkdir(conversationDir, { recursive: true });
    
    const files = await fs.readdir(conversationDir);
    const conversations = [];
    
    for (const file of files) {
      if (file.endsWith('.json')) {
        try {
          const filePath = path.join(conversationDir, file);
          const stats = await fs.stat(filePath);
          const content = await fs.readFile(filePath, 'utf8');
          const conversation = JSON.parse(content);
          
          conversations.push({
            filename: file,
            path: filePath,
            size: stats.size,
            modified: stats.mtime,
            created: stats.birthtime,
            id: conversation.conversation_id,
            messageCount: conversation.messages?.length || 0,
            preview: conversation.messages?.[0]?.content?.substring(0, 100) || 'No messages'
          });
        } catch (error) {
          console.error(`Error reading conversation ${file}:`, error.message);
        }
      }
    }
    
    // Sort by modification date (newest first)
    conversations.sort((a, b) => new Date(b.modified) - new Date(a.modified));
    
    console.log(`✅ Found ${conversations.length} conversations`);
    return {
      success: true,
      conversations: conversations
    };
  } catch (error) {
    console.error('❌ Failed to list conversations:', error.message);
    return {
      success: false,
      error: error.message,
      conversations: []
    };
  }
});

// Handle file operations - REAL IMPLEMENTATION
ipcMain.handle('file-operation', async (event, operation) => {
  const fs = require('fs').promises;
  const path = require('path');
  
  try {
    console.log('🗂️ File operation:', operation.type, operation.path);
    
    switch (operation.type) {
      case 'read':
        const content = await fs.readFile(operation.path, 'utf8');
        return { success: true, content };
        
      case 'write':
        // Create directory if it doesn't exist
        await fs.mkdir(path.dirname(operation.path), { recursive: true });
        await fs.writeFile(operation.path, operation.content, 'utf8');
        return { success: true, message: `File written to ${operation.path}` };
        
      case 'list':
        const items = await fs.readdir(operation.path, { withFileTypes: true });
        const detailed = items.map(item => ({
          name: item.name,
          isDirectory: item.isDirectory(),
          path: path.join(operation.path, item.name)
        }));
        return { success: true, items: detailed, path: operation.path };
        
      case 'exists':
        try {
          await fs.access(operation.path);
          return { success: true, exists: true };
        } catch {
          return { success: true, exists: false };
        }
        
      default:
        return { success: false, error: `Unknown file operation: ${operation.type}` };
    }
  } catch (error) {
    console.error('File operation error:', error);
    return { success: false, error: error.message };
  }
});

// Handle command execution - REAL IMPLEMENTATION
ipcMain.handle('execute-command', async (event, commandData) => {
  const { exec } = require('child_process');
  const util = require('util');
  const execAsync = util.promisify(exec);
  
  try {
    console.log('⚡ Executing command:', commandData.command);
    
    const options = {
      cwd: commandData.cwd || process.cwd(),
      timeout: commandData.timeout || 60000,
      maxBuffer: 1024 * 1024 * 10, // 10MB buffer
      encoding: 'utf8'
    };
    
    const result = await execAsync(commandData.command, options);
    
    console.log('✅ Command completed successfully');
    return {
      success: true,
      stdout: result.stdout,
      stderr: result.stderr,
      command: commandData.command,
      cwd: options.cwd
    };
  } catch (error) {
    console.error('❌ Command failed:', error.message);
    return {
      success: false,
      error: error.message,
      stdout: error.stdout || '',
      stderr: error.stderr || '',
      command: commandData.command,
      exitCode: error.code
    };
  }
});

// Handle web browsing - REAL IMPLEMENTATION  
ipcMain.handle('web-browse', async (event, action) => {
  try {
    console.log('🌐 Web browsing:', action.type);
    
    switch (action.type) {
      case 'open':
        const { shell } = require('electron');
        await shell.openExternal(action.url);
        return { success: true, message: `Opened ${action.url} in default browser` };
        
      case 'fetch':
        const https = require('https');
        const http = require('http');
        
        return new Promise((resolve) => {
          const client = action.url.startsWith('https') ? https : http;
          
          client.get(action.url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
              resolve({
                success: true,
                content: data,
                statusCode: res.statusCode,
                headers: res.headers
              });
            });
          }).on('error', (error) => {
            resolve({
              success: false,
              error: error.message
            });
          });
        });
        
      default:
        return { success: false, error: `Unknown web action: ${action.type}` };
    }
  } catch (error) {
    console.error('Web browsing error:', error);
    return { success: false, error: error.message };
  }
});

// Error handling
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

console.log('NexusAI Assistant starting up...');
