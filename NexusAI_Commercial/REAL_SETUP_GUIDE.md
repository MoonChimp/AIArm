# 🎯 NexusAI REAL Setup Guide - Using YOUR Existing Tools

## ✅ What You Already Have

### Ollama Models (27 models!)
- `nexusai-tools:latest` (4.7 GB) - Your latest tool model
- `nexusai-a0-coder1.0:latest` (4.7 GB) - Coding specialist
- `nexusai-visual-agent:latest` (4.7 GB) - Visual tasks
- `nexusai-agent-enhanced:latest` (4.7 GB) - Enhanced capabilities
- `nexusai-music-agent:latest` (2.0 GB) - Music generation
- `codellama:instruct` (3.8 GB) - Code generation
- `llama3:latest` (4.7 GB) - General purpose
- `llama3.2:latest` (2.0 GB) - Lighter version
- `llava:34b` (20 GB) - Vision model
- `qwen2.5-coder:latest` (4.7 GB) - Advanced coding
- And 17 more models!

### Stable Diffusion WebUI
- **Location:** `D:\AIArm\stable-diffusion-webui-master`
- **SDXL Support:** ✅ YES! (stable-diffusion-xl-base-1.0)
- **API Port:** 7860
- **Start with:** `webui-user.bat` or `webui.bat`

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Ollama (if not running)
```bash
ollama serve
```
*Keep this terminal open*

### Step 2: Start Stable Diffusion WebUI (Optional - for image generation)
```bash
cd D:\AIArm\stable-diffusion-webui-master
webui-user.bat --api
```
*The --api flag enables API access*

### Step 3: Start NexusAI Backend
```bash
cd D:\AIArm\NexusAI_Commercial
START_NEXUS_FUNCTIONAL.bat
```

---

## 🎨 Your Available Agents

### 1. Chat Agents (Ollama)
**Default Model:** `nexusai-tools:latest`

**Available Models:**
- `nexusai-tools:latest` - Latest general purpose
- `nexusai-a0-coder1.0:latest` - Coding tasks
- `nexusai-visual-agent:latest` - Visual understanding
- `nexusai-agent-enhanced:latest` - Enhanced responses
- `llama3:latest` - Fallback option

### 2. Cinema Agent (Image Generation)
**Two Options:**

**Option A: SDXL via Python (Direct)**
- Uses: `stabilityai/stable-diffusion-xl-base-1.0`
- Requires: PyTorch, diffusers library
- Quality: Professional cinema-grade (1024x1024)

**Option B: Stable Diffusion WebUI (Recommended)**
- Uses: Your existing SD WebUI at port 7860
- Access: http://localhost:7860
- Has all your installed models
- More flexible and powerful

### 3. Music Agent
- Model: `nexusai-music-agent:latest` (2.0 GB)
- Also: `llamusic/llamusic:3b`

---

## ⚙️ Configuration Files

### Backend Model Configuration
**File:** `D:\AIArm\NexusAI_Commercial\backend\nexus_functional_api.py`

**Current Default:**
```python
DEFAULT_MODEL = "llama2"  # ❌ You don't need this!
```

**Should Be:**
```python
DEFAULT_MODEL = "nexusai-tools:latest"  # ✅ Your latest model
```

### Frontend JavaScript
**File:** `D:\AIArm\NexusAI_Commercial\assets\js\chatting.js`

**Line 59:**
```javascript
model: 'llama2'  // ❌ Change this
```

**Should Be:**
```javascript
model: 'nexusai-tools:latest'  // ✅ Your model
```

---

## 🔧 Verifying Your Setup

### Check Ollama
```bash
ollama list
```
Should show all 27 models ✅

### Check Ollama Running
```bash
curl http://localhost:11434/api/tags
```
Should return JSON with model list ✅

### Check SD WebUI (if started)
```bash
curl http://localhost:7860
```
Should return HTML ✅

### Check NexusAI Backend
```bash
curl http://localhost:5000/api/status
```
Should return system status ✅

---

## 🎯 Testing Each Agent

### Test Chat Agent
1. Open: `D:\AIArm\NexusAI_Commercial\html\chat.html`
2. Type: "Hello, introduce yourself"
3. Should get response from `nexusai-tools`

### Test Image Generation (if SD WebUI running)
1. In chat: "generate image of a sunset"
2. Should create image via Cinema Agent

### Test Music Agent (if installed)
1. Use Ollama directly: `ollama run nexusai-music-agent:latest "Create a piano melody"`

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│              User Interface                      │
│         (html/chat.html)                        │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│         NexusAI Backend API                      │
│      (nexus_functional_api.py)                   │
│         Port: 5000                               │
└──┬────────────┬────────────┬────────────────────┘
   │            │            │
   ↓            ↓            ↓
┌──────┐   ┌────────┐   ┌──────────────────┐
│Ollama│   │Cinema  │   │Stable Diffusion  │
│ 27   │   │Agent   │   │WebUI (Optional)  │
│Models│   │(SDXL)  │   │Port: 7860        │
└──────┘   └────────┘   └──────────────────┘
```

---

## 🔍 Troubleshooting

### "Backend not available"
- **Fix:** Run `START_NEXUS_FUNCTIONAL.bat`

### "Ollama not running"  
- **Fix:** Run `ollama serve` in terminal

### "Model not found"
- **Check:** `ollama list` - Verify model name matches exactly
- **Your models use `-` not `_` (e.g., `nexusai-tools` not `nexusai_tools`)

### Image generation not working
- **Option 1:** Start SD WebUI with `--api` flag
- **Option 2:** Install Python SDXL dependencies
- **Check:** Cinema Agent logs for specific error

---

## 🎬 Cinema Agent Setup Options

### Option 1: Use Your SD WebUI (Recommended)
```bash
cd D:\AIArm\stable-diffusion-webui-master
webui-user.bat --api --listen
```

### Option 2: Install Python SDXL (If not working)
```bash
pip install diffusers transformers accelerate torch torchvision
```

---

## 📝 Next Steps

1. ✅ Logo borders fixed (transparent)
2. ✅ Models verified (27 available)
3. ⏳ Update backend to use `nexusai-tools:latest`
4. ⏳ Update frontend JavaScript
5. ⏳ Test complete workflow

**Ready to update the configuration files?**
