# UE5 Integration - Step-by-Step Guide

## 🎮 Integrating NexusAI HTML Interface into Unreal Engine 5

This guide shows you how to embed your NexusAI HTML interface into UE5 with holographic effects.

---

## ✅ Prerequisites

1. **NexusAI Backend Running**
   ```powershell
   cd D:\AIArm
   python NEXUS_ULTIMATE_INTERFACE.py
   ```
   Should show: "NEXUS ULTIMATE INTERFACE ONLINE"

2. **HTML Interface Working**
   - Open `index.html` in browser
   - Should connect to backend
   - Status should show "Connected"

3. **UE5 Project Open**
   - Your NexusAI project loaded
   - Content Browser visible

---

## 📦 Phase 1: Enable Web Browser Plugin (5 minutes)

### Step 1: Open Plugins Window

1. In UE5, click **Edit** menu (top left)
2. Click **Plugins**
3. Plugin window opens

### Step 2: Find Web Browser Plugin

1. In the search box, type: `web browser`
2. You'll see **"Web Browser Widget"** plugin
3. **Check the box** next to it to enable
4. Click **Restart Now** button

### Step 3: Wait for Restart

1. UE5 will close and reopen
2. Your project will reload
3. Wait for shaders to compile (if any)

---

## 🎨 Phase 2: Create Web Browser Widget (10 minutes)

### Step 1: Create Widget Blueprint

1. In **Content Browser**, navigate to your **UI** folder (or create one)
2. **Right-click** in empty space
3. **User Interface → Widget Blueprint**
4. Name it: `NexusAI_WebInterface`
5. **Double-click** to open it

### Step 2: Add Web Browser Component

1. You're now in the **Widget Designer** view
2. On the left side, find the **Palette** panel
3. Scroll down to **"Special"** category
4. Find **"Web Browser"** component
5. **Drag** it onto the canvas (the checkered area in the center)

### Step 3: Make Web Browser Fill Screen

1. **Select** the Web Browser component (click on it)
2. Look at the **Details** panel (right side)
3. Find **"Anchors"** section at the top
4. Click the **anchor preset selector** (looks like a grid)
5. Click the **bottom-right preset** (fills entire screen)
6. The Web Browser should now cover the entire canvas

### Step 4: Configure Web Browser Settings

1. With Web Browser still selected, in **Details** panel:
2. Find **"Initial URL"** field
3. Enter: `file:///D:/AIArm/NexusAI_Interface/NexusAI_Custom/index.html`
   - ⚠️ **IMPORTANT**: Use forward slashes `/` not backslashes `\`
   - ⚠️ **IMPORTANT**: Use `file:///` (three slashes)
4. Scroll down, find **"Supports Transparency"**
5. **Check** the box ✅
6. Scroll to top, find **"Is Variable"**
7. **Check** the box ✅

### Step 5: Compile and Save

1. Click **"Compile"** button (top toolbar)
2. Wait for green checkmark
3. Click **"Save"** button
4. Close the Widget Designer

---

## 🔗 Phase 3: Add Widget to Level (10 minutes)

### Step 1: Open Level Blueprint

1. In the main UE5 window, click **Blueprints** button (top toolbar)
2. Click **"Open Level Blueprint"**
3. Blueprint editor opens

### Step 2: Clear Existing Nodes (if any)

1. If you have old nodes from previous setup:
   - **Select all** (Ctrl+A)
   - **Delete** (Delete key)
2. Start fresh

### Step 3: Create Widget on Begin Play

1. Find **Event BeginPlay** node (should already be there)
   - If not: Right-click → Add Event → Event BeginPlay
2. **Drag** from the white pin on the right of BeginPlay
3. In the search box, type: `create widget`
4. Select **"Create Widget"**
5. In the new node, click the **dropdown** that says "Select Class"
6. Choose **"NexusAI_WebInterface"** (your widget)

### Step 4: Add Widget to Viewport

1. **Drag** from the **Return Value** pin of Create Widget node
2. Type: `add to viewport`
3. Select **"Add to Viewport"**
4. Connect the **white execution pins** (arrow from BeginPlay → Create Widget → Add to Viewport)

### Step 5: Set Input Mode (Optional but Recommended)

