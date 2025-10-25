# NEXUS AI - Quick Reference Card

## 🚀 Start Everything
```batch
D:\AIArm\MASTER_START_NEXUS_AI.bat
```
Then open: **http://localhost:5173**

---

## 🎯 Core URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Main UI** | http://localhost:5173 | React interface |
| **API Server** | http://localhost:5000 | Backend API |
| **Ollama** | http://localhost:11434 | LLM server |
| **Stable Diffusion** | http://localhost:7860 | Image generation |

---

## 💬 Common Commands

### Chat with Nexus
```
"Hello Nexus"
"Create a calculator web app"
"Generate an image of a sunset"
"Compose a peaceful melody"
"Write a story about AI"
```

### Direct Agent Access
Via UI: Select agent from dropdown in chat
Via API:
```javascript
{
  "message": "Your request",
  "agent": "code" // or music, photo, story, video, websearch
}
```

---

## 🔧 Troubleshooting

### Restart Everything
```batch
D:\AIArm\MASTER_START_NEXUS_AI.bat
```

### Check Ollama Models
```batch
ollama list
ollama pull llama3:latest
```

### Frontend Issues
```batch
cd D:\AIArm\NexusUI
npm install
npm run dev
```

### Backend Issues
```batch
cd D:\AIArm
pip install flask flask-cors requests psutil
python nexus_api_server.py
```

---

## 📡 API Endpoints

### Essential
```
GET  /api/status
POST /api/chat
GET  /api/system
GET  /api/agents/status
```

### Consciousness
```
GET  /api/consciousness/status
GET  /api/consciousness/thoughts?limit=10
POST /api/consciousness/inject
GET  /api/consciousness/concepts
```

### Memory
```
GET /api/memory/conversations?limit=20
```

---

## 📁 Important Directories

```
D:\AIArm\
├── Generated\        # AI creations
│   ├── Code\
│   ├── Music\
│   ├── Photos\
│   ├── Stories\
│   └── Videos\
├── Memory\           # System memory
├── NexusUI\          # Frontend
├── NexusCore\        # Backend logic
└── InnerLife\        # Consciousness
```

---

## 🧠 Agent Capabilities

| Agent | Can Create |
|-------|-----------|
| **Code** | Websites, apps, calculators, scripts |
| **Music** | Melodies, songs, compositions |
| **Photo** | Images, artwork, visualizations |
| **Story** | Narratives, tales, creative writing |
| **Video** | Video scripts, titles, concepts |
| **WebSearch** | Internet information, current events |

---

## ⚡ Performance Tips

1. Keep Ollama running continuously
2. Use SSD for Generated\ folder
3. Minimum 16GB RAM recommended
4. GPU for Stable Diffusion

---

## 🆘 Emergency Commands

### Kill All Processes
```batch
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

### Reset Ports
```batch
netstat -ano | findstr :5000
netstat -ano | findstr :5173
```

---

## 📚 Full Documentation
See: `D:\AIArm\COMPLETE_NEXUS_AI_GUIDE.md`

---

**Quick Start:** Run `MASTER_START_NEXUS_AI.bat` → Open http://localhost:5173 → Chat with Nexus! 🚀
