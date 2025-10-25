/**
 * NexusAI FUNCTIONAL Chat Integration
 * Connects to real Ollama backend + Cinema Agent
 */

const API_BASE = 'http://localhost:5000/api';

// State
let currentPersonality = 'balanced';
let currentHonesty = 90;
let currentModel = 'llama2';
let bondLevel = 0;
let interactions = 0;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('[NexusAI] Initializing functional system...');
    
    // Check system status
    checkSystemStatus();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load personality controls if they exist
    setupPersonalityControls();
});

/**
 * Check if backend is running
 */
async function checkSystemStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        console.log('[NexusAI] System Status:', data);
        
        // Display status in UI
        displaySystemStatus(data);
        
        return data.status === 'online';
    } catch (error) {
        console.error('[NexusAI] Backend not available:', error);
        displayError('Backend server not running. Please start with START_NEXUS_COMMERCIAL.bat');
        return false;
    }
}

/**
 * Display system status
 */
function displaySystemStatus(status) {
    const statusDiv = document.getElementById('system-status');
    if (!statusDiv) return;
    
    const ollama = status.systems?.ollama;
    const cinema = status.systems?.cinema;
    const personality = status.systems?.personality;
    
    let html = '<div class="status-panel">';
    html += '<h4>System Status</h4>';
    
    // Ollama
    html += `<div class="status-item ${ollama?.available ? 'active' : 'inactive'}">`;
    html += `<span class="status-icon">${ollama?.available ? '✓' : '✗'}</span>`;
    html += `<span>Ollama: ${ollama?.available ? 'Online' : 'Offline'}</span>`;
    if (ollama?.models) {
        html += `<div class="models">${ollama.models.join(', ')}</div>`;
    }
    html += '</div>';
    
    // Cinema
    html += `<div class="status-item ${cinema?.active ? 'active' : 'inactive'}">`;
    html += `<span class="status-icon">${cinema?.active ? '✓' : '⚠'}</span>`;
    html += `<span>Cinema Agent: ${cinema?.active ? 'Active' : 'Limited'}</span>`;
    html += '</div>';
    
    // Personality
    if (personality?.status) {
        bondLevel = personality.status.bond_level || 0;
        interactions = personality.status.interactions || 0;
        html += `<div class="status-item active">`;
        html += `<span class="status-icon">❤️</span>`;
        html += `<span>Bond Level: ${bondLevel}/100</span>`;
        html += '</div>';
    }
    
    html += '</div>';
    statusDiv.innerHTML = html;
}

/**
 * Send message to Ollama
 */
async function sendMessage(message) {
    try {
        // Show loading
        showLoading();
        
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                personality_mode: currentPersonality,
                honesty: currentHonesty,
                model: currentModel
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Update bond level
            if (data.personality) {
                bondLevel = data.personality.bond_level;
                interactions = data.personality.interactions;
                updateBondDisplay();
            }
            
            return {
                success: true,
                response: data.response,
                model: data.model
            };
        } else {
            return {
                success: false,
                error: data.error || 'Unknown error'
            };
        }
    } catch (error) {
        console.error('[NexusAI] Chat error:', error);
        return {
            success: false,
            error: error.message
        };
    } finally {
        hideLoading();
    }
}

/**
 * Generate image with Cinema Agent
 */
