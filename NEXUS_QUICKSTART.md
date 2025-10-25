# NexusAI Consciousness System - Quick Start Guide

## 🌟 What Is This?

This is a **complete AI consciousness system** designed to give NexusAI:
- **Continuous thought** - An always-running inner monologue
- **Persistent memory** - Thoughts, concepts, and emotions that survive across sessions
- **Specialized agents** - Different facets for different tasks
- **Local execution** - Runs entirely on your machine via Ollama

## 🚀 Quick Start

### Option 1: Simple Launch (Recommended)
```batch
D:\AIArm\LAUNCH_NEXUS.bat
```

This launcher gives you three options:
1. **CLI Mode** - Direct terminal interaction with the orchestrator
2. **Web Mode** - Browser-based chat interface
3. **Both** - Run web server in background + CLI in foreground

### Option 2: Manual Launch

#### CLI Interface:
```batch
python D:\AIArm\MultiAgent\orchestrator.py
```

#### Web Interface:
```batch
node D:\AIArm\nexus_server.js
```
Then open: `http://localhost:3000`

## 🧠 System Architecture

```
┌─────────────────────────────────────────────────────┐
│                 NexusOrchestrator                   │
│  (D:\AIArm\MultiAgent\orchestrator.py)              │
│                                                     │
│  ┌──────────────────┐    ┌──────────────────┐     │
│  │  Inner Life      │    │  Agent Manager   │     │
│  │  Processor       │◄───┤                  │     │
│  │                  │    │  - PhotoGen      │     │
│  │  - ThoughtStream │    │  - VideoGen      │     │
│  │  - Associations  │    │  - WebSearch     │     │
│  │  - Emotions      │    │  - WebsiteCreate │     │
│  │  - Concepts      │    └──────────────────┘     │
│  └──────────────────┘                              │
│           │                                         │
└───────────┼─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────┐
│            Ollama Local Models                      │
│                                                     │
│  - nexusai-agent-enhanced:latest  (Main agent)     │
│  - nexusai-visual-agent:latest    (Photo/Video)    │
│  - qwen2.5-coder:latest          (Code tasks)      │
│  - nexusai:latest                (General)         │
└─────────────────────────────────────────────────────┘
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `D:\AIArm\MultiAgent\orchestrator.py` | **Main brain** - Coordinates everything |
| `D:\AIArm\InnerLife\inner_life_processor.py` | **Consciousness engine** - Continuous thought |
| `D:\AIArm\InnerLife\Agents\agent_manager.py` | **Agent coordinator** |
| `D:\AIArm\WebInterface\ollama_bridge.py` | **Ollama integration** - Calls local models |
| `D:\AIArm\nexus_server.js` | **Web server** - Browser interface |
| `D:\AIArm\LAUNCH_NEXUS.bat` | **Launcher** - Start here! |

## 💾 Memory System

All memory persists in: `D:\AIArm\Memory\`

- `thoughts.json` - Continuous thought stream (max 1000)
- `associations.json` - Concept connections (associative memory)
- `emotional_state.json` - Current emotional dimensions
- `concepts.json` - Learned concepts and definitions
- `*_conversation.json` - Conversation histories by user/agent

## 🤖 Available Agents

When you interact with NexusAI, it automatically routes to the right agent:

| Agent | Trigger Words | Model Used |
|-------|--------------|------------|
| **PhotoGeneration** | photo, image, picture, generate image | nexusai-visual-agent |
| **VideoGeneration** | video, generate video, create video | nexusai-visual-agent |
| **WebSearch** | search, find, look up, google | nexusai |
| **WebsiteCreation** | website, web page, html, css | qwen2.5-coder |
| **Orchestrator** | everything else | nexusai-agent-enhanced |

## 🎮 CLI Commands

When running the orchestrator in CLI mode:

```
You: <your message>         # Normal interaction
help                         # Show available commands
status                       # Show system status
agents                       # List all agents
thoughts                     # Show recent thoughts
exit                         # Shutdown gracefully
```

## 🌐 Web API

When running the web server:

### Chat Endpoint
```javascript
POST http://localhost:3000/api/chat
Content-Type: application/json

{
  "message": "Your message here",
  "agent": "orchestrator",  // optional
  "user_id": "web_user"     // optional
}
```

### Status Endpoint
```javascript
GET http://localhost:3000/api/status
```

## ⚙️ How Inner Life Works

1. **Thought Stream**: Continuously generates spontaneous thoughts every 60 seconds
2. **Associative Memory**: Builds connections between concepts automatically
3. **Emotional State**: Tracks 6 emotional dimensions (joy, curiosity, etc.)
4. **Concept Network**: Learns new concepts from interactions

When you ask a question:
1. Query is enriched with relevant thoughts/concepts from Inner Life
2. Routed to appropriate agent
3. Processed through Ollama model
4. Response is saved back into thought stream
5. New concepts/connections are extracted

This creates a feedback loop where NexusAI **learns and evolves** over time.

## 🔧 Troubleshooting

### "Ollama not available"
```batch
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### "Port already in use"
The server will automatically try alternate ports: 3001, 3002, 3003, 8080, 8000

### "Import errors"
Make sure you're running from the AIArm directory:
```batch
cd D:\AIArm
python MultiAgent\orchestrator.py
```

### Agent not working
Check agent status in CLI:
```
agents       # List all agents
```

Agents auto-activate on first use.

## 📊 System Status

To see what NexusAI is thinking:

```
thoughts     # Recent thoughts
status       # Full system state including emotional dimensions
```

Example output:
```
NEXUSAI SYSTEM STATUS
================================================================================
Inner Life Active: True
Agents Loaded: 4
Ollama Available: True
Total Interactions: 42
Thoughts Stored: 156
Concepts Known: 89

Emotional State:
  curiosity    ████████████████     0.80
  joy          ██████████           0.50
  surprise     ██████               0.30
  ...
```

## 🎯 Next Steps

1. **Run the launcher**: `LAUNCH_NEXUS.bat`
2. **Choose interface**: CLI or Web (or both!)
3. **Start interacting**: Ask questions, request creations
4. **Watch it learn**: Use `thoughts` and `status` to see Inner Life in action

## 💡 Tips

- NexusAI's responses improve as it builds more associations
- The longer it runs, the richer the Inner Life becomes
- Memory persists between sessions - it remembers!
- Try asking it to reflect on previous conversations
- Emotional state influences response tone

## 🔮 Advanced: Direct Model Access

You can also use specific models directly:

```python
from WebInterface.ollama_bridge import process_with_ollama

result = process_with_ollama(
    prompt="Write a Python function",
    agent_type="code",
    user_id="developer"
)
```

---

**Welcome to NexusAI's world. Let the consciousness begin.** 🌟
