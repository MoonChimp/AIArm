# 🎯 CLINE INSTRUCTIONS FOR NEXUS AI 3D UE5 SYSTEM

## ⚠️ CRITICAL: READ THIS ENTIRE DOCUMENT BEFORE MAKING ANY CHANGES

---

## 🏗️ System Architecture - UNDERSTAND THIS FIRST

```
UE5 (C++/Blueprint/Python) 
    ↓ HTTP REST API
NEXUS_UE5_API.py (FastAPI Server)
    ↓ Function Calls
Python AI Backend (Ollama/Your AI System)
```

**NEVER mix these layers! Each has its own language and purpose.**

---

## 📁 File Structure - DO NOT DEVIATE

```
D:\AIArm\
├── NEXUS_UE5_API.py                    # FastAPI server - PYTHON ONLY
├── LAUNCH_NEXUS_3D_SYSTEM.bat          # Windows batch launcher
├── NEXUS_UE5_PROJECT\                  # UE5 project directory
│   ├── Content\
│   │   ├── Python\
│   │   │   └── NexusAI_Interface.py    # UE5 Python bridge
│   │   ├── Blueprints\                 # UE5 Blueprint files (.uasset)
│   │   ├── Materials\                  # UE5 Materials
│   │   └── Maps\                       # UE5 Level files
│   ├── Config\                         # UE5 config files (.ini)
│   ├── Source\                         # C++ source (if needed)
│   └── NexusAI.uproject                # UE5 project file (JSON)
└── [Existing AI system files]
```

**RULES:**
- ✅ Python files go in root or Content/Python/
- ✅ UE5 assets stay in Content/
- ❌ NEVER put Python code in .uasset files
- ❌ NEVER put Blueprint code in .py files
- ❌ NEVER create files outside D:\AIArm\

---

## 🔴 COMMON MISTAKES TO AVOID

### ❌ MISTAKE #1: Mixing Languages
**WRONG:**
```python
# In NEXUS_UE5_API.py
import unreal  # ❌ This is UE5 Python, not available in standalone Python!
```

**RIGHT:**
```python
# In NEXUS_UE5_API.py
from fastapi import FastAPI  # ✅ Use FastAPI/standard Python libraries
```

### ❌ MISTAKE #2: Wrong Import Paths
**WRONG:**
```python
# In NexusAI_Interface.py (UE5 Python)
import fastapi  # ❌ FastAPI not available in UE5 Python context
```

**RIGHT:**
```python
# In NexusAI_Interface.py (UE5 Python)
import unreal  # ✅ Use unreal module for UE5
import requests  # ✅ Use requests for HTTP calls to API
```

### ❌ MISTAKE #3: Incorrect API Calls
**WRONG:**
```python
# Calling undefined endpoints
response = requests.post("http://localhost:8000/api/chat/send")  # ❌ Wrong endpoint
```

**RIGHT:**
```python
# Use exact endpoints defined in NEXUS_UE5_API.py
response = requests.post("http://localhost:8000/api/chat", json={"message": "Hello"})  # ✅
```

### ❌ MISTAKE #4: File Path Errors
**WRONG:**
```python
ue_path = "C:\\Program Files\\Epic Games\\UE_5.6\\..."  # ❌ Hardcoded, may not exist
```

**RIGHT:**
```python
ue_path = os.getenv("UE5_PATH", "C:\\Program Files\\Epic Games\\UE_5.6\\...")  # ✅ Use env var with fallback
```

### ❌ MISTAKE #5: Not Handling Async Properly
**WRONG:**
```python
# In FastAPI endpoint
def some_function():
    result = some_async_call()  # ❌ Not awaiting async function
```

**RIGHT:**
```python
# In FastAPI endpoint
async def some_function():
    result = await some_async_call()  # ✅ Properly await async
```

---

## 📋 API ENDPOINT SPECIFICATION

### EXISTING ENDPOINTS (DO NOT CHANGE)

