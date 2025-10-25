/**
 * NexusAI REAL Chat Integration
 * Replaces dummy bot responses with actual Ollama API calls
 */

const API_BASE = 'http://localhost:5000/api';

// DOM elements
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_IMG = "../assets/images/icons/pro1.png";
const PERSON_IMG = "../assets/images/icons/profile.png";
const BOT_NAME = "NexusAI";
const PERSON_NAME = "You";

// State
let currentPersonality = 'balanced';
let currentHonesty = 90;
let bondLevel = 0;
let currentSessionId = 'default'; // Conversation memory session

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('[NexusAI] Real chat system loaded');
    checkBackendStatus();
});

// Form submission
msgerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const msgText = msgerInput.value.trim();
    if (!msgText) return;

    // Add user message
    appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
    msgerInput.value = "";

    // Hide no-chat placeholder
    const nochat = document.querySelector(".no-chat");
    if (nochat) nochat.classList.add("d-none");

    // Check if image generation request
    if (msgText.toLowerCase().includes('generate image') || 
        msgText.toLowerCase().includes('create image')) {
        await handleImageGeneration(msgText);
    } else {
        // Regular chat with Ollama
        await handleRealChat(msgText);
    }
});

/**
 * Handle real chat with Ollama
 */
async function handleRealChat(message) {
    try {
        // Show typing indicator
        appendMessage(BOT_NAME, BOT_IMG, "left", "<em>Thinking...</em>");

        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                personality_mode: currentPersonality,
                honesty: currentHonesty,
                model: 'nexusai-tools:latest',
                session_id: currentSessionId
            })
        });

        // Remove typing indicator
        const lastMsg = msgerChat.lastElementChild;
        if (lastMsg && lastMsg.querySelector('em')) {
            lastMsg.remove();
        }

        if (response.ok) {
            const data = await response.json();
            
            // Update bond level
            if (data.personality) {
                bondLevel = data.personality.bond_level;
                console.log(`[NexusAI] Bond level: ${bondLevel}/100`);
            }
            
            // Display response
            appendMessage(BOT_NAME, BOT_IMG, "left", data.response);
        } else {
            const error = await response.json();
            appendMessage(BOT_NAME, BOT_IMG, "left", 
                `<span style="color: #dc3545;">Error: ${error.error || 'Failed to get response'}</span><br>
                <small>Make sure Ollama is running: <code>ollama serve</code></small>`
            );
        }
    } catch (error) {
        console.error('[NexusAI] Chat error:', error);
        
        // Remove typing indicator
        const lastMsg = msgerChat.lastElementChild;
        if (lastMsg && lastMsg.querySelector('em')) {
            lastMsg.remove();
        }
        
        appendMessage(BOT_NAME, BOT_IMG, "left", 
            `<span style="color: #dc3545;">Backend not available</span><br>
            <small>Start backend with: <code>START_NEXUS_FUNCTIONAL.bat</code></small>`
        );
    }
}

/**
 * Handle image generation request
 */
async function handleImageGeneration(message) {
    try {
        // Extract prompt
        const prompt = message.replace(/generate image|create image/gi, '').trim();
        
        appendMessage(BOT_NAME, BOT_IMG, "left", 
            `<em>Generating cinema-quality image: "${prompt}"...</em>`
        );

        const response = await fetch(`${API_BASE}/cinema/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                aspect_ratio: '16:9',
                film_look: 'cinematic'
            })
        });

        // Remove generating message
        const lastMsg = msgerChat.lastElementChild;
        if (lastMsg && lastMsg.querySelector('em')) {
            lastMsg.remove();
        }

        if (response.ok) {
            const data = await response.json();
            
            if (data.status === 'success') {
                const imagePath = data.image_path.replace(/\\/g, '/').split('/').pop();
                const imageUrl = `${API_BASE}/cinema/image/${imagePath}`;
                
                appendMessage(BOT_NAME, BOT_IMG, "left", 
                    `✓ Generated with Cinema Agent (SDXL)<br>
                    <img src="${imageUrl}" alt="Generated image" style="max-width: 100%; border-radius: 8px; margin-top: 10px;">
                    <br><small>Prompt: ${data.prompt}</small>`
                );
            } else {
                appendMessage(BOT_NAME, BOT_IMG, "left", 
                    `<span style="color: #dc3545;">Image generation failed</span><br>
                    <small>${data.message || 'Cinema Agent not available'}</small>`
                );
            }
        } else {
            const error = await response.json();
            appendMessage(BOT_NAME, BOT_IMG, "left", 
                `<span style="color: #dc3545;">Cinema Agent not active</span><br>
                <small>${error.message || 'Install dependencies with INSTALL_CINEMA_DEPENDENCIES.bat'}</small>`
            );
        }
    } catch (error) {
        console.error('[NexusAI] Image generation error:', error);
        
        const lastMsg = msgerChat.lastElementChild;
        if (lastMsg && lastMsg.querySelector('em')) {
            lastMsg.remove();
        }
        
        appendMessage(BOT_NAME, BOT_IMG, "left", 
            `<span style="color: #dc3545;">Backend not available</span>`
        );
    }
}

/**
 * Check backend status
 */
async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        console.log('[NexusAI] Backend status:', data);
        
        if (data.systems?.ollama?.available) {
            console.log('[NexusAI] ✓ Ollama connected');
        } else {
            console.warn('[NexusAI] ⚠ Ollama not running');
        }
        
        if (data.systems?.cinema?.active) {
            console.log('[NexusAI] ✓ Cinema Agent active');
        }
        
        return true;
    } catch (error) {
        console.error('[NexusAI] Backend not available:', error);
        return false;
    }
}

/**
 * Append message to chat
 */
function appendMessage(name, img, side, text) {
    const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-bubble">
            <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop = msgerChat.scrollHeight;
}

/**
 * Set personality mode (called from external controls)
 */
window.setPersonalityMode = async function(mode) {
    currentPersonality = mode;
    console.log(`[NexusAI] Personality set to: ${mode}`);
    
    try {
        await fetch(`${API_BASE}/personality/mode`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode })
        });
    } catch (error) {
        console.error('[NexusAI] Failed to set personality:', error);
    }
};

/**
 * Set honesty level (called from external controls)
 */
window.setHonestyLevel = async function(level) {
    currentHonesty = level;
    console.log(`[NexusAI] Honesty set to: ${level}%`);
    
    try {
        await fetch(`${API_BASE}/personality/honesty`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level })
        });
    } catch (error) {
        console.error('[NexusAI] Failed to set honesty:', error);
    }
};

// Utils
function get(selector, root = document) {
    return root.querySelector(selector);
}

console.log('[NexusAI] REAL chat system initialized');
