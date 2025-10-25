# Nexus UI - React Interface for Nexus AI

Beautiful dark-themed React interface for your Nexus AI system, inspired by your design screenshots.

## Features

- **Sphere Home** - 3D animated sphere interface with floating action cards
- **Chat Interface** - Natural conversation with Nexus AI
- **System Monitor** - Performance and status monitoring (coming soon)
- **Mind View** - Inner Life thought stream visualization (coming soon)
- **Settings** - System configuration (coming soon)

## Design Inspiration

Based on your aesthetic preferences:
- Dark theme with purple/pink gradients
- Animated 3D sphere as central element
- Modern, sleek UI with glassmorphism effects
- Smooth animations and transitions

## Architecture

```
┌─────────────────────────────────────────┐
│  React Frontend (Port 3002)             │
│  - Vite + React 18                      │
│  - Framer Motion animations             │
│  - Axios for API calls                  │
└─────────────┬───────────────────────────┘
              │
              │ HTTP Requests
              ▼
┌─────────────────────────────────────────┐
│  Flask API Server (Port 5000)           │
│  - Routes requests to Nexus             │
│  - CORS enabled                         │
└─────────────┬───────────────────────────┘
              │
              │ Python imports
              ▼
┌─────────────────────────────────────────┐
│  Nexus Actionable Backend               │
│  - All AI capabilities                  │
│  - File operations                      │
│  - Agent system                         │
└─────────────────────────────────────────┘
```

## Installation

The unified launcher (`START_AIARM.bat`) handles installation automatically!

### Manual Installation (if needed)

```bash
cd D:\AIArm\NexusUI
npm install
```

## Running

### Easy Way (Recommended)
```bash
D:\AIArm\START_AIARM.bat
```

This starts:
1. Checks Ollama
2. Installs dependencies (first run)
3. Starts Flask API server
4. Starts React dev server
5. Opens browser to http://localhost:3002

### Manual Way

Terminal 1 - Backend:
```bash
cd D:\AIArm
python nexus_api_server.py
```

Terminal 2 - Frontend:
```bash
cd D:\AIArm\NexusUI
npm start
```

## Components

### SphereHome
- Central animated 3D sphere
- Mouse-reactive rotation
- Floating action cards
- Particle effects

### ChatInterface
- Real-time chat with Nexus
- Message history
- Typing indicators
- Suggested prompts

### Navigation
- Bottom nav bar
- Smooth page transitions
- Active state indicators

## API Endpoints

**Flask Backend (localhost:5000):**
- `GET /api/status` - Check if Nexus is online
- `POST /api/chat` - Send message to Nexus
- `GET /api/system` - Get system information

## Technologies

- **React 18** - UI framework
- **Vite** - Build tool
- **Framer Motion** - Animations
- **Axios** - HTTP client
- **Flask** - Python backend
- **Flask-CORS** - Cross-origin requests

## Color Scheme

```css
--primary-glow: #7c3aed (Purple)
--secondary-glow: #ec4899 (Pink)
--bg-dark: #0a0a0f (Almost black)
--bg-card: #1a1a2e (Dark blue-gray)
```

## Customization

Edit colors in `src/index.css`:
```css
:root {
  --primary-glow: #7c3aed;
  --secondary-glow: #ec4899;
  --bg-dark: #0a0a0f;
  --bg-card: #1a1a2e;
}
```

## Build for Production

```bash
npm run build
npm run preview
```

## Troubleshooting

**React app won't start:**
```bash
cd D:\AIArm\NexusUI
rm -rf node_modules
npm install
npm start
```

**Backend not connecting:**
- Check Flask server is running on port 5000
- Check CORS is enabled
- Verify Nexus Actionable is importable

**Browser not opening:**
- Manually visit http://localhost:3002
- Check if port 3002 is available

## Next Steps

1. Add system monitoring with real-time stats
2. Integrate Inner Life thought stream
3. Add settings panel
4. Implement file browser
5. Add voice interface

---

**Your Nexus AI now has a beautiful interface!** 🚀
