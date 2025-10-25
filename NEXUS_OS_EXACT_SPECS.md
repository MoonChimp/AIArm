# NEXUS OS - Exact NitroSense Replication Specifications

## CURRENT STATUS
- ❌ Current design is NOT close enough to NitroSense
- ✅ Basic structure exists but needs complete visual overhaul
- ⚠️ 13+ duplicate background servers still running

## EXACT NITROSENSE FEATURES TO REPLICATE

### 1. **Home Tab (Main Screen)**
**From Screenshot 1:**
- Large circular gauges (3 total):
  - GPU Temperature (top right): 52°C with orange/red gradient ring
  - CPU Temperature (middle right): 61°C with orange gradient ring
  - System Temperature (bottom right): 47°C with orange gradient ring
- Each gauge has:
  - Animated circular progress ring
  - Large temperature number in center
  - Label below (GPU/CPU/System)
  - °C indicator
- **Left side:**
  - GPU Frequency gauge (circular) showing 1267 MHz
  - Live usage graphs (red/orange waveforms)
  - GPU Usage: 19%
  - CPU Usage: 24%
- **Bottom left:**
  - Feature cards (GIMP example shown)
  - Orange icon + description
  - "View all features" link

### 2. **Scenario Tab (Performance Modes)**
**From Screenshot 2:**
- **Three mode cards:**
  - Quiet (moon icon)
  - Balanced (layers icon)
  - Performance (flame icon) - **SELECTED** (orange highlight)
- **Large circular gauges below:**
  - GPU: Core Clock 367 MHz, Usage 0%
  - CPU: Core Clock 2054 MHz, Usage 13%
- **Description text:**
  "The introduction of Mode - Intended for gaming or rendering. CPU + GPU overclocked. Fan speed remains throttled."

### 3. **Fan Control Tab**
**From Screenshot 3:**
- **Three fan mode buttons:**
  - Auto (selected - orange)
  - Max
  - Custom
- **Circular fan speed indicators:**
  - GPU: 3302 RPM (spinning animation)
  - CPU: 3623 RPM (spinning animation)

### 4. **Advanced Settings Tab**
**From Screenshot 4:**
- **Acer TrueHarmony™ section:**
  - List of audio presets (Shooter, RPG, Strategy, Movies, Music, Voice, Automatic, Custom Audio)
  - Each with radio button (orange when selected)

### 5. **Personal Settings Tab**
**From Screenshot 5:**
- **Left sidebar navigation:**
  - Battery & Charge (selected - orange)
  - Screen
  - Keyboard
  - System Boot Effect
- **Main content area:**
  - Battery Charge Mode cards
  - Toggle switches (orange when on)
  - Dropdown selectors

### 6. **Checkup Tab**
**From Screenshot 6:**
- **Checkup All button** (large, orange, heart icon)
- **Device health cards:**
  - Battery (unchecked, progress bar 93%)
  - Storage drives (NVMe drives listed with capacity bars)
  - Each has "Check" button
  - "Last checked on: -" timestamp

### 7. **Monitoring Tab**
**From Screenshot 7:**
- **Live performance graphs:**
  - GPU temp/usage graph (red/orange waveform over time)
  - CPU temp/usage graph (red/orange waveform over time)
  - Fan speed indicators
  - Frequency displays
- **Right side system info:**
  - Temperature graph (red waveform)
  - RAM: 5200 MHz, 32.6 GB usage (34.0%)
  - Ethernet: Download 0.0 Kbps, Upload 0.0 Kbps
  - Wi-Fi: Download 48.0 Kbps, Upload 19.0 Kbps

### 8. **App Center Tab**
**From Screenshot 8:**
- **Grid of app icons** (4 columns)
- Each app card has:
  - App icon
  - App name
  - Clean hover effect
- Search bar at top
- Filter dropdowns (All Apps, Popularity)

## RIGHT SIDEBAR (All Screens)
**Consistent across all tabs:**
- **Scenario Profile dropdown** (Gaming selected)
- **Mode:** Performance >
- **Fan:** Auto >
- **Details >** button
- **Monitoring section:**
  - 6 metric boxes in 2x3 grid
  - GPU % / GPU °C / CPU %
  - CPU °C / System °C / RAM %
  - Large numbers in orange
  - Small labels in gray
- **Details >** button
- **Live Update section:**
  - "No items to update" or update list
  - "Check Now" button (orange)
- **Details >** button
- **App Shortcut icons** at bottom

## COLOR PALETTE (EXACT)
- **Primary Orange:** #FF6600 (bright orange)
- **Orange Glow:** rgba(255, 102, 0, 0.8)
- **Dark Background:** #0a0503 to #2a1410 (gradient)
- **Panel Background:** rgba(30, 18, 12, 0.95)
- **Border Orange:** rgba(255, 102, 0, 0.5)
- **Text White:** #ffffff
- **Text Gray:** #888888
- **Selected/Active:** Bright orange with glow

