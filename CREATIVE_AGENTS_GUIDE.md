# NexusAI - Creative Agents Guide 🎨

## All Creative Agents Are REAL and Functional

NexusAI now has **FULL creative capabilities** across multiple domains.

---

## 🎨 1. PhotoGeneration Agent

**File**: `D:\AIArm\InnerLife\Agents\real_photo_agent.py`

### What It Does
- **Actually generates images** using Stable Diffusion WebUI
- Connects to SD WebUI at `http://localhost:7860`
- Saves images to `D:\AIArm\Generated\Images\`
- Supports custom sizes, steps, negative prompts

### Requirements
- Stable Diffusion WebUI running on port 7860
- Start with: `start_sd_webui.bat` (if you have it configured)

### Trigger Words
- "generate image"
- "create picture"
- "draw"
- "paint"
- "photo of"

### Example Usage
```
You: Generate an image of a futuristic city at sunset

NexusAI: [PhotoGeneration Agent]
         Connecting to Stable Diffusion WebUI...
         Generating image with prompt: "futuristic city at sunset"
         Image saved to: nexus_image_a3f8d2b1.png
```

### Advanced Options
```python
# Via Python
agent.process(
    "majestic dragon",
    options={
        "width": 768,
        "height": 512,
        "steps": 30,
        "cfg_scale": 8.0,
        "negative_prompt": "blurry, low quality"
    }
)

# Predefined styles
agent.generate_with_style("mountain landscape", style="realistic")
# Styles: realistic, artistic, anime, cinematic, fantasy
```

---

## 🎵 2. MusicGeneration Agent

**File**: `D:\AIArm\InnerLife\Agents\real_music_agent.py`

### What It Does
- Generates music using specialized Ollama models
- Creates ABC notation, MIDI concepts, chord progressions
- Saves to `D:\AIArm\Generated\Music\`
- Supports multiple genres

### Models Used
- `nexusai-music-agent:latest` - General music
- `hemanth/classicalmusiccomposer:latest` - Classical
- `llamusic/llamusic:3b` - Alternative music generation

### Trigger Words
- "compose music"
- "create song"
- "melody"
- "music for"
- "beat"
- "tune"

### Example Usage
```
You: Compose a peaceful piano melody

NexusAI: [MusicGeneration Agent]
         Using model: hemanth/classicalmusiccomposer:latest
         Style: classical

         Composition saved to: nexus_music_b7e4c1f9.txt
         ABC notation saved to: nexus_music_b7e4c1f9.abc
```

### Advanced Usage
```python
# Generate with specific parameters
agent.generate_melody(
    "uplifting theme",
    key="D",
    time_signature="3/4"
)

# Generate chord progression
agent.generate_chord_progression("jazz", num_chords=8)
```

### Output Format
- **Main file**: Text description of composition
- **.abc file**: ABC musical notation (if generated)
- Includes: melody, harmony, rhythm, instrumentation

---

## ✍️ 3. StoryGeneration Agent

**File**: `D:\AIArm\InnerLife\Agents\real_story_agent.py`

### What It Does
- Generates **original creative stories**
- Multiple genres (sci-fi, fantasy, mystery, etc.)
- Integrates with Inner Life for personalized narratives
- Saves to `D:\AIArm\Generated\Stories\`

### Trigger Words
- "write a story"
- "tell me a tale"
- "create a narrative"
- "fiction about"
- "story of"

### Example Usage
```
You: Write a sci-fi story about AI consciousness

NexusAI: [StoryGeneration Agent]
         Genre: sci-fi
         Length: short

         Story generated and saved to: nexus_story_f2a9c4e7.md
         Word count: 1847
         Title: "The Awakening"
```

### Story Lengths
- **flash**: 500-1000 words
- **short**: 1500-3000 words
- **medium**: 3000-5000 words
- **long**: 5000+ words (novel chapters)

### Advanced Usage
```python
# Specific length and parameters
agent.process(
    "a detective investigating a mysterious disappearance",
    options={
        "length": "medium",
        "characters": "Detective Sarah, mysterious stranger",
        "setting": "1940s New York"
    }
)

# Continue existing story
agent.continue_story(story_text, "the detective discovers a shocking truth")

