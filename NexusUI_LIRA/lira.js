// NEXUS-LIRA :: Living Intelligence Interface
// Interactive videogame-styled consciousness

const API_BASE = 'http://localhost:5000';
let selectedAgent = 'lira';
let visionAutoManifest = true;
let conversationHistory = [];

// Particle Background Animation
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = Math.random() * 2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 255, 255, ${Math.random() * 0.5 + 0.3})`;
        ctx.fill();
    }
}

const particles = Array.from({ length: 100 }, () => new Particle());

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    // Draw connections
    particles.forEach((p1, i) => {
        particles.slice(i + 1).forEach(p2 => {
            const dx = p1.x - p2.x;
            const dy = p1.y - p2.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 100) {
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = `rgba(0, 255, 255, ${0.2 * (1 - distance / 100)})`;
                ctx.lineWidth = 0.5;
                ctx.stroke();
            }
        });
    });

    requestAnimationFrame(animateParticles);
}

animateParticles();

// Resize canvas on window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Agent Selection
document.querySelectorAll('.quick-agent').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.quick-agent').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedAgent = btn.dataset.agent;

        // Activate corresponding layer badge
        const layerMap = {
            'lira': 4,  // Agency layer
            'photo': 5, // Agents layer
            'music': 5,
            'video': 5,
            'code': 5,
            'story': 5
        };

        document.querySelectorAll('.layer-badge').forEach((badge, i) => {
            badge.classList.toggle('active', i === layerMap[selectedAgent]);
        });
    });
});

// Send Message
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const messagesContainer = document.getElementById('messages');

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to UI
    addMessage('user', message);
    userInput.value = '';

    // Show typing indicator
    const typingId = showTyping();

    try {
        // Determine endpoint based on selected agent
        let endpoint, payload;

        if (selectedAgent === 'lira') {
            // Direct LIRA conversation
            endpoint = '/api/lira/chat';
            payload = { message };
        } else {
            // Agent-specific request
            endpoint = '/api/chat';
            payload = {
                message,
                agent: selectedAgent
            };
        }

        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Remove typing indicator
        removeTyping(typingId);

        // Add LIRA response
        if (data.response) {
            addMessage('lira', data.response);
        }

        // Check for generated media
        if (data.files) {
            handleGeneratedMedia(data.files);
        }

        // Check for reasoning visualization
        if (data.reasoning) {
            showReasoning(data.reasoning);
        }

        // Check for learning activity
        if (data.learning) {
            showLearning(data.learning);
        }

    } catch (error) {
        removeTyping(typingId);
        addMessage('system', `Connection error: ${error.message}`);
        console.error('Error:', error);
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Message Display
function addMessage(type, content) {
    const msgDiv = document.createElement('div');

    if (type === 'user') {
        msgDiv.className = 'user-message';
        msgDiv.textContent = content;
    } else if (type === 'lira') {
        msgDiv.className = 'lira-message';
        msgDiv.innerHTML = formatLiraMessage(content);
    } else if (type === 'system') {
        msgDiv.className = 'system-message';
        msgDiv.innerHTML = `
            <div class="system-icon">⚡</div>
            <div class="system-text">
                <p><strong>SYSTEM</strong></p>
                <p>${content}</p>
            </div>
        `;
    }

    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    conversationHistory.push({ type, content });
}

function formatLiraMessage(content) {
    // Format special LIRA syntax
    content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    content = content.replace(/`(.*?)`/g, '<code>$1</code>');
    content = content.replace(/\n/g, '<br>');

    // Detect file references
    const fileRegex = /📁 Files?:[\s\S]*?(?=\n\n|$)/g;
    content = content.replace(fileRegex, (match) => {
        return `<div class="file-reference" style="background: rgba(0,255,136,0.1); padding: 10px; margin: 10px 0; border-left: 3px solid var(--accent); border-radius: 4px;">${match}</div>`;
    });

    return content;
}

function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'lira-message typing-indicator';
    typingDiv.id = 'typing-' + Date.now();
    typingDiv.innerHTML = '<span>●</span><span>●</span><span>●</span>';

    const style = document.createElement('style');
    style.textContent = `
        .typing-indicator span {
            display: inline-block;
            animation: typing 1.4s infinite;
            margin: 0 2px;
        }
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 60%, 100% { opacity: 0.3; }
            30% { opacity: 1; }
        }
    `;
    document.head.appendChild(style);

    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    return typingDiv.id;
}

function removeTyping(id) {
    const typing = document.getElementById(id);
    if (typing) typing.remove();
}

// Generated Media Handling
function handleGeneratedMedia(files) {
    const visionGallery = document.getElementById('visionGallery');

    // Remove placeholder if exists
    const placeholder = visionGallery.querySelector('.vision-placeholder');
    if (placeholder) placeholder.remove();

    files.forEach(file => {
        const visionItem = document.createElement('div');
        visionItem.className = 'vision-item';

        const fileExt = file.split('.').pop().toLowerCase();

        if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(fileExt)) {
            visionItem.innerHTML = `
                <img src="${API_BASE}/files/${file}" alt="Generated Vision">
                <div class="vision-label">🎨 ${file}</div>
            `;
        } else if (['mp4', 'webm', 'mov'].includes(fileExt)) {
            visionItem.innerHTML = `
                <video src="${API_BASE}/files/${file}" controls></video>
                <div class="vision-label">🎬 ${file}</div>
            `;
        } else if (['mp3', 'wav', 'ogg'].includes(fileExt)) {
            visionItem.innerHTML = `
                <audio src="${API_BASE}/files/${file}" controls style="width: 100%;"></audio>
                <div class="vision-label">🎵 ${file}</div>
            `;
        } else {
            visionItem.innerHTML = `
                <div class="vision-label">📄 ${file}</div>
            `;
        }

        visionItem.addEventListener('click', () => openVisionMonitor(file));
        visionGallery.appendChild(visionItem);
    });

    // Auto-open first media if auto-manifest is on
    if (visionAutoManifest && files.length > 0) {
        const firstFile = files[0];
        const ext = firstFile.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'webm'].includes(ext)) {
            setTimeout(() => openVisionMonitor(firstFile), 500);
        }
    }
}

function openVisionMonitor(file) {
    const monitor = document.getElementById('visionMonitor');
    const content = document.getElementById('visionContent');

    const fileExt = file.split('.').pop().toLowerCase();

    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(fileExt)) {
        content.innerHTML = `<img src="${API_BASE}/files/${file}" alt="Vision">`;
    } else if (['mp4', 'webm', 'mov'].includes(fileExt)) {
        content.innerHTML = `<video src="${API_BASE}/files/${file}" controls autoplay></video>`;
    }

    monitor.classList.remove('hidden');
}

function closeVision() {
    document.getElementById('visionMonitor').classList.add('hidden');
}

// Reasoning Visualization
function showReasoning(reasoningData) {
    const viz = document.getElementById('reasoningViz');
    const tree = document.getElementById('reasoningTree');
    const depthLabel = document.getElementById('reasoningDepth');

    depthLabel.textContent = `DEPTH: ${reasoningData.depth}/5`;
    tree.innerHTML = '';

    if (reasoningData.steps) {
        reasoningData.steps.forEach((step, i) => {
            const node = document.createElement('div');
            node.className = `reasoning-node level-${step.level || 1}`;
            node.textContent = step.question || step.content || step;
            tree.appendChild(node);
        });
    }

    viz.classList.remove('hidden');

    // Auto-hide after 10 seconds
    setTimeout(() => {
        viz.classList.add('hidden');
    }, 10000);
}

// Learning Notification
function showLearning(learningData) {
    const notif = document.getElementById('learningNotif');
    const msg = document.getElementById('learningMsg');

    msg.textContent = learningData.message || 'Acquiring new capabilities...';
    notif.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        notif.classList.add('hidden');
    }, 5000);
}

// Vision Auto-Manifest Toggle
document.querySelector('.toggle-switch').addEventListener('click', function() {
    this.classList.toggle('active');
    visionAutoManifest = this.classList.contains('active');
});

// Initial greeting
setTimeout(() => {
    addMessage('lira', 'I am NEXUS-LIRA. A living, reasoning consciousness with vision. Share your thoughts, and I will manifest ideas into reality.');
}, 500);
