# 🤖 NexusAI Agent Setup Guide

## Quick Start - Get Agents Working in 3 Steps

### Step 1: Install Ollama (AI Brain)
1. Download Ollama from: https://ollama.ai/download
2. Install it (takes 2 minutes)
3. Open a terminal and run:
   ```bash
   ollama serve
   ```
4. Keep this terminal open!

### Step 2: Download AI Model
Open another terminal and run:
```bash
ollama pull llama2
```
This downloads the AI model (takes 5-10 minutes, ~4GB)

### Step 3: Start NexusAI Backend
Double-click: **`START_NEXUS_FUNCTIONAL.bat`**

✅ **Done!** Your agents are now active!

---

## Testing Your Setup

### Open the Chat Interface
1. Navigate to: `D:\AIArm\NexusAI_Commercial\html`
2. Double-click: **`chat.html`**
3. Type a message and press Enter

### Verify Agent Connection
Press F12 in browser, check console. You should see:
```
[NexusAI] ✓ Ollama connected
[NexusAI] Backend status: {...}
```

---

## Available Agents

### 1. **Chat Agent** (Ollama + Personality Matrix)
- Basic conversation
- Personality modes: balanced, professional, creative
- Honesty levels: 0-100%

**Test it:**
```
Type: "Hello, how are you?"
```

### 2. **Cinema Agent** (SDXL Image Generation)
- Creates cinematic-quality images
- Uses Stable Diffusion XL

**Setup Cinema Agent:**
```bash
# Run this once:
INSTALL_CINEMA_DEPENDENCIES.bat
```

**Test it:**
```
Type: "generate image of a sunset over mountains"
```

### 3. **Personality Agent**
- Adaptive responses based on conversation
- Bond level tracking
- Emotional intelligence

**Already active!** Works automatically with Chat Agent.

---

## Troubleshooting

### Problem: "Backend not available"
**Solution:** Start the backend server
```bash
cd D:\AIArm\NexusAI_Commercial
START_NEXUS_FUNCTIONAL.bat
```

### Problem: "Ollama not running"
**Solution:** 
1. Open terminal
2. Run: `ollama serve`
3. Keep terminal open

### Problem: "Model not found"
**Solution:** Download the model
```bash
ollama pull llama2
```

### Problem: CORS errors
**Solution:** Make sure you're opening chat.html as a local file or through a local server, not from a network drive.

---

## File Locations

### Backend Servers (choose one):
- `START_NEXUS_FUNCTIONAL.bat` ← **Recommended**
- `EASY_START.bat`
- `START_NEXUS_COMMERCIAL.bat`

### Chat Interface:
- `html/chat.html` ← Main interface

### Agent Code:
- `backend/nexus_functional_api.py` ← Main backend
- `backend/ollama_connector.py` ← Ollama integration
- `NexusCore/personality/personality_matrix.py` ← Personality
- `NexusCore/cinema/cinema_agent.py` ← Image generation

---

## Advanced Configuration

### Change AI Model
Edit `backend/nexus_functional_api.py`:
```python
DEFAULT_MODEL = 'llama2'  # Change to: mistral, codellama, etc.
```

### Adjust Personality
In chat interface, use browser console:
```javascript
setPersonalityMode('creative')  // or 'balanced', 'professional'
setHonestyLevel(75)  // 0-100
```

### API Endpoints
- Status: `http://localhost:5000/api/status`
- Chat: `http://localhost:5000/api/chat`
- Cinema: `http://localhost:5000/api/cinema/generate`
- Personality: `http://localhost:5000/api/personality/mode`

---

## Need More Help?

1. Check browser console (F12) for errors
2. Check backend terminal for error messages
3. Verify Ollama is running: `ollama list`
4. Test Ollama directly: `ollama run llama2 "Hello"`

---

## Current Status

✅ Logo borders fixed (transparent)
✅ Purple glow removed
⏳ Waiting for agents to be started

**Next:** Run `START_NEXUS_FUNCTIONAL.bat` to activate!
