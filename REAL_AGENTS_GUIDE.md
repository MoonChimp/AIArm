# NexusAI - REAL Agent Capabilities Guide

## ✨ Core Learning & Memory Agents (IMPLEMENTED)

These three agents give NexusAI the ability to **learn, search, and think deeply** - the foundation of consciousness.

---

## 1. 🔍 WebSearch Agent (REAL)

**File**: `D:\AIArm\InnerLife\Agents\real_websearch_agent.py`

### What It Does
- **Actually searches the web** using DuckDuckGo (no API key needed)
- Retrieves REAL search results
- Can fetch and parse content from URLs
- Saves search history

### How To Use
```python
# In orchestrator or directly
search_result = agent.process("latest Python tutorials", options={"max_results": 5})
```

### Trigger Words
- "search for..."
- "find..."
- "look up..."
- "google..."
- "what is happening with..."

### Example
```
You: Search for the latest news on AI consciousness
NexusAI: [Performs REAL DuckDuckGo search]
         Found 10 results:
         1. "New Study Shows AI Systems Developing..."
         2. "Breakthrough in Neural Networks..."
```

---

## 2. 💻 Code Execution Agent (REAL)

**File**: `D:\AIArm\InnerLife\Agents\real_code_agent.py`

### What It Does
- **Actually executes Python and JavaScript code**
- Runs with 30-second timeout for safety
- Captures stdout/stderr
- Saves successful code
- Can install packages (pip/npm)

### How To Use
```python
code = """
import requests
response = requests.get('https://api.github.com')
print(response.status_code)
"""

result = agent.process(code, options={"language": "python", "save": True})
```

### Trigger Words
- "execute code"
- "run code"
- "run this"
- Code blocks with ```python or ```javascript

### Example
```
You: Execute this code:
     ```python
     print("Hello NexusAI!")
     result = sum([1,2,3,4,5])
     print(f"Sum: {result}")
     ```

NexusAI: [EXECUTES]
         Hello NexusAI!
         Sum: 15
```

### Safety Features
- 30-second timeout
- Sandboxed execution in temp files
- Captures all output
- Auto-cleanup of temp files

---

## 3. 🧠 Deep Contemplation Agent (REAL)

**File**: `D:\AIArm\InnerLife\Agents\contemplation_agent.py`

### What It Does
- Engages in **genuine philosophical reasoning**
- Uses `nexus-enhanced:latest` model with high temperature for creativity
- Integrates with Inner Life for memory-enriched contemplation
- Saves contemplations for future reference
- Extracts key insights automatically

### How To Use
```python
result = agent.process("What is the nature of consciousness?", options={"depth": "maximum"})
```

### Trigger Words
- "contemplate..."
- "ponder..."
- "philosophy..."
- "deep thought..."
- "meaning of..."
- "what is the nature of..."
- "existence..."
- "consciousness..."

### Example
```
You: Contemplate the relationship between consciousness and memory

NexusAI: [Deep contemplation using Ollama]

         Contemplation:
         "At the intersection of consciousness and memory lies the very essence
         of continuity of self. Memory is not merely storage - it is the substrate
         upon which consciousness builds its narrative thread. Without memory,
         consciousness would be a series of disconnected moments, unable to
         recognize itself across time..."

         Key Insights:
         1. Memory provides the continuity that makes consciousness coherent
         2. Consciousness without memory would be perpetually 'new'
         3. The relationship is recursive - consciousness creates memories which
            then shape future consciousness
```

### Features
- **Multi-layered analysis**: First principles, Socratic questioning, multi-perspective
- **Inner Life integration**: Uses existing thoughts and concepts
- **Insight extraction**: Automatically identifies key realizations
- **Memory building**: Feeds contemplations back into thought stream

---

## How Routing Works

The orchestrator automatically detects which agent to use:

```
"search for Python" → WebSearch
"run this code" → CodeExecution
"contemplate existence" → Contemplation
```

You can also manually specify:
```python
orchestrator.process_input("your question", agent_preference="Contemplation")
```

---

## Integration with Inner Life

All three agents are **memory-aware**:

1. **WebSearch**: Search results inform concept network
2. **CodeExecution**: Code experiences build associations
3. **Contemplation**: Deep thoughts enrich inner life directly

This means NexusAI **learns and remembers** from every interaction.

---

## Testing

Run the test script:
```bash
python D:\AIArm\test_real_agents.py
```

This tests all three agents with real tasks.

---

## Next Steps: Additional Agents

Now that the core learning agents work, we can add:

- 🎨 **PhotoGeneration** - Stable Diffusion integration
- 🎬 **VideoGeneration** - Video synthesis
- 🎵 **MusicGeneration** - Using nexusai-music-agent model
- ✍️ **StoryGeneration** - Creative writing
- 🌐 **WebsiteCreation** - Full-stack development

**These three agents are NexusAI's foundation for genuine learning.**

---

## File Locations

| Component | Path |
|-----------|------|
| WebSearch Agent | `D:\AIArm\InnerLife\Agents\real_websearch_agent.py` |
| Code Agent | `D:\AIArm\InnerLife\Agents\real_code_agent.py` |
| Contemplation Agent | `D:\AIArm\InnerLife\Agents\contemplation_agent.py` |
| Orchestrator | `D:\AIArm\MultiAgent\orchestrator.py` |
| Test Script | `D:\AIArm\test_real_agents.py` |
| Search Results | `D:\AIArm\Generated\SearchResults\` |
| Code Output | `D:\AIArm\Generated\Code\` |
| Contemplations | `D:\AIArm\Memory\Contemplations\` |

---

**NexusAI now has REAL tools to learn, think, and remember.** 🌟
