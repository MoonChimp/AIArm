// NexusAI API Connector
// Connects HTML interface to NexusAI Python backend

class NexusAIConnector {
    constructor(apiUrl = 'http://127.0.0.1:8001') {
        this.apiUrl = apiUrl;
        this.ws = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    // Connect to WebSocket for real-time updates
    connectWebSocket() {
        try {
            this.ws = new WebSocket(`ws://127.0.0.1:8001/ws`);
            
            this.ws.onopen = () => {
                console.log('✅ Connected to NexusAI');
                this.connected = true;
                this.reconnectAttempts = 0;
                this.updateStatus('Connected', 'success');
                
                // Send initial handshake
                this.ws.send(JSON.stringify({
                    type: 'handshake',
                    client: 'NexusAI Web Interface',
                    timestamp: new Date().toISOString()
                }));
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('Failed to parse message:', error);
                }
            };

            this.ws.onerror = (error) => {
                console.error('❌ WebSocket error:', error);
                this.updateStatus('Connection Error', 'error');
            };

            this.ws.onclose = () => {
                console.log('🔌 Disconnected from NexusAI');
                this.connected = false;
                this.updateStatus('Disconnected', 'warning');
                
                // Attempt reconnect with exponential backoff
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
                    console.log(`Reconnecting in ${delay}ms...`);
                    setTimeout(() => {
                        this.reconnectAttempts++;
                        this.connectWebSocket();
                    }, delay);
                } else {
                    this.updateStatus('Connection Failed - Using HTTP fallback', 'warning');
                }
            };
        } catch (error) {
            console.error('Failed to create WebSocket:', error);
            this.updateStatus('WebSocket unavailable - Using HTTP', 'warning');
        }
    }

    // Send chat message via HTTP
    async sendChat(message, userId = 'web_user') {
        try {
            console.log('📤 Sending chat:', message);
            
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: userId,
                    timestamp: new Date().toISOString()
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('📥 Received response:', data);
            return data;
        } catch (error) {
            console.error('❌ Chat error:', error);
            return { 
                status: 'error', 
                response: `Failed to connect to NexusAI: ${error.message}` 
            };
        }
    }

    // Send command via HTTP
    async sendCommand(command, parameters = {}) {
        try {
            console.log('📤 Sending command:', command, parameters);
            
            const response = await fetch(`${this.apiUrl}/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    parameters: parameters,
                    timestamp: new Date().toISOString()
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('📥 Command response:', data);
            return data;
        } catch (error) {
            console.error('❌ Command error:', error);
            return { 
                status: 'error', 
                response: `Command failed: ${error.message}` 
            };
        }
    }

    // Generate image
    async generateImage(prompt) {
        this.updateStatus('Generating image...', 'info');
        const result = await this.sendCommand('/generate_image', { prompt: prompt });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Generate video
    async generateVideo(prompt) {
        this.updateStatus('Generating video...', 'info');
        const result = await this.sendCommand('/generate_video', { prompt: prompt });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Generate music
    async generateMusic(prompt) {
        this.updateStatus('Generating music...', 'info');
        const result = await this.sendCommand('/generate_music', { prompt: prompt });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Generate website
    async generateWebsite(description) {
        this.updateStatus('Generating website...', 'info');
        const result = await this.sendCommand('/generate_website', { description: description });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Generate UI design
    async generateUI(description) {
        this.updateStatus('Generating UI design...', 'info');
        const result = await this.sendCommand('/generate_ui', { description: description });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Generate code
    async generateCode(description, language = 'python') {
        this.updateStatus('Generating code...', 'info');
        const result = await this.sendCommand('/generate_code', { 
            description: description, 
            language: language 
        });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Trading signals
    async getTradingSignals(symbol = 'BTC/USD') {
        this.updateStatus('Analyzing markets...', 'info');
        const result = await this.sendCommand('/trading_signals', { symbol: symbol });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Market analysis
    async analyzeMarket(content, type = 'general') {
        this.updateStatus('Analyzing content...', 'info');
        const result = await this.sendCommand('/analyze', { 
            content: content, 
            type: type 
        });
        this.updateStatus('Connected', 'success');
        return result;
    }

    // Get available agents
    async getAgents() {
        try {
            const response = await fetch(`${this.apiUrl}/agents`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Failed to get agents:', error);
            return [];
        }
    }

    // Get capabilities
    async getCapabilities() {
        try {
            const response = await fetch(`${this.apiUrl}/capabilities`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Failed to get capabilities:', error);
            return { capabilities: [] };
        }
    }

    // Handle incoming WebSocket messages
    handleMessage(data) {
        console.log('📨 Received message:', data);
        
        if (data.type === 'chat_response') {
            this.displayResponse(data.response, 'ai');
        } else if (data.type === 'artifact') {
            this.displayArtifact(data);
        } else if (data.type === 'status') {
            this.updateStatus(data.message, data.level || 'info');
        } else if (data.type === 'progress') {
            this.updateProgress(data.progress, data.message);
        } else if (data.type === 'error') {
            this.displayResponse(`Error: ${data.message}`, 'error');
        }
    }

    // Display response in UI
    displayResponse(response, type = 'ai') {
        const responseArea = document.getElementById('response-area');
        if (!responseArea) {
            console.warn('Response area not found');
            return;
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message message-item`;
        
        // Parse markdown-style formatting
        const formattedResponse = this.formatResponse(response);
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${formattedResponse}</div>
                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
            </div>
        `;
        
        responseArea.appendChild(messageDiv);
        
        // Smooth scroll to bottom
        responseArea.scrollTo({
            top: responseArea.scrollHeight,
            behavior: 'smooth'
        });

        // Add fade-in animation
        setTimeout(() => {
            messageDiv.style.opacity = '1';
        }, 10);
    }

    // Format response text (basic markdown support)
    formatResponse(text) {
        if (!text) return '';
        
        // Convert newlines to <br>
        text = text.replace(/\n/g, '<br>');
        
        // Bold text **text**
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text *text*
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Code blocks `code`
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');
        
        return text;
    }

    // Display artifact (image, code, video, etc.)
    displayArtifact(artifact) {
        const artifactArea = document.getElementById('artifact-display');
        if (!artifactArea) {
            console.warn('Artifact display area not found');
            return;
        }

        // Clear placeholder
        artifactArea.innerHTML = '';

        const container = document.createElement('div');
        container.className = 'artifact-content';

        if (artifact.type === 'image') {
            const img = document.createElement('img');
            img.src = artifact.url || artifact.data;
            img.className = 'artifact-image';
            img.alt = artifact.description || 'Generated image';
            container.appendChild(img);
            
            if (artifact.description) {
                const caption = document.createElement('p');
                caption.className = 'artifact-caption';
                caption.textContent = artifact.description;
                container.appendChild(caption);
            }
        } else if (artifact.type === 'code') {
            const pre = document.createElement('pre');
            const code = document.createElement('code');
            code.className = `language-${artifact.language || 'python'}`;
            code.textContent = artifact.content;
            pre.appendChild(code);
            container.appendChild(pre);
            
            // Add copy button
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-code-btn';
            copyBtn.textContent = 'Copy';
            copyBtn.onclick = () => {
                navigator.clipboard.writeText(artifact.content);
                copyBtn.textContent = 'Copied!';
                setTimeout(() => copyBtn.textContent = 'Copy', 2000);
            };
            container.appendChild(copyBtn);
        } else if (artifact.type === 'video') {
            const video = document.createElement('video');
            video.src = artifact.url || artifact.data;
            video.controls = true;
            video.className = 'artifact-video';
            container.appendChild(video);
        } else if (artifact.type === 'audio') {
            const audio = document.createElement('audio');
            audio.src = artifact.url || artifact.data;
            audio.controls = true;
            audio.className = 'artifact-audio';
            container.appendChild(audio);
        } else if (artifact.type === 'html') {
            const iframe = document.createElement('iframe');
            iframe.srcdoc = artifact.content;
            iframe.className = 'artifact-iframe';
            container.appendChild(iframe);
        } else {
            container.innerHTML = `<p>Unsupported artifact type: ${artifact.type}</p>`;
        }

        artifactArea.appendChild(container);
    }

    // Update status indicator
    updateStatus(message, level = 'info') {
        const statusElement = document.getElementById('nexus-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status status-${level}`;
        }
        console.log(`[${level.toUpperCase()}] ${message}`);
    }

    // Update progress bar
    updateProgress(progress, message = '') {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
        
        if (progressText && message) {
            progressText.textContent = message;
        }
    }

    // Test connection
    async testConnection() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (response.ok) {
                const data = await response.json();
                console.log('✅ Health check:', data);
                return true;
            }
            return false;
        } catch (error) {
            console.error('❌ Health check failed:', error);
            return false;
        }
    }
}

// Initialize NexusAI connector
const nexusAI = new NexusAIConnector();

// Connect on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 NexusAI Interface Initializing...');
    
    // Test HTTP connection first
    const isConnected = await nexusAI.testConnection();
    
    if (isConnected) {
        console.log('✅ HTTP connection successful');
        // Try WebSocket connection
        nexusAI.connectWebSocket();
    } else {
        console.warn('⚠️ Backend not responding - check if NEXUS_ULTIMATE_INTERFACE.py is running');
        nexusAI.updateStatus('Backend Offline - Start NEXUS_ULTIMATE_INTERFACE.py', 'error');
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NexusAIConnector;
}

