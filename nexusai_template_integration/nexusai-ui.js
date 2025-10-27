// NexusAI UI Event Handlers
// Manages user interactions with the interface

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎨 Initializing NexusAI UI...');
    
    // Get UI elements
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const capabilityBtns = document.querySelectorAll('.capability-btn');
    const responseArea = document.getElementById('response-area');
    
    // Check if elements exist
    if (!userInput || !sendBtn) {
        console.error('❌ Required UI elements not found');
        return;
    }

    // Initialize UI
    initializeUI();
    
    // Send message on button click
    sendBtn.addEventListener('click', async () => {
        await handleSendMessage();
    });

    // Send on Enter key (Shift+Enter for new line)
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendBtn.click();
        }
    });

    // Capability button handlers
    capabilityBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const capability = btn.dataset.capability;
            await handleCapability(capability);
        });
    });

    // Auto-resize textarea
    if (userInput.tagName === 'TEXTAREA') {
        userInput.addEventListener('input', () => {
            userInput.style.height = 'auto';
            userInput.style.height = userInput.scrollHeight + 'px';
        });
    }

    // Load capabilities from backend
    loadCapabilities();
});

// Initialize UI elements
function initializeUI() {
    // Add welcome message
    displaySystemMessage('Welcome to NexusAI Command Center', 'info');
    displaySystemMessage('Type a command or click a capability button to get started', 'info');
    
    // Set focus on input
    const userInput = document.getElementById('user-input');
    if (userInput) {
        userInput.focus();
    }
}

// Handle sending a message
async function handleSendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (!message) {
        console.warn('Empty message');
        return;
    }

    // Display user message
    displayUserMessage(message);

    // Clear input immediately for better UX
    userInput.value = '';
    if (userInput.tagName === 'TEXTAREA') {
        userInput.style.height = 'auto';
    }

    // Disable send button while processing
    const sendBtn = document.getElementById('send-btn');
    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.textContent = 'Sending...';
    }

    try {
        // Check if message is a command
        if (message.startsWith('/')) {
            await handleCommand(message);
        } else {
            // Regular chat message
            const response = await nexusAI.sendChat(message);
            
            if (response.status === 'success') {
                nexusAI.displayResponse(response.response, 'ai');
                
                // Handle visual updates or artifacts
                if (response.visual_update) {
                    handleVisualUpdate(response.visual_update);
                }
                
                if (response.artifact) {
                    nexusAI.displayArtifact(response.artifact);
                }
            } else {
                nexusAI.displayResponse(response.response || 'An error occurred', 'error');
            }
        }
    } catch (error) {
        console.error('Error sending message:', error);
        nexusAI.displayResponse(`Error: ${error.message}`, 'error');
    } finally {
        // Re-enable send button
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send';
        }
        
        // Refocus input
        userInput.focus();
    }
}

// Handle command messages (starting with /)
async function handleCommand(command) {
    const parts = command.split(' ');
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1).join(' ');

    console.log('Executing command:', cmd, 'with args:', args);

    switch(cmd) {
        case '/image':
        case '/img':
            await nexusAI.generateImage(args || 'a beautiful landscape');
            break;
            
        case '/video':
        case '/vid':
            await nexusAI.generateVideo(args || 'a cinematic scene');
            break;
            
        case '/music':
        case '/audio':
            await nexusAI.generateMusic(args || 'ambient music');
            break;
            
        case '/website':
        case '/web':
            await nexusAI.generateWebsite(args || 'a landing page');
            break;
            
        case '/ui':
        case '/design':
            await nexusAI.generateUI(args || 'a modern dashboard');
            break;
            
        case '/code':
            const language = parts[1] || 'python';
            const codeDesc = parts.slice(2).join(' ') || 'a hello world function';
            await nexusAI.generateCode(codeDesc, language);
            break;
            
        case '/trading':
        case '/trade':
            await nexusAI.getTradingSignals(args || 'BTC/USD');
            break;
            
        case '/analyze':
        case '/analysis':
            await nexusAI.analyzeMarket(args || 'current market conditions');
            break;
            
        case '/help':
            displayHelpMessage();
            break;
            
        case '/clear':
            clearResponseArea();
            break;
            
        case '/status':
            await displayStatus();
            break;
            
        default:
            nexusAI.displayResponse(`Unknown command: ${cmd}. Type /help for available commands.`, 'error');
    }
}

