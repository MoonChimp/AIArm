/**
 * NexusAI Commercial - Electron Preload Script
 * Provides secure communication between main and renderer processes
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // App information
    getAppPath: () => ipcRenderer.invoke('get-app-path'),
    getBackendStatus: () => ipcRenderer.invoke('get-backend-status'),

    // File dialogs
    showSaveDialog: (options) => ipcRenderer.invoke('show-save-dialog', options),
    showOpenDialog: (options) => ipcRenderer.invoke('show-open-dialog', options),

    // Chat functionality
    sendMessage: (message, sessionId) => ipcRenderer.invoke('send-message', message, sessionId),
    setPersonality: (mode) => ipcRenderer.invoke('set-personality', mode),

    // Event listeners
    onNewChatSession: (callback) => ipcRenderer.on('new-chat-session', callback),
    onClearMemory: (callback) => ipcRenderer.on('clear-memory', callback),
    onGenerateImage: (callback) => ipcRenderer.on('generate-image', callback),
    onExecuteCode: (callback) => ipcRenderer.on('execute-code', callback),
    onSetPersonality: (callback) => ipcRenderer.on('set-personality', callback),

    // Remove event listeners
    removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),

    // Platform information
    platform: process.platform,
    versions: process.versions,
});

// Also expose a simple API for the cinematic interface
contextBridge.exposeInMainWorld('nexusAPI', {
    // Chat functionality
    chat: {
        sendMessage: async (message, sessionId = 'default') => {
            try {
                const response = await fetch('http://localhost:5000/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: sessionId,
                        personality_mode: 'balanced',
                        model: 'nexusai-tools:latest'
                    })
                });

                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('Chat API error:', error);
                throw error;
            }
        },

        generateImage: async (prompt) => {
            try {
                const response = await fetch('http://localhost:5000/api/cinema/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        aspect_ratio: '16:9',
                        film_look: 'cinematic'
                    })
                });

                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('Image generation error:', error);
                throw error;
            }
        },

        executeCode: async (code, type = 'python') => {
            try {
                const response = await fetch('http://localhost:5000/api/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        type: type
                    })
                });

                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('Code execution error:', error);
                throw error;
            }
        }
    },

    // File operations
    files: {
        readFile: async (filepath) => {
            try {
                const response = await fetch('http://localhost:5000/api/files/read', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ path: filepath })
                });

                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('File read error:', error);
                throw error;
            }
        },

        writeFile: async (filepath, content) => {
            try {
                const response = await fetch('http://localhost:5000/api/files/write', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        path: filepath,
                        content: content
                    })
                });

                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('File write error:', error);
                throw error;
            }
        },

        listDirectory: async (directory) => {
            try {
                const response = await fetch('http://localhost:5000/api/files/list', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ directory: directory })
                });

                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('Directory list error:', error);
                throw error;
            }
        }
    },

    // Memory and learning
    memory: {
        getSessions: async () => {
            try {
                const response = await fetch('http://localhost:5000/api/memory/sessions');
                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('Memory sessions error:', error);
                throw error;
            }
        },

        clearSession: async (sessionId) => {
            try {
                const response = await fetch(`http://localhost:5000/api/memory/clear/${sessionId}`, {
                    method: 'POST'
                });

                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('Clear session error:', error);
                throw error;
            }
        }
    },

    // Self-awareness
    awareness: {
        getInfo: async () => {
            try {
                const response = await fetch('http://localhost:5000/api/self-awareness');
                if (response.ok) {
                    return await response.json();
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            } catch (error) {
                console.error('Self-awareness error:', error);
                throw error;
            }
        }
    }
});

// Console logging for debugging
console.log('NexusAI preload script loaded');
console.log('Available APIs:', Object.keys(window.nexusAPI || {}));
