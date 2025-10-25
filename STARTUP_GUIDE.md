# 🚀 Nexus AI - Quick Start Guide

## One-Click Startup

Double-click: **`START_NEXUS.bat`**

This will automatically start all Nexus components:
1. Ollama AI Engine
2. Stable Diffusion WebUI (for image generation)
3. Nexus API Server
4. Crystal Interface UI

After 10 seconds, your browser will open automatically to: **http://localhost:3003**

---

## What Gets Started

### 1. Ollama (AI Brain)
- Provides language models for conversation and intelligence
- Runs automatically in background

### 2. Stable Diffusion WebUI (Image Generation)
- Required for photo generation
- Runs at http://localhost:7860
- Takes 1-2 minutes to fully load

### 3. Nexus API Server (port 5000)
- Orchestrates all agents
- Handles routing and coordination
- Manages conversation history

### 4. Crystal UI (port 3003)
- Beautiful glassmorphism interface
- Access at http://localhost:3003

---

## If Something Goes Wrong

### "Stable Diffusion not found"
Install from: https://github.com/AUTOMATIC1111/stable-diffusion-webui

Or edit `START_NEXUS.bat` to point to your installation location.

### "Port already in use"
Close any existing Nexus instances:
```batch
taskkill /F /IM python.exe
taskkill /F /IM ollama.exe
```

Then run `START_NEXUS.bat` again.

### Services not starting
Make sure you have:
- Python 3.10+ installed
- Ollama installed
- All dependencies: `pip install -r requirements.txt`

---

## Manual Startup (Advanced)

If you prefer to start components individually:

```batch
# Terminal 1 - Ollama
ollama serve

# Terminal 2 - Stable Diffusion
cd C:\stable-diffusion-webui
webui-user.bat

# Terminal 3 - Nexus API
cd D:\AIArm
python nexus_api_server.py

# Terminal 4 - UI
cd D:\AIArm\NexusUI_Crystal
python -m http.server 3003
```

Then open: http://localhost:3003

---

## Stopping Nexus

Just close the terminal windows or press Ctrl+C in each.

Or use:
```batch
taskkill /F /IM python.exe
```

---

## 💬 Using Nexus

### Chat Mode (Default)
Click the "NEXUS" agent button and just talk naturally!

### Specialized Agents
Click any agent button:
- **CODE** - Build applications
- **PHOTO** - Generate images
- **MUSIC** - Create songs
- **VIDEO** - Make videos  
- **STORY** - Write stories
- **SEARCH** - Find information

### Example Requests
- "Create a kitten playing ukulele on a porch"
- "Build a todo list app"
- "Write a song about adventure"
- "Search for latest AI news"

---

## Files

- `START_NEXUS.bat` - One-click launcher
- `nexus_api_server.py` - Backend API
- `NexusUI_Crystal/` - Interface files
- `NexusCore/orchestrator.py` - AI brain

Enjoy using Nexus AI! 🎉
