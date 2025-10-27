# NexusAI + MegaBot Template - Complete Integration Guide

## 🎯 Goal
Integrate the professional MegaBot AI Writer HTML template with your NexusAI backend and display it in UE5 as a stunning holographic interface.

---

## 📋 What You'll Build

A complete AI command center with:
- ✅ Professional UI from MegaBot template
- ✅ Connected to NexusAI backend API
- ✅ All capabilities accessible (Image, Video, Music, Code, Trading, etc.)
- ✅ Real-time artifact display
- ✅ Embedded in UE5 with holographic effects
- ✅ Fully interactive

---

## 🚀 Phase 1: Extract and Setup Template (10 minutes)

### Step 1: Extract Template

```powershell
# Open PowerShell in D:\AIArm
cd D:\AIArm

# Extract the template
Expand-Archive -Path "themeforest-QeXGM1Iz-megabot-ai-writer-copywriting-landing-page-html-template.zip" -DestinationPath "NexusAI_Interface"

# Navigate to extracted folder
cd NexusAI_Interface
```

### Step 2: Locate Main HTML File

Look for the main HTML file (usually `index.html` or `home.html`). This will be your base interface.

### Step 3: Create NexusAI Custom Version

```powershell
# Create a custom version for NexusAI
mkdir NexusAI_Custom
# Copy all files to custom folder
Copy-Item -Path * -Destination NexusAI_Custom -Recurse
cd NexusAI_Custom
```

---

## 🔧 Phase 2: Modify Template for NexusAI (30 minutes)

### Step 1: Add NexusAI API Connection

Create a new file: `nexusai-connector.js`

```javascript
// NexusAI API Connector
// Place this file in the js/ folder of your template

class NexusAIConnector {
    constructor(apiUrl = 'http://127.0.0.1:8001') {
        this.apiUrl = apiUrl;
        this.ws = null;
        this.connected = false;
    }

    // Connect to WebSocket for real-time updates
    connectWebSocket() {
        this.ws = new WebSocket(`ws://127.0.0.1:8001/ws`);
        
        this.ws.onopen = () => {
            console.log('Connected to NexusAI');
            this.connected = true;
            this.updateStatus('Connected', 'success');
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateStatus('Connection Error', 'error');
        };

        this.ws.onclose = () => {
            console.log('Disconnected from NexusAI');
            this.connected = false;
            this.updateStatus('Disconnected', 'warning');
            // Attempt reconnect after 3 seconds
            setTimeout(() => this.connectWebSocket(), 3000);
        };
    }

    // Send chat message
    async sendChat(message, userId = 'user') {
        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: userId
                })
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Chat error:', error);
            return { status: 'error', response: 'Failed to connect to NexusAI' };
        }
    }

    // Send command
    async sendCommand(command, parameters = {}) {
        try {
            const response = await fetch(`${this.apiUrl}/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    parameters: parameters
                })
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Command error:', error);
            return { status: 'error', response: 'Command failed' };
        }
    }

    // Generate image
    async generateImage(prompt) {
        return await this.sendCommand('/generate_image', { prompt: prompt });
    }

    // Generate code
    async generateCode(description, language = 'python') {
        return await this.sendCommand('/generate_code', { 
            description: description, 
            language: language 
        });
    }

    // Analyze content
    async analyzeContent(content, type = 'general') {
        return await this.sendCommand('/analyze', { 
            content: content, 
            type: type 
        });
    }

    // Get available agents
    async getAgents() {
        try {
            const response = await fetch(`${this.apiUrl}/agents`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Failed to get agents:', error);
            return [];
        }
    }

    // Handle incoming WebSocket messages
    handleMessage(data) {
        console.log('Received:', data);
        
        // Update UI based on message type
        if (data.type === 'chat_response') {
            this.displayResponse(data.response);
        } else if (data.type === 'artifact') {
            this.displayArtifact(data);
        } else if (data.type === 'status') {
            this.updateStatus(data.message, data.level);
        }
    }

    // Display response in UI
    displayResponse(response) {
        const responseArea = document.getElementById('response-area');
        if (responseArea) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'ai-response';
            messageDiv.innerHTML = `
                <div class="response-content">
                    <p>${response}</p>
                    <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                </div>
            `;
            responseArea.appendChild(messageDiv);
            responseArea.scrollTop = responseArea.scrollHeight;
        }
    }

    // Display artifact (image, code, etc.)
    displayArtifact(artifact) {
        const artifactArea = document.getElementById('artifact-display');
        if (!artifactArea) return;

        artifactArea.innerHTML = '';

        if (artifact.type === 'image') {
            const img = document.createElement('img');
            img.src = artifact.url;
            img.className = 'artifact-image';
            artifactArea.appendChild(img);
        } else if (artifact.type === 'code') {
            const pre = document.createElement('pre');
            const code = document.createElement('code');
            code.className = `language-${artifact.language}`;
            code.textContent = artifact.content;
            pre.appendChild(code);
            artifactArea.appendChild(pre);
        } else if (artifact.type === 'video') {
            const video = document.createElement('video');
            video.src = artifact.url;
            video.controls = true;
            video.className = 'artifact-video';
            artifactArea.appendChild(video);
        }
    }

    // Update status indicator
    updateStatus(message, level = 'info') {
        const statusElement = document.getElementById('nexus-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status status-${level}`;
        }
    }
}

