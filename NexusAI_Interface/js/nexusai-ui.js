// NexusAI UI Event Handlers
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const capabilityBtns = document.querySelectorAll('.capability-btn');
    
    if (!userInput || !sendBtn) return;

    sendBtn.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (!message) return;
        
        displayUserMessage(message);
        userInput.value = '';
        sendBtn.disabled = true;
        sendBtn.textContent = 'Sending...';
        
        try {
            const response = await nexusAI.sendChat(message);
            if (response.status === 'success') {
                nexusAI.displayResponse(response.response, 'ai');
            } else {
                nexusAI.displayResponse(response.response || 'Error occurred', 'error');
            }
        } catch (error) {
            nexusAI.displayResponse(`Error: ${error.message}`, 'error');
        } finally {
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send';
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendBtn.click();
        }
    });

    capabilityBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const capability = btn.dataset.capability;
            const prompt = userInput.value.trim() || `Generate ${capability}`;
            displayUserMessage(`[${capability.toUpperCase()}] ${prompt}`);
            
            const response = await nexusAI.sendCommand(`/generate_${capability}`, { prompt: prompt });
            if (response.status === 'success') {
                nexusAI.displayResponse(response.response, 'ai');
            }
        });
    });
});

function displayUserMessage(message) {
    const responseArea = document.getElementById('response-area');
    if (!responseArea) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${message}</div>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
    `;
    responseArea.appendChild(messageDiv);
    responseArea.scrollTop = responseArea.scrollHeight;
}