1. **Drag** from the white pin after "Add to Viewport"
2. Type: `set input mode ui only`
3. Select **"Set Input Mode UI Only"**
4. Connect the execution pin
5. On this node:
   - **Player Controller**: Drag from BeginPlay → type `get player controller` → connect
   - **In Widget to Focus**: Drag from Create Widget's Return Value → connect

### Step 6: Show Mouse Cursor

1. From "Set Input Mode UI Only", drag the white pin
2. Type: `set show mouse cursor`
3. Select **"Set Show Mouse Cursor"**
4. On this node:
   - **Target**: Connect to "Get Player Controller"
   - **Show Mouse Cursor**: Check the box ✅

### Step 7: Compile and Save

1. Click **"Compile"** (top left)
2. Click **"Save"**
3. Close Blueprint editor

---

## ▶️ Phase 4: Test the Integration (5 minutes)

### Step 1: Make Sure Backend is Running

```powershell
# In PowerShell, check if running
cd D:\AIArm
python NEXUS_ULTIMATE_INTERFACE.py
```

### Step 2: Play in UE5

1. In main UE5 window, click **"Play"** button (top toolbar) or press **Alt+P**
2. Wait for level to load

### Step 3: What You Should See

✅ **SUCCESS INDICATORS:**
- HTML interface loads in UE5 viewport
- Status bar shows "Connected" in cyan
- You can see the capability buttons
- Mouse cursor is visible
- You can click and type

❌ **IF NOTHING SHOWS:**
- Check Output Log (Window → Developer Tools → Output Log)
- Look for errors mentioning "Web Browser" or file path
- Verify file path is correct
- Make sure Web Browser plugin is enabled

### Step 4: Test Functionality

1. **Click** in the text input box at the bottom
2. **Type**: `Hello NexusAI`
3. **Press Enter** or click **Send**
4. **Wait** for response to appear
5. **Try a capability button** - click "Image"
6. **Type**: `a futuristic AI interface`
7. **Click Send**

### Step 5: Stop Play Mode

1. Press **Escape** or click **Stop** button
2. You're back in editor mode

---

## 🌟 Phase 5: Add Holographic Effects (20 minutes)

### Step 1: Add Post Process Volume

1. In **Place Actors** panel (left side), search: `post process`
2. **Drag** "Post Process Volume" into your level
3. **Select** it (click on it in viewport or World Outliner)

### Step 2: Make it Global

1. In **Details** panel (right side)
2. Find **"Post Process Volume Settings"**
3. Check **"Infinite Extent (Unbound)"** ✅
4. This makes effects apply everywhere

### Step 3: Configure Bloom (Glow Effect)

1. Still in Details panel, scroll down
2. Find **"Bloom"** section
3. Click the **arrow** to expand it
4. Set these values:
   - **Method**: Standard
   - **Intensity**: `3.0`
   - **Threshold**: `0.5`
   - **Size Scale**: `4.0`
   - Check the boxes next to each to enable them ✅

### Step 4: Add Color Grading

1. Scroll to **"Color Grading"** section
2. Expand **"Global"** subsection
3. Set:
   - **Saturation**: Increase cyan (B channel) to `1.2`
   - **Gain**: Add slight blue tint - set to `(R:0.95, G:0.95, B:1.05, A:1.0)`
4. Expand **"Shadows"** subsection
5. Set:
   - **Gain**: Make darker - set to `(R:0.8, G:0.8, B:0.9, A:1.0)`

### Step 5: Add Vignette

1. Find **"Lens"** section
2. Expand **"Image Effects"** subsection
3. Find **"Vignette Intensity"**
4. Set to: `0.4`
5. Check the box ✅

### Step 6: Test Effects

1. Click **Play** (Alt+P)
2. You should see:
   - Cyan/blue elements glow
   - Slightly darker edges (vignette)
   - More vibrant cyan colors
   - Overall "holographic" feel

---

## 🎨 Phase 6: Optional Enhancements (15 minutes)

### Option A: Add Background Blur

