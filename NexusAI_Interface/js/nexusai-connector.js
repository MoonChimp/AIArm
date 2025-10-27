// NexusAI API Connector
class NexusAIConnector {
    constructor(apiUrl = 'http://127.0.0.1:8001') {
        this.apiUrl = apiUrl;
        this.ws = null;
        this.connected = false;
    }

    async sendChat(message, userId = 'web_user') {
        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, user_id: userId })
            });
            const data = await response.json();
            return data;
        } catch (error) {
            return { status: 'error', response: `Failed: ${error.message}` };
        }
    }

    async sendCommand(command, parameters = {}) {
        try {
            const response = await fetch(`${this.apiUrl}/command`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: command, parameters: parameters })
            });
            const data = await response.json();
            return data;
        } catch (error) {
            return { status: 'error', response: `Command failed: ${error.message}` };
        }
    }

    displayResponse(response, type = 'ai') {
        const responseArea = document.getElementById('response-area');
        if (!responseArea) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${response}</div>
                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
            </div>
        `;
        responseArea.appendChild(messageDiv);
        responseArea.scrollTop = responseArea.scrollHeight;
    }

    updateStatus(message, level = 'info') {
        const statusElement = document.getElementById('nexus-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status status-${level}`;
        }
    }

    async testConnection() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}

const nexusAI = new NexusAIConnector();

document.addEventListener('DOMContentLoaded', async () => {
    const isConnected = await nexusAI.testConnection();
    if (isConnected) {
        nexusAI.updateStatus('Connected', 'success');
    } else {
        nexusAI.updateStatus('Backend Offline', 'error');
    }
});