// Initialize NexusAI connector
const nexusAI = new NexusAIConnector();

// Connect on page load
document.addEventListener('DOMContentLoaded', () => {
    nexusAI.connectWebSocket();
});
```

### Step 2: Modify Main HTML File

Add these elements to your main HTML file (usually `index.html`):

```html
<!-- Add in <head> section -->
<script src="js/nexusai-connector.js"></script>

<!-- Add in <body> section, replace or modify existing chat interface -->
<div class="nexusai-interface">
    <!-- Status Bar -->
    <div class="status-bar">
        <span id="nexus-status" class="status">Connecting...</span>
    </div>

    <!-- Artifact Display Area -->
    <div id="artifact-display" class="artifact-container">
        <div class="artifact-placeholder">
            <p>Generated content will appear here</p>
        </div>
    </div>

    <!-- Response Area -->
    <div id="response-area" class="response-container">
        <!-- AI responses will appear here -->
    </div>

    <!-- Capabilities Arsenal -->
    <div class="capabilities-arsenal">
        <h3>NexusAI Capabilities</h3>
        <div class="capability-buttons">
            <button class="capability-btn" data-capability="image">
                <i class="icon-image"></i> Image
            </button>
            <button class="capability-btn" data-capability="video">
                <i class="icon-video"></i> Video
            </button>
            <button class="capability-btn" data-capability="music">
                <i class="icon-music"></i> Music
            </button>
            <button class="capability-btn" data-capability="website">
                <i class="icon-globe"></i> Website
            </button>
            <button class="capability-btn" data-capability="ui">
                <i class="icon-layout"></i> UI Design
            </button>
            <button class="capability-btn" data-capability="code">
                <i class="icon-code"></i> Code
            </button>
            <button class="capability-btn" data-capability="trading">
                <i class="icon-trending-up"></i> Trading
            </button>
            <button class="capability-btn" data-capability="signals">
                <i class="icon-activity"></i> Signals
            </button>
            <button class="capability-btn" data-capability="analysis">
                <i class="icon-pie-chart"></i> Analysis
            </button>
        </div>
    </div>

    <!-- Input Area -->
    <div class="input-container">
        <input type="text" id="user-input" placeholder="Type your command or question..." />
        <button id="send-btn" class="send-button">Send</button>
    </div>
</div>
```

### Step 3: Add JavaScript Event Handlers

Add this to your main JavaScript file or create `nexusai-ui.js`:

```javascript
// NexusAI UI Event Handlers

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const capabilityBtns = document.querySelectorAll('.capability-btn');

    // Send message on button click
    sendBtn.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Display user message
        displayUserMessage(message);

        // Send to NexusAI
        const response = await nexusAI.sendChat(message);
        
        // Display response
        if (response.status === 'success') {
            nexusAI.displayResponse(response.response);
            
            // If there's an artifact, display it
            if (response.visual_update) {
                // Handle visual updates
            }
        }

        // Clear input
        userInput.value = '';
    });

    // Send on Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });

    // Capability button handlers
    capabilityBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const capability = btn.dataset.capability;
            handleCapability(capability);
        });
    });
});