1. Open **NexusAI_WebInterface** widget
2. In **Designer** view
3. **Add** an **Image** component
4. Place it **behind** the Web Browser (in Hierarchy panel, drag it above Web Browser)
5. Set:
   - **Anchor**: Fill screen
   - **Color**: Dark blue with low opacity `(R:0, G:0.1, B:0.2, A:0.3)`
   - **Brush → Draw As**: Rounded Box
   - **Brush → Rounding**: `(10, 10, 10, 10)`

### Option B: Add Animated Background

1. In your level, add a **Plane** mesh
2. Position it behind the camera
3. Create a **Material** with:
   - Animated noise texture
   - Cyan/blue color
   - Emissive for glow
4. Apply to plane

### Option C: Add Particle Effects

1. In **Place Actors**, search: `particle`
2. Add **"GPU Sprites"** or **"Niagara System"**
3. Configure for:
   - Small cyan particles
   - Slow floating motion
   - Subtle glow

---

## 🐛 Troubleshooting

### Interface Not Loading

**Problem**: Black screen or "Failed to load" message

**Solutions**:
1. Check file path - must use forward slashes: `file:///D:/AIArm/...`
2. Verify HTML file exists at that location
3. Check Output Log for specific error
4. Try opening HTML in browser first to verify it works

### Backend Not Connecting

**Problem**: Status shows "Backend Offline"

**Solutions**:
1. Start backend: `python NEXUS_ULTIMATE_INTERFACE.py`
2. Check it's running on port 8001
3. Open browser console (F12) to see connection errors
4. Verify firewall isn't blocking localhost connections

### Can't Click or Type

**Problem**: Interface visible but not interactive

**Solutions**:
1. Check "Set Input Mode UI Only" node exists
2. Verify "Set Show Mouse Cursor" is set to true
3. Make sure Web Browser has "Supports Transparency" checked
4. Try clicking "Simulate" instead of "Play" to test

### Holographic Effects Not Visible

**Problem**: Interface looks flat, no glow

**Solutions**:
1. Verify Post Process Volume has "Infinite Extent" checked
2. Check Bloom settings are enabled (checkboxes)
3. Increase Bloom Intensity to `5.0` for more glow
4. Make sure you're in Lit view mode (not Unlit)

### Performance Issues

**Problem**: Low FPS, laggy interface

**Solutions**:
1. Reduce Bloom Size Scale to `2.0`
2. Lower screen resolution
3. Disable particle effects if added
4. Close other applications
5. Check Task Manager for CPU/RAM usage

---

## 📦 Phase 7: Package for Distribution (Optional)

### Step 1: Project Settings

1. **Edit → Project Settings**
2. **Packaging** section
3. Set:
   - **Build Configuration**: Shipping
   - **Full Rebuild**: ✅
   - **For Distribution**: ✅

### Step 2: Package Project

1. **File → Package Project → Windows → Windows (64-bit)**
2. Choose output folder
3. Wait for packaging (10-30 minutes)
4. Test the .exe file

### Step 3: Include Backend

1. Copy `NEXUS_ULTIMATE_INTERFACE.py` to package folder
2. Create `start_nexus.bat`:
   ```batch
   @echo off
   start python NEXUS_ULTIMATE_INTERFACE.py
   start NexusAI.exe
   ```
3. Include Python installer or instructions

---

## ✅ Final Checklist

Before showing to clients:

- [ ] Backend starts without errors
- [ ] HTML interface loads in browser
- [ ] Interface loads in UE5
- [ ] Can type and send messages
- [ ] AI responses appear
- [ ] All capability buttons work
- [ ] Artifacts display correctly
- [ ] Holographic effects visible
- [ ] No console errors
- [ ] Smooth performance (30+ FPS)
- [ ] Mouse cursor visible and responsive
- [ ] Professional appearance

---

## 🎉 You're Done!

You now have a fully functional, visually stunning AI interface embedded in Unreal Engine 5!

**Next Steps:**
1. Customize branding and colors
2. Add more capabilities
3. Improve artifact display
4. Add animations and transitions
5. Create demo scenarios for clients
6. Package for distribution

**Need Help?**
- Check UE5 Output Log for errors
- Check browser console (F12) for JavaScript errors
- Review backend terminal for API errors
- Test each component individually

---

**Congratulations! Your NexusAI Command Center is ready for client demos!** 🚀

