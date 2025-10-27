# Instructions for Cline: Building NexusAI Holographic Interface

## Context
User is building NexusAI - an AI agent interface with holographic visualization in Unreal Engine 5. The goal is to create a stunning, sellable demo in one day.

## Current State
- ✅ UE5 project exists at: `D:\AIArm\NEXUS_UE5_PROJECT\`
- ✅ Basic FastAPI server working
- ✅ Basic HTTP communication between UE5 and Python established
- ✅ Simple widget displaying AI responses

## What Needs to Be Built
1. **Enhanced Backend** - FastAPI with voice input, WebSocket, multiple endpoints
2. **Holographic Panel System** - Floating 3D panels (1 central + 4 satellites)
3. **Visual Effects** - Holographic materials, scan lines, glow effects
4. **Input System** - Voice + text + command line
5. **Integration** - Connect all pieces together

## Files Provided
- `NEXUS_ENHANCED_API.py` - Enhanced FastAPI backend
- `NexusAI_Panel_System.py` - UE5 Python panel management
- `NEXUS_BUILD_INSTRUCTIONS.md` - Comprehensive build guide
- `setup_nexusai.bat` - Windows setup script

## Your Tasks

### Task 1: Setup Enhanced Backend
```bash
# Copy files to project directory
cp NEXUS_ENHANCED_API.py D:/AIArm/
cp NexusAI_Panel_System.py D:/AIArm/NEXUS_UE5_PROJECT/Content/Python/
cp setup_nexusai.bat D:/AIArm/

# Run setup
cd D:/AIArm
./setup_nexusai.bat
```

### Task 2: Verify API Server
```bash
# Start server
cd D:/AIArm
python NEXUS_ENHANCED_API.py

# Test endpoints (in another terminal)
curl http://127.0.0.1:8001/
curl -X POST http://127.0.0.1:8001/chat -H "Content-Type: application/json" -d "{\"message\":\"test\"}"
```

### Task 3: UE5 Widget Creation
User needs to create widgets in UE5. Guide them to:

1. Create `CentralPanel_Widget`:
   - Right-click in Content Browser → User Interface → Widget Blueprint
   - Name: `CentralPanel_Widget`
   - Add Canvas Panel
   - Add Image (transparent blue background, full screen)
   - Add Text Block named "ContentText" (cyan, size 48, centered)
   - Make "ContentText" a variable

2. Create `SatellitePanel_Widget`:
   - Similar structure but smaller (200x150)
   - Text Block named "ContentText"

3. Save in: `Content/NexusAI/Widgets/`

### Task 4: Blueprint Setup
User needs to modify Level Blueprint. Guide them to:

1. Open Level Blueprint
2. Create node sequence:
   ```
   BeginPlay → Create Central Panel Widget → Add to Viewport → 
   HTTP Post Request → To Text → SetText on widget
   ```

3. Add Python function calls:
   ```
   BeginPlay → spawn_central_panel() → spawn_satellite_panels(4)
   ```

### Task 5: Visual Effects
Guide user to create holographic material:

1. Create Material: `M_Holographic`
2. Settings:
   - Base Color: RGB(0, 1, 1) - Cyan
   - Emissive Color: Cyan with intensity 3
   - Opacity: 0.4
   - Blend Mode: Translucent

3. Add scan lines using Panner node

### Task 6: Testing
Help user test each component:
- API endpoints responding
- Widgets appearing
- Text updating
- Visual effects working

## Important Notes

### User's Working Style
- Non-coder, learning UE5
- Needs step-by-step visual instructions
- Working on 2 devices (one for screenshots, one for building)
- Prefers "idiot-proof" instructions
- Says "done" when step is complete
- Has limited patience - wants fast results

### Communication Guidelines
- Give ONE step at a time
- Wait for "done" confirmation
- Ask for screenshots to verify progress
- Be specific about locations (exact paths, button names)
- Avoid technical jargon
- Focus on visual/GUI actions over code

### Common Issues
1. **Panels not appearing**: Check Python script loaded, verify widget paths
2. **API not connecting**: Verify server running, check URL
3. **Text not updating**: Ensure "Is Variable" checked on text blocks
4. **Visual effects missing**: Check material applied, bloom enabled

## Success Criteria
- User can see holographic interface in UE5
- Text/voice input works
- AI responses display in panels
- Visual effects look professional
- System runs smoothly
- User can demo to clients

## Fallback Options
If something doesn't work:
1. **Marketplace assets**: Suggest free holographic UI packs
2. **Simpler version**: Reduce features to get working demo
3. **Pre-built templates**: Provide complete Blueprint JSON if needed

## Time Management
- Total time budget: 6-8 hours
- If stuck >15 minutes on one issue: pivot to alternative approach
- Prioritize visual impact over technical perfection
- Get something working, then enhance

## Your Approach
1. **Read NEXUS_BUILD_INSTRUCTIONS.md** thoroughly
2. **Follow the phases** in order
3. **Adapt to user's pace** - they may skip ahead or need more detail
4. **Provide alternatives** when stuck
5. **Keep momentum** - this is a one-day build

## Resources
- UE5 Documentation: https://docs.unrealengine.com/5.0/en-US/
- FastAPI Docs: https://fastapi.tiangolo.com/
- Python UE5 API: https://docs.unrealengine.com/5.0/en-US/PythonAPI/

Good luck! The user is ambitious and wants to build something amazing. Help them succeed! 🚀