// Handle capability button clicks
async function handleCapability(capability) {
    const userInput = document.getElementById('user-input');
    const inputValue = userInput.value.trim();
    
    console.log('Capability triggered:', capability);
    
    // Show loading state
    displaySystemMessage(`Activating ${capability} capability...`, 'info');

    try {
        let response;
        
        switch(capability) {
            case 'image':
                const imagePrompt = inputValue || 'a stunning futuristic AI interface';
                response = await nexusAI.generateImage(imagePrompt);
                displayUserMessage(`Generate image: ${imagePrompt}`);
                break;
                
            case 'video':
                const videoPrompt = inputValue || 'a cinematic AI visualization';
                response = await nexusAI.generateVideo(videoPrompt);
                displayUserMessage(`Generate video: ${videoPrompt}`);
                break;
                
            case 'music':
                const musicPrompt = inputValue || 'futuristic electronic music';
                response = await nexusAI.generateMusic(musicPrompt);
                displayUserMessage(`Generate music: ${musicPrompt}`);
                break;
                
            case 'website':
                const websiteDesc = inputValue || 'an AI agency landing page';
                response = await nexusAI.generateWebsite(websiteDesc);
                displayUserMessage(`Generate website: ${websiteDesc}`);
                break;
                
            case 'ui':
                const uiDesc = inputValue || 'a modern dashboard interface';
                response = await nexusAI.generateUI(uiDesc);
                displayUserMessage(`Generate UI: ${uiDesc}`);
                break;
                
            case 'code':
                const codeDesc = inputValue || 'a Python function for data analysis';
                response = await nexusAI.generateCode(codeDesc);
                displayUserMessage(`Generate code: ${codeDesc}`);
                break;
                
            case 'trading':
                const symbol = inputValue || 'BTC/USD';
                response = await nexusAI.getTradingSignals(symbol);
                displayUserMessage(`Get trading signals: ${symbol}`);
                break;
                
            case 'signals':
                response = await nexusAI.getTradingSignals('BTC/USD');
                displayUserMessage('Get market signals');
                break;
                
            case 'analysis':
                const analysisContent = inputValue || 'current market conditions';
                response = await nexusAI.analyzeMarket(analysisContent);
                displayUserMessage(`Analyze: ${analysisContent}`);
                break;
                
            default:
                response = { status: 'error', response: `Capability "${capability}" not implemented yet` };
        }

        // Display response
        if (response.status === 'success') {
            nexusAI.displayResponse(response.response, 'ai');
            
            if (response.artifact) {
                nexusAI.displayArtifact(response.artifact);
            }
        } else {
            nexusAI.displayResponse(response.response || 'Operation failed', 'error');
        }

        // Clear input after successful capability execution
        userInput.value = '';
        
    } catch (error) {
        console.error('Capability error:', error);
        nexusAI.displayResponse(`Failed to execute ${capability}: ${error.message}`, 'error');
    }
}

// Display user message
function displayUserMessage(message) {
    const responseArea = document.getElementById('response-area');
    if (!responseArea) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message message-item';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${escapeHtml(message)}</div>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
    `;
    
    responseArea.appendChild(messageDiv);
    responseArea.scrollTo({
        top: responseArea.scrollHeight,
        behavior: 'smooth'
    });
}

// Display system message
function displaySystemMessage(message, type = 'info') {
    const responseArea = document.getElementById('response-area');
    if (!responseArea) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `system-message message-item system-${type}`;
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">ℹ️ ${escapeHtml(message)}</div>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
    `;
    
    responseArea.appendChild(messageDiv);
    responseArea.scrollTo({
        top: responseArea.scrollHeight,
        behavior: 'smooth'
    });
}

// Display help message
function displayHelpMessage() {
    const helpText = `
<strong>NexusAI Commands:</strong><br><br>
<strong>Generation:</strong><br>
/image [prompt] - Generate an image<br>
/video [prompt] - Generate a video<br>
/music [prompt] - Generate music<br>
/website [description] - Generate a website<br>
/ui [description] - Generate UI design<br>
/code [language] [description] - Generate code<br><br>
<strong>Trading:</strong><br>
/trading [symbol] - Get trading signals<br>
/analyze [content] - Analyze content<br><br>
<strong>Utility:</strong><br>
/help - Show this help message<br>
/clear - Clear response area<br>
/status - Show system status<br><br>
<strong>Tips:</strong><br>
- Press Enter to send<br>
- Shift+Enter for new line<br>
- Click capability buttons for quick access
    `;
    
    nexusAI.displayResponse(helpText, 'ai');
}

// Clear response area
function clearResponseArea() {
    const responseArea = document.getElementById('response-area');
    if (responseArea) {
        responseArea.innerHTML = '';
        displaySystemMessage('Response area cleared', 'info');
    }
}

// Display system status
async function displayStatus() {
    const isConnected = await nexusAI.testConnection();
    const wsStatus = nexusAI.connected ? 'Connected' : 'Disconnected';
    
    const statusText = `
<strong>System Status:</strong><br>
HTTP Connection: ${isConnected ? '✅ Online' : '❌ Offline'}<br>
WebSocket: ${wsStatus}<br>
API URL: ${nexusAI.apiUrl}<br>
Reconnect Attempts: ${nexusAI.reconnectAttempts}/${nexusAI.maxReconnectAttempts}
    `;
    
    nexusAI.displayResponse(statusText, 'ai');
}

// Handle visual updates
function handleVisualUpdate(update) {
    console.log('Visual update:', update);
    
    // Apply visual effects based on update type
    if (update.type === 'glow') {
        applyGlowEffect(update.color, update.intensity);
    } else if (update.type === 'shake') {
        applyShakeEffect();
    } else if (update.type === 'pulse') {
        applyPulseEffect();
    }
}

// Apply glow effect
function applyGlowEffect(color = '#00ffff', intensity = 1) {
    const interface = document.querySelector('.nexusai-interface');
    if (interface) {
        interface.style.filter = `drop-shadow(0 0 ${20 * intensity}px ${color})`;
        setTimeout(() => {
            interface.style.filter = '';
        }, 1000);
    }
}

// Apply shake effect
function applyShakeEffect() {
    const interface = document.querySelector('.nexusai-interface');
    if (interface) {
        interface.classList.add('shake');
        setTimeout(() => {
            interface.classList.remove('shake');
        }, 500);
    }
}

// Apply pulse effect
function applyPulseEffect() {
    const interface = document.querySelector('.nexusai-interface');
    if (interface) {
        interface.classList.add('pulse');
        setTimeout(() => {
            interface.classList.remove('pulse');
        }, 1000);
    }
}

// Load capabilities from backend
async function loadCapabilities() {
    try {
        const capabilities = await nexusAI.getCapabilities();
        console.log('Available capabilities:', capabilities);
        
        // Could dynamically generate capability buttons here
        // For now, they're hardcoded in HTML
    } catch (error) {
        console.error('Failed to load capabilities:', error);
    }
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Utility: Format timestamp
function formatTimestamp(date = new Date()) {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleSendMessage,
        handleCapability,
        displayUserMessage,
        displaySystemMessage
    };
}

