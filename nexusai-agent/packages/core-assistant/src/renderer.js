// NexusAI Assistant - Renderer Process
const { ipcRenderer } = require('electron');

class NexusAIRenderer {
    constructor() {
        this.currentMode = 'act'; // 'plan' or 'act'
        this.isConnected = false;
        this.conversationHistory = [];
        this.taskProgress = [];
        
        this.initializeElements();
        this.setupEventListeners();
        this.checkOllamaConnection();
        this.loadLatestConversation();
    }

    initializeElements() {
        this.chatContainer = document.getElementById('chat-container');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.loadingText = document.getElementById('loading-text');
        this.planActToggle = document.getElementById('plan-act-toggle');
        this.settingsBtn = document.getElementById('settings-btn');
        this.connectionStatus = document.getElementById('connection-status');
        this.modelStatus = document.getElementById('model-status');
        this.modeStatus = document.getElementById('mode-status');
        this.sidePanel = document.getElementById('side-panel');
        this.closePanelBtn = document.getElementById('close-panel');
        this.testConnectionBtn = document.getElementById('test-connection');
        this.refreshModelsBtn = document.getElementById('refresh-models');
        this.ollamaUrlInput = document.getElementById('ollama-url');
        this.modelNameInput = document.getElementById('model-name');
        this.enableFallbackCheckbox = document.getElementById('enable-fallback');
        this.taskProgressDiv = document.getElementById('task-progress');
        this.progressItems = document.getElementById('progress-items');
        this.loadConversationBtn = document.getElementById('load-conversation');
        this.saveConversationBtn = document.getElementById('save-conversation');
        this.conversationsList = document.getElementById('conversations-list');
    }

    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        this.planActToggle.addEventListener('click', () => this.toggleMode());
        this.settingsBtn.addEventListener('click', () => this.toggleSidePanel());
        this.closePanelBtn.addEventListener('click', () => this.toggleSidePanel());
        this.testConnectionBtn.addEventListener('click', () => this.testOllamaConnection());
        this.refreshModelsBtn.addEventListener('click', () => this.refreshAvailableModels());
        this.ollamaUrlInput.addEventListener('change', () => this.saveSettings());
        this.modelNameInput.addEventListener('change', () => this.saveSettings());
        this.enableFallbackCheckbox.addEventListener('change', () => this.saveSettings());
        this.userInput.addEventListener('input', () => this.autoResizeTextarea());
        document.addEventListener('click', (e) => {
            if (this.sidePanel.classList.contains('open') && 
                !this.sidePanel.contains(e.target) && 
                !this.settingsBtn.contains(e.target)) {
                this.toggleSidePanel();
            }
        });
        this.userInput.addEventListener('focus', () => {
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage && this.conversationHistory.length === 0) {
                welcomeMessage.style.opacity = '0.7';
            }
        });
        this.userInput.addEventListener('blur', () => {
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage && this.conversationHistory.length === 0) {
                welcomeMessage.style.opacity = '1';
            }
        });
        if (this.loadConversationBtn) {
            this.loadConversationBtn.addEventListener('click', () => this.showLoadConversationDialog());
        }
        if (this.saveConversationBtn) {
            this.saveConversationBtn.addEventListener('click', () => this.saveCurrentConversation());
        }
    }

    async checkOllamaConnection() {
        try {
            const result = await ipcRenderer.invoke('test-ollama-connection');
            if (result.success && result.available) {
                this.updateConnectionStatus(true);
            } else {
                this.updateConnectionStatus(false);
            }
        } catch (error) {
            this.updateConnectionStatus(false);
        }
    }

    updateConnectionStatus(connected) {
        this.isConnected = connected;
        const statusDot = this.connectionStatus.querySelector('.status-dot');
        const statusText = this.connectionStatus.querySelector('.status-text');
        if (connected) {
            this.connectionStatus.classList.add('connected');
            statusText.textContent = 'Ollama Connected';
        } else {
            this.connectionStatus.classList.remove('connected');
            statusText.textContent = 'Ollama Disconnected';
        }
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;
        this.setInputEnabled(false);
        this.showLoading('NexusAI is thinking...');
        if (this.conversationHistory.length === 0) {
            this.clearWelcomeMessage();
        }
        this.addMessage('user', message);
        this.userInput.value = '';
        this.autoResizeTextarea();
        try {
            const response = await ipcRenderer.invoke('process-message', {
                message: message,
                mode: this.currentMode,
                history: this.conversationHistory
            });
            if (response.success) {
                this.addMessage('assistant', response.response);
                if (response.taskProgress) {
                    this.updateTaskProgress(response.taskProgress);
                }
                if (response.suggestedMode && response.suggestedMode !== this.currentMode) {
                    this.showModeChangePrompt(response.suggestedMode);
                }
            } else {
                this.addMessage('error', `Error: ${response.error}`);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('error', `Failed to process message: ${error.message}`);
        } finally {
            this.hideLoading();
            this.setInputEnabled(true);
            this.userInput.focus();
        }
    }

    addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        if (type === 'error') {
            messageContent.style.background = 'rgba(239, 68, 68, 0.1)';
            messageContent.style.borderColor = 'rgba(239, 68, 68, 0.2)';
            messageContent.style.color = '#fca5a5';
        }
        messageContent.innerHTML = this.formatMessage(content);
        messageDiv.appendChild(messageContent);
        this.chatContainer.appendChild(messageDiv);
        this.conversationHistory.push({ type, content });
        this.scrollToBottom();
        this.autoSaveConversation();
    }

    formatMessage(content) {
        return content
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '');
    }

    clearWelcomeMessage() {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.animation = 'fadeOut 0.5s ease-out';
            setTimeout(() => {
                welcomeMessage.remove();
            }, 500);
        }
    }

    toggleMode() {
        this.currentMode = this.currentMode === 'act' ? 'plan' : 'act';
        this.updateModeDisplay();
    }

    updateModeDisplay() {
        this.planActToggle.textContent = this.currentMode.toUpperCase() + ' MODE';
        this.planActToggle.className = `plan-act-btn ${this.currentMode}-mode`;
        this.modeStatus.textContent = this.currentMode === 'act' ? 'Act Mode' : 'Plan Mode';
        this.modeStatus.className = `mode-status ${this.currentMode}`;
        const placeholder = this.currentMode === 'plan' 
            ? 'Describe your task for planning... (Shift+Enter for new line, Enter to send)'
            : 'Type your message here... (Shift+Enter for new line, Enter to send)';
        this.userInput.placeholder = placeholder;
    }

    toggleSidePanel() {
        this.sidePanel.classList.toggle('open');
    }

    async testOllamaConnection() {
        this.testConnectionBtn.textContent = 'Testing...';
        this.testConnectionBtn.disabled = true;
        try {
            const result = await ipcRenderer.invoke('test-ollama-connection');
            if (result.success && result.available) {
                this.updateConnectionStatus(true);
                this.showNotification('Connected to Ollama successfully!', 'success');
                if (result.models) {
                    this.updateAvailableModels(result.models);
                }
            } else {
                this.updateConnectionStatus(false);
                this.showNotification(result.message || 'Failed to connect to Ollama', 'error');
            }
        } catch (error) {
            this.updateConnectionStatus(false);
            this.showNotification(`Connection error: ${error.message}`, 'error');
        } finally {
            this.testConnectionBtn.textContent = 'Test Connection';
            this.testConnectionBtn.disabled = false;
        }
    }

    async refreshAvailableModels() {
        this.refreshModelsBtn.textContent = 'Refreshing...';
        this.refreshModelsBtn.disabled = true;
        try {
            const result = await ipcRenderer.invoke('get-available-models');
            if (result.success) {
                this.updateAvailableModels(result.models);
                this.showNotification(`Found ${result.models.length} models`, 'success');
            } else {
                this.showNotification('Failed to refresh models', 'error');
            }
        } catch (error) {
            this.showNotification(`Error refreshing models: ${error.message}`, 'error');
        } finally {
            this.refreshModelsBtn.textContent = 'Refresh Models';
            this.refreshModelsBtn.disabled = false;
        }
    }

    updateAvailableModels(models) {
        console.log('Available models:', models);
    }

    updateTaskProgress(progressItems) {
        if (!progressItems || progressItems.length === 0) {
            this.taskProgressDiv.style.display = 'none';
            return;
        }
        this.taskProgressDiv.style.display = 'block';
        this.progressItems.innerHTML = progressItems.map(item => 
            `<div class="progress-item">${item}</div>`
        ).join('');
    }

    showModeChangePrompt(suggestedMode) {
        const message = `The AI suggests switching to ${suggestedMode.toUpperCase()} mode for this task. Would you like to switch?`;
        if (confirm(message)) {
            this.currentMode = suggestedMode;
            this.updateModeDisplay();
        }
    }

    setInputEnabled(enabled) {
        this.userInput.disabled = !enabled;
        this.sendBtn.disabled = !enabled;
        if (enabled) {
            this.userInput.focus();
        }
    }

    showLoading(text = 'Processing...') {
        this.loadingText.textContent = text;
        this.loadingOverlay.classList.add('active');
    }

    hideLoading() {
        this.loadingOverlay.classList.remove('active');
    }

    autoResizeTextarea() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 200) + 'px';
    }

    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: ${type === 'error' ? 'rgba(239, 68, 68, 0.9)' : 'rgba(34, 197, 94, 0.9)'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        `;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    saveSettings() {
        const settings = {
            ollamaUrl: this.ollamaUrlInput.value,
            modelName: this.modelNameInput.value,
            enableFallback: this.enableFallbackCheckbox.checked
        };
        localStorage.setItem('nexusai-settings', JSON.stringify(settings));
        ipcRenderer.invoke('update-settings', settings);
    }

    loadSettings() {
        const saved = localStorage.getItem('nexusai-settings');
        if (saved) {
            const settings = JSON.parse(saved);
            this.ollamaUrlInput.value = settings.ollamaUrl || 'http://localhost:11434';
            this.modelNameInput.value = settings.modelName || 'nexusai-agent-enhanced:latest';
            this.enableFallbackCheckbox.checked = settings.enableFallback || false;
        }
    }

    async autoSaveConversation() {
        if (this.conversationHistory.length > 0) {
            try {
                const conversationData = {
                    messages: this.conversationHistory.map(msg => ({
                        [msg.type]: msg.content,
                        timestamp: new Date().toISOString()
                    })),
                    metadata: {
                        mode: this.currentMode,
                        messageCount: this.conversationHistory.length,
                        lastUpdated: new Date().toISOString(),
                        autoSaved: true
                    }
                };
                await ipcRenderer.invoke('save-conversation', conversationData);
            } catch (error) {
                console.error('Auto-save failed:', error.message);
            }
        }
    }

    async loadLatestConversation() {
        // Implementation for loading the latest conversation can be added here
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new NexusAIRenderer();
});