```python
# In NEXUS_UE5_API.py

# 1. Chat with AI
POST /api/chat
Request: {"message": "string", "context": "optional"}
Response: {"response": "string", "agents_used": ["agent1"]}

# 2. Register Interface
POST /api/interface/register
Request: {"interface_id": "string", "type": "UE5"}
Response: {"status": "registered", "interface_id": "string"}

# 3. Update Display
POST /api/interface/{interface_id}/display
Request: {"content": "string", "position": [x, y, z]}
Response: {"status": "updated"}

# 4. Activate Agent
POST /api/interface/{interface_id}/agent/{agent_name}
Request: {"action": "activate"}
Response: {"status": "activated"}

# 5. Trigger Effect
POST /api/interface/{interface_id}/effect
Request: {"effect_type": "string", "parameters": {}}
Response: {"status": "triggered"}
```

### WHEN ADDING NEW ENDPOINTS

**Template:**
```python
@app.post("/api/new_endpoint")
async def new_endpoint(request: RequestModel):
    """
    Purpose: [Describe what this does]
    Used by: [UE5 / External client / etc]
    """
    try:
        # 1. Validate input
        if not request.data:
            raise HTTPException(status_code=400, detail="Missing data")
        
        # 2. Process request
        result = await process_data(request.data)
        
        # 3. Return response
        return {"status": "success", "data": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🐍 PYTHON CODE GUIDELINES

### For NEXUS_UE5_API.py (FastAPI Server)

**REQUIRED IMPORTS:**
```python
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import Optional, Dict, List
```

**DO:**
- ✅ Use Pydantic models for request/response validation
- ✅ Use async/await for all I/O operations
- ✅ Add proper error handling with try/except
- ✅ Use type hints for all functions
- ✅ Log all important events
- ✅ Keep port 8000 unless user specifies otherwise

**DON'T:**
- ❌ Import unreal module (not available in standalone Python)
- ❌ Block the event loop with synchronous operations
- ❌ Return bare strings without proper JSON structure
- ❌ Forget CORS middleware for web clients
- ❌ Use print() instead of proper logging

### For NexusAI_Interface.py (UE5 Python)

**REQUIRED IMPORTS:**
```python
import unreal
import requests
import json
from typing import Optional, Dict, List
```

**DO:**
- ✅ Use unreal module for UE5 interactions
- ✅ Use requests library for HTTP calls to API
- ✅ Handle connection failures gracefully
- ✅ Use unreal.log() for debugging
- ✅ Cache UE5 object references to avoid repeated lookups

**DON'T:**
- ❌ Import FastAPI (not available in UE5 Python)
- ❌ Use threading (UE5 has its own tick system)
- ❌ Forget to check if objects exist before using them
- ❌ Make synchronous HTTP calls on main thread
- ❌ Hardcode API URLs (use configuration)

---

## 🎮 UE5 INTEGRATION GUIDELINES

### Blueprint ↔ Python Communication

**CORRECT Pattern:**
```python
# In NexusAI_Interface.py

@unreal.uclass()
class NexusAIInterface(unreal.BlueprintFunctionLibrary):
    
    @unreal.ufunction(static=True, meta=dict(Category="Nexus AI"))
    def send_message_to_ai(message: str) -> str:
        """Callable from Blueprints"""
        try:
            response = requests.post(
                "http://localhost:8000/api/chat",
                json={"message": message},
                timeout=30
            )
            return response.json()["response"]
        except Exception as e:
            unreal.log_error(f"AI request failed: {e}")
            return "Error communicating with AI"
```

### Creating 3D Elements

**CORRECT Pattern:**
```python
# Spawn a holographic display
def create_hologram(location, text):
    # 1. Load Blueprint class
    blueprint = unreal.EditorAssetLibrary.load_asset(
        "/Game/Blueprints/BP_HologramDisplay"
    )
    
    # 2. Spawn actor
    world = unreal.EditorLevelLibrary.get_editor_world()
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        blueprint.generated_class(),
        location
    )
    
    # 3. Set properties
    if actor:
        # Use Blueprint function to set text
        unreal.BlueprintFunctionLibrary.call_function_by_name(
            actor, "SetDisplayText", text
        )
    
    return actor