function displayUserMessage(message) {
    const responseArea = document.getElementById('response-area');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${message}</p>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
    `;
    responseArea.appendChild(messageDiv);
    responseArea.scrollTop = responseArea.scrollHeight;
}

async function handleCapability(capability) {
    const userInput = document.getElementById('user-input');
    
    switch(capability) {
        case 'image':
            const prompt = userInput.value || 'Create an image';
            const imageResponse = await nexusAI.generateImage(prompt);
            nexusAI.displayResponse(`Generating image: ${prompt}`);
            break;
            
        case 'code':
            const codeDesc = userInput.value || 'Write a function';
            const codeResponse = await nexusAI.generateCode(codeDesc);
            nexusAI.displayResponse(`Generating code: ${codeDesc}`);
            break;
            
        case 'analysis':
            const content = userInput.value || 'Analyze this';
            const analysisResponse = await nexusAI.analyzeContent(content);
            nexusAI.displayResponse(`Analyzing: ${content}`);
            break;
            
        default:
            const command = `/generate_${capability}`;
            const params = { prompt: userInput.value };
            const response = await nexusAI.sendCommand(command, params);
            nexusAI.displayResponse(response.response);
    }
}
```

### Step 4: Add Custom CSS

Create `nexusai-custom.css`:

```css
/* NexusAI Custom Styles */

.nexusai-interface {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Inter', sans-serif;
}

/* Status Bar */
.status-bar {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 255, 0.3);
    padding: 10px 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.status {
    color: #00ffff;
    font-weight: 600;
    font-size: 14px;
}

.status-success { color: #00ff00; }
.status-error { color: #ff0000; }
.status-warning { color: #ffaa00; }

/* Artifact Display */
.artifact-container {
    background: rgba(0, 0, 0, 0.5);
    border: 2px solid rgba(0, 255, 255, 0.3);
    border-radius: 12px;
    padding: 20px;
    min-height: 300px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.artifact-placeholder {
    color: rgba(0, 255, 255, 0.5);
    text-align: center;
}

.artifact-image {
    max-width: 100%;
    max-height: 500px;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.artifact-video {
    max-width: 100%;
    border-radius: 8px;
}

/* Response Area */
.response-container {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 12px;
    padding: 20px;
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 20px;
}

.user-message, .ai-response {
    margin-bottom: 15px;
    padding: 12px;
    border-radius: 8px;
    animation: fadeIn 0.3s ease-in;
}

.user-message {
    background: rgba(0, 100, 255, 0.2);
    border-left: 3px solid #0064ff;
}

.ai-response {
    background: rgba(0, 255, 255, 0.1);
    border-left: 3px solid #00ffff;
}

.message-content p {
    margin: 0 0 5px 0;
    color: #ffffff;
    line-height: 1.6;
}

.timestamp {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.5);
}

/* Capabilities Arsenal */
.capabilities-arsenal {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(0, 255, 255, 0.3);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.capabilities-arsenal h3 {
    color: #00ffff;
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.capability-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 10px;
}

.capability-btn {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 255, 0.3);
    color: #00ffff;
    padding: 12px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.capability-btn:hover {
    background: rgba(0, 255, 255, 0.2);
    border-color: #00ffff;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    transform: translateY(-2px);
}

.capability-btn:active {
    transform: translateY(0);
}

/* Input Container */
.input-container {
    display: flex;
    gap: 10px;
    background: rgba(0, 0, 0, 0.5);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(0, 255, 255, 0.3);
}

#user-input {
    flex: 1;
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(0, 255, 255, 0.3);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 16px;
    outline: none;
    transition: all 0.3s ease;
}

#user-input:focus {
    border-color: #00ffff;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
}

#user-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
}

.send-button {
    background: linear-gradient(135deg, #00ffff, #0088ff);
    border: none;
    color: #000;
    padding: 12px 30px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.send-button:hover {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    transform: scale(1.05);
}

.send-button:active {
    transform: scale(0.98);
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Scrollbar Styling */
.response-container::-webkit-scrollbar {
    width: 8px;
}

.response-container::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
}

.response-container::-webkit-scrollbar-thumb {
    background: rgba(0, 255, 255, 0.3);
    border-radius: 4px;
}

.response-container::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 255, 255, 0.5);
}
```

Add this CSS file to your HTML:
```html
<link rel="stylesheet" href="css/nexusai-custom.css">
```

---

## 🎮 Phase 3: Test the Modified Template (10 minutes)

### Step 1: Start NexusAI Backend

```powershell
cd D:\AIArm
python NEXUS_ULTIMATE_INTERFACE.py
```

### Step 2: Open Template in Browser

```powershell
# Navigate to your custom template folder
cd D:\AIArm\NexusAI_Interface\NexusAI_Custom

# Open in default browser
start index.html
```

### Step 3: Test Features

1. **Status** - Should show "Connected" in cyan
2. **Type a message** - "Hello NexusAI"
3. **Click Send** - Response should appear
4. **Click capability buttons** - Should trigger commands
5. **Check console** - F12 → Console tab for any errors

---

## 🎨 Phase 4: Integrate with UE5 (30 minutes)

### Step 1: Enable Web Browser Plugin in UE5

1. Open your NexusAI project in UE5
2. **Edit → Plugins**
3. Search for **"Web Browser"**
4. **Enable** the plugin
5. **Restart UE5**

### Step 2: Create Web Browser Widget

1. In Content Browser, **Right-click → User Interface → Widget Blueprint**
2. Name it: `NexusAI_WebInterface`
3. **Open** the widget

### Step 3: Add Web Browser Component

1. In **Designer** view
2. From **Palette**, find **"Web Browser"** (under Special)
3. **Drag** it onto the canvas
4. **Anchor** it to fill the screen (bottom-right anchor preset)
5. Set **Size** to fill entire canvas

### Step 4: Configure Web Browser

1. **Select** the Web Browser component
2. In **Details** panel:
   - **Initial URL:** `file:///D:/AIArm/NexusAI_Interface/NexusAI_Custom/index.html`
   - **Supports Transparency:** ✅ Check this
   - **Is Variable:** ✅ Check this
3. **Compile** and **Save**

### Step 5: Add to Level Blueprint

1. **Open Level Blueprint**
2. Add nodes:

```
Event BeginPlay
  ↓
Create Widget (NexusAI_WebInterface)
  ↓
Add to Viewport
```

3. **Compile**, **Save**, **Play**

---

## 🌟 Phase 5: Add Holographic Effects in UE5 (20 minutes)

### Step 1: Create Post Process Volume

1. In **Place Actors** panel, search for **"Post Process Volume"**
2. **Drag** it into your level
3. In **Details** panel:
   - **Infinite Extent (Unbound):** ✅ Check this

### Step 2: Configure Bloom (Glow Effect)

1. Select Post Process Volume
2. In Details → **Bloom** section:
   - **Intensity:** `3.0`
   - **Threshold:** `0.5`
   - **Size Scale:** `4.0`

### Step 3: Add Color Grading

1. In Post Process Volume → **Color Grading** section:
   - **Saturation:** Increase cyan channel
   - **Global:** Add slight blue tint
   - **Shadows:** Make darker for contrast

### Step 4: Add Vignette

1. In Post Process Volume → **Vignette** section:
   - **Intensity:** `0.4`

---

## 🎯 Phase 6: Final Polish (20 minutes)

### Step 1: Adjust Widget Transparency

1. Open `NexusAI_WebInterface` widget
2. Select Web Browser component
3. In Details → **Rendering**:
   - **Opacity:** `0.95` (slight transparency)

### Step 2: Add Background

1. Add an **Image** component behind the Web Browser
2. Set color to dark blue with low opacity
3. Add slight blur effect

### Step 3: Test Everything

1. **Press Play** in UE5
2. Verify:
   - Interface loads
   - Can type messages
   - Responses appear
   - Capability buttons work
   - Artifacts display
   - Holographic effects visible

---

## 🚀 You're Done!

You now have:
- ✅ Professional HTML interface
- ✅ Connected to NexusAI backend
- ✅ All capabilities accessible
- ✅ Artifact display system
- ✅ Embedded in UE5
- ✅ Holographic visual effects
- ✅ Production-ready demo

---

## 🐛 Troubleshooting

### Interface Not Loading in UE5:
- Check file path is correct (use forward slashes: `file:///D:/AIArm/...`)
- Ensure Web Browser plugin is enabled
- Check UE5 Output Log for errors

### API Not Connecting:
- Verify NexusAI backend is running
- Check URL is `http://127.0.0.1:8001` (not https)
- Look at browser console (F12) for errors

### Capability Buttons Not Working:
- Check `nexusai-connector.js` is loaded
- Verify API endpoints in backend
- Check browser console for JavaScript errors

### Artifacts Not Displaying:
- Ensure artifact-display div exists
- Check artifact data format from API
- Verify CSS is loaded

---

## 📝 Next Steps

1. **Customize branding** - Change colors, logos, text
2. **Add more capabilities** - Extend the arsenal
3. **Improve artifact display** - Better formatting
4. **Add authentication** - User login system
5. **Deploy** - Package UE5 project for distribution

---

**Congratulations! You have a production-ready AI interface!** 🎉

