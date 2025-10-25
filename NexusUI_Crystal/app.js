const API_URL = 'http://localhost:5000/api';

let currentAgent = 'nexus';
let messages = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadAgentButtons();
    setupEventListeners();
    checkAPIStatus();
    addWelcomeMessage();
});

function setupEventListeners() {
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

function loadAgentButtons() {
    const agentButtons = document.querySelectorAll('.agent-btn');

    agentButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            agentButtons.forEach(b => b.classList.remove('active'));

            // Add active to clicked
            btn.classList.add('active');

            // Update current agent
            currentAgent = btn.dataset.agent;

            // Show agent change message
            addSystemMessage(`Switched to ${currentAgent.toUpperCase()} agent`);
        });
    });

    // Set Nexus as default active
    document.querySelector('[data-agent="nexus"]').classList.add('active');
}

async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        if (response.ok) {
            console.log('✅ Nexus API: Online');
        } else {
            addSystemMessage('⚠️ Nexus API connection issue', 'warning');
        }
    } catch (error) {
        addSystemMessage('❌ Nexus API offline. Start the server.', 'error');
    }
}

function addWelcomeMessage() {
    const welcomeText = `
Welcome to Nexus AI - Crystal Interface

I am your advanced AI assistant with specialized capabilities:
• **CODE** - Build complete applications
• **PHOTO** - Generate stunning images
• **MUSIC** - Compose original songs
• **VIDEO** - Create video content
• **STORY** - Write creative narratives
• **SEARCH** - Find information online

Select an agent below or ask me anything!`;

    addMessage('assistant', welcomeText, 'NEXUS');
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (!message) return;

    // Add user message
    addMessage('user', message, 'You');

    // Clear input
    userInput.value = '';

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                agent: currentAgent
            })
        });

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Add assistant response
        addMessage('assistant', data.response, currentAgent.toUpperCase());

        // Show files if any
        if (data.files && data.files.length > 0) {
            addFileMessage(data.files);
        }

    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('assistant', `Error: ${error.message}. Make sure the Nexus API server is running.`, 'ERROR');
    }
}

function addMessage(role, content, label) {
    const messagesContainer = document.getElementById('messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const labelDiv = document.createElement('div');
    labelDiv.className = 'message-label';
    labelDiv.textContent = label;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    messageDiv.appendChild(labelDiv);
    messageDiv.appendChild(contentDiv);

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    messages.push({ role, content, label });
}

function addFileMessage(files) {
    const messagesContainer = document.getElementById('messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';

    const labelDiv = document.createElement('div');
    labelDiv.className = 'message-label';
    labelDiv.textContent = 'FILES GENERATED';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    files.forEach(file => {
        const link = document.createElement('a');
        link.href = '#';
        link.className = 'download-link';
        link.textContent = `📁 ${file}`;
        link.onclick = (e) => {
            e.preventDefault();
            alert(`File saved to: D:/AIArm/Generated/\n${file}`);
        };
        contentDiv.appendChild(link);
        contentDiv.appendChild(document.createElement('br'));
    });

    messageDiv.appendChild(labelDiv);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addSystemMessage(text, type = 'info') {
    const messagesContainer = document.getElementById('messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';

    const labelDiv = document.createElement('div');
    labelDiv.className = 'message-label';
    labelDiv.textContent = 'SYSTEM';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    contentDiv.style.opacity = '0.8';
    contentDiv.style.fontStyle = 'italic';

    messageDiv.appendChild(labelDiv);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'typing-indicator';

    const labelDiv = document.createElement('div');
    labelDiv.className = 'message-label';
    labelDiv.textContent = currentAgent.toUpperCase();

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<span style="opacity: 0.6;">Thinking...</span>';

    messageDiv.appendChild(labelDiv);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// File upload handlers (to be implemented)
document.querySelector('.file-btn').addEventListener('click', () => {
    alert('File upload feature coming soon!');
});

document.querySelector('.media-btn').addEventListener('click', () => {
    alert('Media upload feature coming soon!');
});
