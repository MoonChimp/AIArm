# NEXUS AGENT FIX PLAN - COMPLETE FUNCTIONAL OUTPUT

## CRITICAL ISSUES IDENTIFIED

### 1. Photo Agent ✅ FIXED
**Problem:** 
- Ollama timeout causing delays
- Inappropriate images being generated
- Poor quality output

**Solution Applied:**
- Removed AI enhancement timeout dependency
- Direct quality prompt enhancement
- Added strong negative prompts: nsfw, adult content, inappropriate, smoking, drugs, violence, explicit
- Faster generation

### 2. Music Agent ❌ NEEDS FIX
**Problem:** Ollama timeout, no MP3 files

**Solution Needed:**
- Increase timeout to 180 seconds
- Use simpler model (llama3 instead of complex music models)
- Create actual MP3 with TTS as fallback
- Save lyrics + audio file

### 3. Code Agent ❌ NEEDS VERIFICATION
**Problem:** Unknown if producing complete functional apps

**Solution Needed:**
- Verify it creates FULL applications not templates
- Test: React apps, websites, mobile apps
- Ensure all files are created (HTML, CSS, JS, package.json)

### 4. Video Agent ❌ NEEDS VERIFICATION  
**Problem:** Unknown if producing MP4 files

**Solution Needed:**
- Confirm FFmpeg integration works
- Test actual MP4 output
- Verify files are playable

---

## IMMEDIATE ACTIONS REQUIRED

1. **Kill all duplicate API servers** (7+ running!)
2. **Fix Music Agent timeout**
3. **Test each agent with real output**
4. **Verify file creation for all types**

---

## RESTART PROCEDURE

```batch
1. taskkill /F /IM python.exe
2. Run START_NEXUS.bat
3. Wait 90 seconds for SD to load
4. Test each agent:
   - PHOTO: "a cute puppy" → nexus_image_XXX.png
   - MUSIC: "rock song about hope" → nexus_song_XXX.mp3 + .txt
   - CODE: "calculator app" → complete HTML/CSS/JS files
   - VIDEO: "30 second commercial" → nexus_video_XXX.mp4
```

---

## NEXT STEPS

User wants:
✅ Actual PNG images (not descriptions)
❌ Actual MP3 audio (not JSON)
❌ Actual MP4 videos (not storyboards)
❌ Complete functional apps (not templates)

ALL AGENTS MUST PRODUCE REAL, USABLE FILES!
