/**
 * NexusAI Cinematic Taskbar Chat Interface
 * Provides embedded chat functionality with cinematic visual effects
 */

class CinematicChatInterface {
    constructor() {
        this.API_BASE = 'http://localhost:5000/api';
        this.sessionId = 'cinematic_session_' + Date.now();
        this.isChatOpen = false;
        this.isTyping = false;

        this.initializeElements();
        this.bindEvents();
        this.updateSystemStatus();
    }

    initializeElements() {
        // Get DOM elements
        this.taskbarInput = document.getElementById('taskbarChatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.chatResponse = document.getElementById('chatResponse');
        this.chatMessages = document.getElementById('chatMessages');

        // Create typing indicator
        this.typingIndicator = this.createTypingIndicator();
    }

    bindEvents() {
        // Taskbar input events
        if (this.taskbarInput) {
            this.taskbarInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });

            this.taskbarInput.addEventListener('focus', () => {
                this.openChat();
            });
        }

        // Send button
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => {
                this.sendMessage();
            });
        }

        // Voice button
        if (this.voiceBtn) {
            this.voiceBtn.addEventListener('click', () => {
                this.toggleVoiceInput();
            });
        }

        // Close chat when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isChatOpen && !this.chatResponse.contains(e.target) && !this.taskbarInput.contains(e.target)) {
                // Keep chat open for now
            }
        });
    }

    openChat() {
        if (this.chatResponse && !this.isChatOpen) {
            this.chatResponse.style.display = 'flex';
            this.isChatOpen = true;
            this.taskbarInput.placeholder = 'Ask NexusAI anything...';

            // Add welcome message
            this.addMessage('ai', 'Hello! I\'m NexusAI, your cinematic AI assistant. I can see the visual field around us and help with any task. What would you like to explore?');
        }
    }

    closeChat() {
        if (this.chatResponse) {
            this.chatResponse.style.display = 'none';
            this.isChatOpen = false;
            this.taskbarInput.placeholder = 'Click to chat with NexusAI...';
        }
    }

    async sendMessage() {
        const message = this.taskbarInput.value.trim();
        if (!message || this.isTyping) return;

        // Add user message to chat
        this.addMessage('user', message);
        this.taskbarInput.value = '';

        // Show typing indicator
        this.showTyping();

        try {
            // Send to API
            const response = await fetch(`${this.API_BASE}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    personality_mode: 'balanced',
                    honesty: 90,
                    model: 'nexusai-tools:latest',
                    session_id: this.sessionId
                })
            });

            if (response.ok) {
                const data = await response.json();

                // Hide typing indicator
                this.hideTyping();

                // Add AI response
                this.addMessage('ai', data.response);

                // Update session info if available
                if (data.conversation_summary) {
                    this.updateSessionInfo(data.conversation_summary);
                }
            } else {
                throw new Error('API request failed');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTyping();
            this.addMessage('ai', 'I apologize, but I\'m having trouble connecting to my systems. Please ensure the NexusAI backend is running.');
        }
    }

    addMessage(type, content) {
        if (!this.chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'chat-message-content';
        contentDiv.innerHTML = this.formatMessage(content);

        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

        // Limit messages to prevent overflow
        this.limitMessages();
    }

    formatMessage(content) {
        // Basic formatting for URLs, code, etc.
        return content
            .replace(/\n/g, '<br>')
            .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    }

    createTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.style.display = 'none';
        indicator.innerHTML = `
            <span>NexusAI is thinking</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        if (this.chatMessages) {
            this.chatMessages.appendChild(indicator);
        }

        return indicator;
    }

    showTyping() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'flex';
            this.isTyping = true;
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }

    hideTyping() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'none';
            this.isTyping = false;
        }
    }

    limitMessages(maxMessages = 50) {
        const messages = this.chatMessages.children;
        while (messages.length > maxMessages) {
            messages[0].remove();
        }
    }

    updateSessionInfo(summary) {
        // Update any session info displays
        const sessionElements = document.querySelectorAll('.session-info');
        sessionElements.forEach(el => {
            el.textContent = summary;
        });
    }

    updateSystemStatus() {
        // Update system monitor bars with random but realistic values
        setInterval(() => {
            const fills = document.querySelectorAll('.monitor-fill');
            fills.forEach(fill => {
                const currentWidth = parseInt(fill.style.width) || 30;
                const variation = Math.random() * 40 - 20; // ±20%
                const newWidth = Math.max(10, Math.min(90, currentWidth + variation));
                fill.style.width = `${newWidth}%`;
            });
        }, 3000);
    }

    toggleVoiceInput() {
        // Placeholder for voice input functionality
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.addMessage('ai', 'Voice input feature is coming soon! For now, please type your message.');
        } else {
            this.addMessage('ai', 'Voice input is not supported in this browser. Please type your message.');
        }
    }

    // Public method to add messages from external sources
    addExternalMessage(content) {
        this.addMessage('ai', content);
    }
}

// Initialize cinematic chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cinematicChat = new CinematicChatInterface();

    // Add some initial visual effects
    initializeVisualEffects();
});

function initializeVisualEffects() {
    // Add subtle parallax effect to visual elements
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.hologram-element, .data-stream');

        parallaxElements.forEach((element, index) => {
            const speed = 0.5 + (index * 0.1);
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });

    // Add mouse tracking for interactive elements
    window.addEventListener('mousemove', (e) => {
        const mouseX = (e.clientX / window.innerWidth) * 100;
        const mouseY = (e.clientY / window.innerHeight) * 100;

        // Subtle movement of holographic elements based on mouse
        const holograms = document.querySelectorAll('.hologram-element');
        holograms.forEach((hologram, index) => {
            const moveX = (mouseX - 50) * 0.1 * (index + 1);
            const moveY = (mouseY - 50) * 0.1 * (index + 1);
            hologram.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });
}

// Export for global access
window.CinematicChatInterface = CinematicChatInterface;