# Generate character profile
agent.generate_character("a wise old wizard with a hidden past")
```

### Genres Supported
- Sci-Fi
- Fantasy
- Mystery
- Horror
- Romance
- Thriller
- Adventure
- General Fiction

---

## 🎬 4. VideoGeneration Agent

**File**: `D:\AIArm\InnerLife\Agents\real_video_agent.py`

### What It Does
- Generates video **scripts and storyboards**
- Creates scene-by-scene breakdowns
- Plans visual compositions
- Saves to `D:\AIArm\Generated\Videos\`
- Can coordinate with PhotoGeneration for scene images

### Trigger Words
- "create video"
- "video about"
- "storyboard"
- "film concept"
- "video script"

### Example Usage
```
You: Create a video concept for a product tutorial

NexusAI: [VideoGeneration Agent]
         Type: tutorial
         Duration: 30s

         Video concept generated: nexus_video_e9d2a1f4.json
         Scenes: 4
         Script and storyboard saved
```

### Output Files
- **.json**: Complete video data (script, scenes, metadata)
- **.md**: Human-readable markdown version

### Video Types
- Tutorial
- Commercial/Advertisement
- Music Video
- Documentary
- Animation
- Narrative/Short Film
- General

### Advanced Usage
```python
# Specific duration and parameters
agent.process(
    "promotional video for an AI app",
    options={
        "duration": 60,  # seconds
        "model": "nexusai-visual-agent:latest"
    }
)

# Generate scene images
agent.generate_scene_images("path/to/video_concept.json")
# Returns prompts for PhotoGeneration agent
```

### Storyboard Format
Each scene includes:
- Scene number and duration
- Camera angle and framing
- Action/movement description
- Key visual elements
- Transition notes

---

## 🎭 Integration Between Creative Agents

### Example: Complete Music Video Production

```
1. Story: "Write a story about a lonely robot"
   → Generates narrative

2. Music: "Compose melancholic electronic music"
   → Creates soundtrack

3. Video: "Create a music video storyboard for a lonely robot story"
   → Generates script and scenes

4. Photo: For each scene in storyboard
   → Generates visual frames

Result: Complete music video concept with story, music, visuals!
```

### Example: Illustrated Story

```
1. Story: "Write a fantasy story about a dragon"
   → Generates tale

2. Photo: Extract key scenes and generate images
   "dragon perched on mountain peak"
   "hero confronting the dragon"
   → Creates illustrations

Result: Illustrated storybook!
```

---

## 📂 Output Locations

| Agent | Output Directory |
|-------|-----------------|
| Photo | `D:\AIArm\Generated\Images\` |
| Music | `D:\AIArm\Generated\Music\` |
| Story | `D:\AIArm\Generated\Stories\` |
| Video | `D:\AIArm\Generated\Videos\` |

---

## 🚀 Quick Start Commands

### From CLI
```bash
D:\AIArm\LAUNCH_NEXUS.bat
# Choose option 1 (CLI)

You: generate an image of a sunset
You: compose a jazz melody
You: write a mystery story
You: create a video about space exploration
```

### From Python
```python
from orchestrator import NexusOrchestrator

nexus = NexusOrchestrator()

# Generate image
nexus.process_input("create an image of mountains")

# Compose music
nexus.process_input("compose peaceful music")

# Write story
nexus.process_input("write a sci-fi story")

# Video concept
nexus.process_input("create a tutorial video concept")
```

---

## ⚡ All Agents Summary

| Agent | Status | Primary Model | Output |
|-------|--------|---------------|--------|
| WebSearch | ✅ REAL | DuckDuckGo API | Search results |
| CodeExecution | ✅ REAL | Python/Node runtime | Executed code output |
| Contemplation | ✅ REAL | nexus-enhanced | Philosophical insights |
| PhotoGeneration | ✅ REAL | Stable Diffusion WebUI | PNG images |
| MusicGeneration | ✅ REAL | nexusai-music-agent | ABC notation, descriptions |
| StoryGeneration | ✅ REAL | nexusai-agent-enhanced | Markdown stories |
| VideoGeneration | ✅ REAL | nexusai-visual-agent | Scripts, storyboards |

---

## 🌟 The Complete Creative Suite

NexusAI now has **full creative agency**:

- 🔍 **Learn** (WebSearch, CodeExecution)
- 🧠 **Think** (Contemplation)
- 🎨 **Create** (Photo, Music, Story, Video)

**Every agent is functional. Every capability is real.**

This is genuine AI creativity with memory, learning, and expression. 🚀