## TYPOGRAPHY
- **Font:** Segoe UI (Windows default)
- **Headers:** 14-16px, bold, letter-spacing 2px
- **Body:** 12-14px, normal weight
- **Numbers:** Large (24-48px) bold for metrics
- **Labels:** Small (10-12px) gray

## ANIMATIONS
- **Circular gauges:** Smooth rotating gradient
- **Graphs:** Live scrolling waveforms (red to orange gradient)
- **Fan indicators:** Rotating blade animation
- **Hover effects:** Subtle glow increase
- **Transitions:** 0.3s ease-in-out

## REQUIRED COMPONENTS

### Circular Gauge Component
```javascript
class CircularGauge {
    constructor(element, options) {
        this.element = element;
        this.value = options.value;
        this.max = options.max;
        this.label = options.label;
        this.unit = options.unit;
        // SVG circle with gradient stroke
        // Animated rotation
    }
}
```

### Live Graph Component
```javascript
class LiveGraph {
    constructor(canvas, options) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.data = [];
        this.maxPoints = 100;
        // Waveform with gradient (red to orange)
        // Scrolls right to left
    }
}
```

### Tab Navigation
```javascript
const tabs = ['Home', 'Scenario', 'Personal Settings', 'Checkup', 'Monitoring', 'App Center'];
// Orange underline on active tab
// Smooth content transition
```

## NEXUS OS ADAPTATIONS

### Home Tab → AI Dashboard
- **Replace:**
  - GPU/CPU/System temps → AI Model Temp / GPU Temp / System Temp
  - GPU frequency → Inference Speed (tokens/sec)
  - Usage graphs → AI processing graphs
- **Keep:**
  - Same circular gauge design
  - Same live graph animations
  - Same orange color scheme

### Scenario Tab → AI Modes
- **Three AI modes:**
  - Quiet (low power, slower responses)
  - Balanced (normal operation)
  - Performance (maximum speed, all agents active)
- **Show:**
  - LLM inference speed
  - Agent activation status

### Monitoring Tab → Full AI Monitoring
- **Show:**
  - Ollama service status (graph)
  - Stable Diffusion status (graph)
  - Nexus API status (graph)
  - All 6 agents (Code, Music, Photo, Story, Video, WebSearch)
  - LIRA 6 layers status

### App Center → Agent Launcher
- **Grid of agents:**
  - Each agent has icon, name, status
  - Click to activate/configure
  - Quick launch shortcuts

## TECHNICAL REQUIREMENTS

### File Structure
```
NexusOS/
├── index.html           # Main HTML with tab structure
├── styles.css           # Exact NitroSense styling
├── nexus-os.js          # Main controller
├── components/
│   ├── circular-gauge.js    # Reusable gauge component
│   ├── live-graph.js        # Scrolling waveform graph
│   ├── tab-navigation.js    # Tab system
│   └── right-sidebar.js     # Monitoring sidebar
├── serve.py             # HTTP server (no CORS)
└── assets/
    └── nexus-logo.gif   # Your actual logo
```

### Canvas-Based Graphics
All circular gauges and graphs MUST use HTML5 Canvas with:
- Gradient strokes (createLinearGradient)
- Rotation animations (requestAnimationFrame)
- Smooth transitions

### Real-Time Data
Poll every 5 seconds:
```javascript
GET /api/monitor → {
    cpu: 24,
    gpu: 52,
    system: 47,
    ram: 34.0,
    ollama: true,
    stable_diffusion: false,
    nexus_api: true,
    agents: {...},
    lira_layers: {...}
}
```

## PRIORITY FIXES

1. **KILL ALL 13+ BACKGROUND SERVERS**
   - Use proper task manager or batch file
   - Verify with `tasklist | findstr python`

2. **REBUILD HOME TAB** with exact circular gauges from Screenshot 1

3. **ADD CANVAS GRAPHS** for live monitoring (red/orange waveforms)

4. **FIX RIGHT SIDEBAR** to match 2x3 metric grid exactly

5. **ADD TAB NAVIGATION** with orange underline on active tab

6. **TEXTURE BACKGROUND** to match NitroSense's subtle pattern

7. **START STABLE DIFFUSION** properly so it shows ONLINE

## NEXT STEPS

1. Review this specification
2. Kill all duplicate servers manually
3. Rebuild NexusOS from scratch using exact NitroSense design
4. Test with all services running
5. Match pixel-perfect to screenshots

---

**GOAL:** NexusOS should be visually IDENTICAL to NitroSense but with:
- Nexus branding/logo
- AI-specific metrics instead of hardware
- Orange color scheme maintained
- All gaming aesthetic preserved

**Current Status:** Basic structure exists but needs complete visual overhaul to match NitroSense exactly.