```

---

## 🔄 PROPER WORKFLOW FOR CHANGES

### When User Asks to Add a Feature:

**STEP 1: CLARIFY**
- Ask which component needs the change (UE5, API, or AI backend)
- Confirm the data flow direction
- Verify file locations

**STEP 2: PLAN**
- Write out the change in comments first
- Identify all files that need modification
- Check for dependencies

**STEP 3: IMPLEMENT**
- Make changes one file at a time
- Test each change before moving to next
- Follow the templates in this document

**STEP 4: VALIDATE**
- Check that imports are correct
- Verify API endpoints match
- Ensure data types are consistent
- Test error handling

---

## ✅ PRE-COMMIT CHECKLIST

Before submitting any code, verify:

### Python Files (NEXUS_UE5_API.py)
- [ ] All imports are standard Python libraries or FastAPI
- [ ] No `import unreal` statements
- [ ] All async functions use `async def` and `await`
- [ ] Pydantic models defined for request/response
- [ ] Error handling with try/except blocks
- [ ] Proper HTTP status codes (200, 400, 500, etc.)
- [ ] CORS middleware configured if needed
- [ ] Port 8000 used unless specified otherwise

### UE5 Python Files (NexusAI_Interface.py)
- [ ] `import unreal` present
- [ ] No FastAPI or uvicorn imports
- [ ] HTTP calls use requests library with timeout
- [ ] Functions decorated with @unreal.ufunction if Blueprint-callable
- [ ] Error logging uses unreal.log() or unreal.log_error()
- [ ] API URL matches NEXUS_UE5_API.py endpoints
- [ ] No blocking operations on main thread

### File Operations
- [ ] All file paths start with D:\AIArm\
- [ ] No files created outside project directory
- [ ] Proper directory structure maintained
- [ ] No modifications to .uproject file unless necessary

### API Communication
- [ ] Request/response JSON structure matches both sides
- [ ] Endpoint URLs are exactly the same in sender and receiver
- [ ] Timeout values set for HTTP requests
- [ ] Connection failures handled gracefully

---

## 🚨 ERROR HANDLING PATTERNS

### In API Server (NEXUS_UE5_API.py)

```python
@app.post("/api/endpoint")
async def endpoint(request: RequestModel):
    try:
        # Validate input
        if not request.required_field:
            raise HTTPException(
                status_code=400,
                detail="Missing required field: required_field"
            )
        
        # Process
        result = await process_something(request)
        
        # Return success
        return {
            "status": "success",
            "data": result
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
```

### In UE5 Python (NexusAI_Interface.py)

```python
def call_api(endpoint, data):
    try:
        response = requests.post(
            f"http://localhost:8000{endpoint}",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        unreal.log_error("API request timed out")
        return {"status": "error", "message": "Timeout"}
        
    except requests.exceptions.ConnectionError:
        unreal.log_error("Could not connect to API server")
        return {"status": "error", "message": "Connection failed"}
        
    except Exception as e:
        unreal.log_error(f"API call failed: {e}")
        return {"status": "error", "message": str(e)}
```

---

## 📝 CODE REVIEW TEMPLATE

When reviewing your own code, ask:

1. **Language Check**
   - Am I using the right language for this file?
   - Are all imports available in this context?

2. **Architecture Check**
   - Does this follow the correct data flow?
   - Am I calling the right component?

3. **Path Check**
   - Are all file paths correct and absolute?
   - Do all paths start with D:\AIArm\?

4. **API Check**
   - Do endpoint URLs match exactly?
   - Are request/response formats consistent?

5. **Error Check**
   - What happens if this fails?
   - Are errors logged appropriately?

6. **Type Check**
   - Do all functions have type hints?
   - Are Pydantic models used for API requests?

---

## 🎯 QUICK REFERENCE

### When to Use Each File:

**NEXUS_UE5_API.py** - Use when:
- Adding new API endpoints
- Modifying server behavior
- Changing how AI backend is called
- Adding WebSocket support
- Modifying CORS settings

**NexusAI_Interface.py** - Use when:
- Adding UE5-callable Python functions
- Modifying how UE5 calls the API
- Adding new Blueprint-exposed functions
- Changing 3D element creation
- Updating display logic

**Blueprints** - Use when:
- Creating 3D visual elements
- Adding UI components
- Implementing game logic
- Creating animations
- Setting up input handling

### Common Variable Names (Be Consistent):

```python
# API Server
app = FastAPI()              # Always name FastAPI instance 'app'
interface_id: str            # Use for UE5 instance identifier
agent_name: str              # Use for AI agent names

# UE5 Python
world = unreal.EditorLevelLibrary.get_editor_world()
actor: unreal.Actor
location: unreal.Vector
```

---

## 🔧 DEBUGGING CHECKLIST

If something doesn't work:

1. **Check Server is Running**
   ```batch
   # Should see: "Uvicorn running on http://localhost:8000"
   python NEXUS_UE5_API.py
   ```

2. **Check API Endpoint**
   ```bash
   # Use curl or browser to test
   curl http://localhost:8000/api/chat -X POST -H "Content-Type: application/json" -d '{"message":"test"}'
   ```

3. **Check UE5 Logs**
   - Open Output Log in UE5
   - Look for Python errors
   - Check unreal.log() messages

4. **Check File Paths**
   ```python
   # Add debug logging
   print(f"File exists: {os.path.exists(path)}")
   ```

5. **Check Imports**
   ```python
   # Try importing in Python REPL
   python
   >>> import unreal  # Should fail outside UE5
   >>> from fastapi import FastAPI  # Should work in standalone Python
   ```

---

## 💡 TIPS FOR SUCCESS

1. **Always read error messages completely** - They tell you exactly what's wrong
2. **Test one change at a time** - Don't modify multiple files simultaneously
3. **Use version control** - Git commit before making changes
4. **Keep backups** - Copy working files before modifying
5. **Ask for clarification** - If instructions are unclear, ask the user
6. **Document your changes** - Add comments explaining why, not just what
7. **Follow the templates** - Don't invent new patterns
8. **Validate assumptions** - Don't assume files exist or endpoints work

---

## 🚀 DEPLOYMENT CHECKLIST

Before deploying or packaging:

### API Server
- [ ] All dependencies in requirements.txt
- [ ] Environment variables documented
- [ ] Port configuration externalized
- [ ] Logging configured properly
- [ ] Error handling covers all cases

### UE5 Project
- [ ] All Python scripts in correct directories
- [ ] Blueprint functions tested
- [ ] API URL configurable (not hardcoded)
- [ ] All assets properly saved
- [ ] Project packages without errors

### System Integration
- [ ] Batch launcher works
- [ ] All components start in correct order
- [ ] Inter-process communication working
- [ ] Shutdown handled gracefully

---

## 📞 WHEN STUCK

If you're unsure about something:

1. **Stop and ask** - Don't guess
2. **Show the user** - Display what you're about to do
3. **Provide options** - Offer multiple approaches
4. **Check this document** - Re-read relevant sections
5. **Verify existing code** - Look at what's already working

---

## ⚡ FINAL REMINDER

**BEFORE WRITING ANY CODE:**
1. Read the user's request carefully
2. Identify which file(s) to modify
3. Check this document for the correct pattern
4. Plan the changes in comments first
5. Implement following the templates
6. Validate using the checklist

**The most common mistakes happen when you:**
- Don't read this document
- Mix up Python contexts (standalone vs UE5)
- Change the wrong file
- Forget error handling
- Don't test before submitting

**You can do this! Follow these instructions and you'll succeed!** 🎯

---

*Document Version: 1.0*
*Last Updated: 2025-10-24*
*For: Cline AI Assistant*
