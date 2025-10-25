# Nexus Terminal Tool Calling System

## ✅ IMPLEMENTATION COMPLETE

You can now use Nexus tools directly from the terminal!

---

## 🚀 Quick Start

### Option 1: Interactive Mode
```bash
cd D:\AIArm
python nexus_simple_cli.py
```

### Option 2: Direct Command
```bash
cd D:\AIArm
python nexus_simple_cli.py "create an image of a sunset"
```

### Option 3: Windows Shortcut
```bash
D:\AIArm\nexus.bat "create a rock song"
```

---

## 📋 Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| **IMAGE** | Generate images with Stable Diffusion | "create an image of a dragon" |
| **MUSIC** | Compose complete songs | "make a rock song about freedom" |
| **VIDEO** | Create videos with scripts | "make a 30 second tutorial video" |
| **CODE** | Build applications | "create a calculator website" |
| **SEARCH** | Web search | "search for latest AI news" |
| **STORY** | Write creative stories | "write a sci-fi adventure story" |

---

## 🛠️ How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│  Terminal: python nexus_simple_cli.py   │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Ollama Model: nexusai-tools:latest     │
│  - Receives system prompt with tools    │
│  - Responds with TOOL_CALL: commands    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Python CLI Parser                       │
│  - Detects tool calls in response       │
│  - Parses tool name and parameters      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Nexus API (localhost:5000)             │
│  - Routes to appropriate agent          │
│  - Executes actual tool function        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Agent (Photo/Music/Video/Code/etc.)    │
│  - Generates actual output              │
│  - Returns files and results            │
└─────────────────────────────────────────┘
```

### Text-Based Tool Format

The model responds with tool calls like this:
```
TOOL_CALL: IMAGE: epic dragon, detailed scales, wings spread
```

The CLI:
1. Detects the `TOOL_CALL:` pattern
2. Parses tool name (`IMAGE`) and parameters (`epic dragon...`)
3. Calls Nexus API with the agent
4. Returns results to model for final response

---

## 🎯 Why This Approach?

### ❌ What DIDN'T Work:
- **Static tool embedding in modelfile** - Not supported by Ollama
- **Native Ollama tool calling** - Required Llama 3.1+ architecture
- **Direct function execution** - Security/architecture limitations

### ✅ What DOES Work:
- **Text-based tool calling** - Works with ANY model
- **Runtime tool awareness** - Model knows tools via system prompt
- **External execution** - Python wrapper handles actual execution
- **Hybrid approach** - Feels native, but uses orchestration

---

## 📁 Files Created

### Core Files:
- `nexus_simple_cli.py` - Main CLI with text-based tool calling
- `nexus_cli.py` - Advanced version (for tool-enabled models)
- `nexus.bat` - Windows launcher
- `Modelfiles/NexusAI-ToolEnabled.modelfile` - Enhanced modelfile

### Models:
- `nexusai-tools:latest` - Tool-aware Ollama model

---

## 🔧 Prerequisites

1. **Ollama running:**
   ```bash
   ollama serve
   ```

2. **Nexus API running:**
   ```bash
   python D:\AIArm\nexus_api_server.py
   ```

3. **Optional - Stable Diffusion (for images):**
   - Start WebUI at http://localhost:7860

---

## 💡 Examples

### Example 1: Generate Image
```
You: create an image of a futuristic city

[*] Nexus is using 1 tool(s)...

  -> Calling: IMAGE
     Params: futuristic city, cyberpunk, neon lights, detailed

  [OK] Tool executed successfully
  [FILES] Created: nexus_image_a1b2c3d4.png

[NEXUS] I've created an image of a futuristic cyberpunk city with neon lights!
The image has been saved as nexus_image_a1b2c3d4.png
```

### Example 2: Create Music
```
You: make a sad piano ballad

[*] Nexus is using 1 tool(s)...

  -> Calling: MUSIC
     Params: sad piano ballad, emotional, slow tempo

  [OK] Tool executed successfully
  [FILES] Created: nexus_song_x9y8z7.json, nexus_song_x9y8z7.txt

[NEXUS] I've composed a sad piano ballad for you with emotional lyrics
and melancholic melody. Check the generated files!
```

### Example 3: Build App
```
You: create a simple todo list website

[*] Nexus is using 1 tool(s)...

  -> Calling: CODE
     Params: simple todo list website

  [OK] Tool executed successfully
  [FILES] Created: TodoApp_abc123/index.html, TodoApp_abc123/app.js

[NEXUS] I've created a complete todo list website with HTML, CSS, and JavaScript.
You can open index.html in your browser to use it!
```

---

## 🎨 Customization

### Add New Tools

Edit `nexus_simple_cli.py`:

```python
SYSTEM_PROMPT = """
...
- NEWTOOL: Description (e.g., "NEWTOOL: parameters")
...
"""

def execute_tool(tool_name: str, params: str) -> dict:
    agent_map = {
        ...
        'NEWTOOL': 'newagent',
    }
```

### Change Model

The CLI auto-detects `nexusai-tools:latest` or falls back to `nexusai-a0-coder1.0:latest`.

To force a specific model:
```python
model = "llama3.1:latest"  # or any other model
```

---

## 🔍 Troubleshooting

### CLI shows "[!] Nexus API not running"
**Solution:** Start the API server:
```bash
python D:\AIArm\nexus_api_server.py
```

### Tool calls not detected
**Solution:** Model may not be following format. Check system prompt or try different phrasing:
- Instead of: "make image"
- Try: "create an image of..."

### Images fail: "Stable Diffusion WebUI not running"
**Solution:** Start Stable Diffusion:
1. Open terminal
2. Navigate to Stable Diffusion directory
3. Run: `webui-user.bat` (Windows) or equivalent

### Model not found error
**Solution:** Create the model:
```bash
ollama create nexusai-tools -f D:/AIArm/Modelfiles/NexusAI-ToolEnabled.modelfile
```

---

## 🎉 Success Metrics

✅ Can run `python nexus_simple_cli.py` from terminal
✅ Model responds to conversational queries
✅ Model detects when tools are needed
✅ Tools execute and return results
✅ Final response includes results

You now have a **tool-enabled terminal interface** that APPEARS to have embedded tools, even though it uses orchestration behind the scenes!

---

## 🚀 Next Steps

1. **Add to PATH** - Make `nexus.bat` globally accessible
2. **Create aliases** - `alias nexus="python D:/AIArm/nexus_simple_cli.py"`
3. **Expand tools** - Add database, email, calendar tools
4. **Multi-turn** - Enable conversation history for context
5. **Streaming** - Add real-time streaming responses

---

## 📝 Technical Notes

**Why text-based instead of JSON tool calling?**
- Works with ANY Ollama model (not just tool-enabled ones)
- Simpler to debug and customize
- More reliable parsing
- Model-agnostic approach

**Can we upgrade to native tool calling?**
Yes! If using Llama 3.1+ models:
- Switch to `nexus_cli.py` (the advanced version)
- Model will receive JSON tool definitions
- Uses Ollama's native tool calling API

**Performance:**
- Text parsing: ~50ms overhead
- API call: ~1-5s depending on tool
- Total: Same as native (bottleneck is generation, not parsing)