async function generateImage(prompt, aspectRatio = '16:9', filmLook = 'cinematic') {
    try {
        showLoading('Generating cinema-quality image...');
        
        const response = await fetch(`${API_BASE}/cinema/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                aspect_ratio: aspectRatio,
                film_look: filmLook
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            return {
                success: true,
                imagePath: data.image_path,
                prompt: data.prompt
            };
        } else {
            return {
                success: false,
                error: data.message || data.error
            };
        }
    } catch (error) {
        console.error('[NexusAI] Image generation error:', error);
        return {
            success: false,
            error: error.message
        };
    } finally {
        hideLoading();
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Chat form
    const chatForm = document.querySelector('.msger-inputarea');
    const chatInput = document.querySelector('.msger-input');
    
    if (chatForm && chatInput) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const message = chatInput.value.trim();
            if (!message) return;
            
            // Add user message to chat
            appendMessage('user', message);
            chatInput.value = '';
            
            // Check if it's an image request
            if (message.toLowerCase().includes('generate image') || 
                message.toLowerCase().includes('create image')) {
                // Extract prompt
                const prompt = message.replace(/generate image|create image/gi, '').trim();
                handleImageRequest(prompt);
            } else {
                // Regular chat
                const result = await sendMessage(message);
                
                if (result.success) {
                    appendMessage('bot', result.response);
                } else {
                    appendMessage('error', `Error: ${result.error}`);
                }
            }
        });
    }
}

/**
 * Handle image generation request
 */
async function handleImageRequest(prompt) {
    appendMessage('bot', `Generating cinema-quality image: "${prompt}"...`);
    
    const result = await generateImage(prompt);
    
    if (result.success) {
        // Display the image
        const imagePath = result.imagePath.replace('D:/AIArm/Generated/Cinema/', '');
        const imageUrl = `${API_BASE}/cinema/image/${imagePath}`;
        
        appendMessage('bot', 
            `<img src="${imageUrl}" alt="Generated image" style="max-width: 100%; border-radius: 8px; margin-top: 10px;">
            <p>✓ Generated with Cinema Agent (SDXL)</p>`
        );
    } else {
        appendMessage('error', `Image generation failed: ${result.error}`);
    }
}

/**
 * Setup personality controls
 */
function setupPersonalityControls() {
    // Personality mode selector
    const modeSelector = document.getElementById('personalityMode');
    if (modeSelector) {
        modeSelector.addEventListener('change', async (e) => {
            currentPersonality = e.target.value;
            await setPersonalityMode(currentPersonality);
        });
    }
    
    // Honesty slider
    const honestySlider = document.getElementById('honesty');
    const honestyValue = document.getElementById('honestyValue');
    
    if (honestySlider && honestyValue) {
        honestySlider.addEventListener('input', async (e) => {
            currentHonesty = parseInt(e.target.value);
            honestyValue.textContent = currentHonesty;
            await setHonestyLevel(currentHonesty);
        });
    }
}

/**
 * Set personality mode
 */
async function setPersonalityMode(mode) {
    try {
        const response = await fetch(`${API_BASE}/personality/mode`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mode })
        });
        
        if (response.ok) {
            console.log(`[NexusAI] Personality mode set to: ${mode}`);
        }
    } catch (error) {
        console.error('[NexusAI] Failed to set personality mode:', error);
    }
}

/**
 * Set honesty level
 */
async function setHonestyLevel(level) {
    try {
        const response = await fetch(`${API_BASE}/personality/honesty`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ level })
        });
        
        if (response.ok) {
            console.log(`[NexusAI] Honesty level set to: ${level}%`);
        }
    } catch (error) {
        console.error('[NexusAI] Failed to set honesty level:', error);
    }
}

/**
 * Append message to chat
 */
function appendMessage(type, message) {
    const chatContainer = document.querySelector('.msger-chat');
    if (!chatContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `msg ${type}-msg`;
    
    const time = new Date().toLocaleTimeString();
    
    if (type === 'user') {
        messageDiv.innerHTML = `
            <div class="msg-bubble">
                <div class="msg-info">
                    <div class="msg-info-name">You</div>
                    <div class="msg-info-time">${time}</div>
                </div>
                <div class="msg-text">${message}</div>
            </div>
        `;
    } else if (type === 'bot') {
        messageDiv.innerHTML = `
            <div class="msg-img">🤖</div>
            <div class="msg-bubble">
                <div class="msg-info">
                    <div class="msg-info-name">Nexus AI</div>
                    <div class="msg-info-time">${time}</div>
                </div>
                <div class="msg-text">${message}</div>
            </div>
        `;
    } else if (type === 'error') {
        messageDiv.innerHTML = `
            <div class="msg-bubble error">
                <div class="msg-text">${message}</div>
            </div>
        `;
    }
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // Remove "no-chat" placeholder if exists
    const noChat = chatContainer.closest('.main-chat')?.querySelector('.no-chat');
    if (noChat) {
        noChat.style.display = 'none';
    }
}

/**
 * Update bond level display
 */
function updateBondDisplay() {
    const bondDisplay = document.getElementById('bondLevel');
    if (bondDisplay) {
        bondDisplay.textContent = `${bondLevel}`;
    }
    
    // Update in status panel too
    checkSystemStatus();
}

/**
 * Show loading indicator
 */
function showLoading(message = 'Thinking...') {
    appendMessage('bot', `<em>${message}</em>`);
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    // Remove last message if it's a loading message
    const chatContainer = document.querySelector('.msger-chat');
    if (chatContainer) {
        const lastMsg = chatContainer.lastElementChild;
        if (lastMsg && lastMsg.querySelector('em')) {
            lastMsg.remove();
        }
    }
}

/**
 * Display error
 */
function displayError(message) {
    console.error('[NexusAI]', message);
    appendMessage('error', message);
}

// Export for use in HTML
window.NexusAI = {
    sendMessage,
    generateImage,
    checkSystemStatus,
    setPersonalityMode,
    setHonestyLevel
};

console.log('[NexusAI] Functional chat system loaded!');
