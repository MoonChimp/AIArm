# 🎨 COPY-PASTE TEMPLATES FOR NEXUS AI SYSTEM

## 📋 Quick Navigation
- [API Endpoint Templates](#api-endpoint-templates)
- [UE5 Python Function Templates](#ue5-python-function-templates)
- [3D Element Creation Templates](#3d-element-creation-templates)
- [AI Agent Integration Templates](#ai-agent-integration-templates)
- [Visual Effect Templates](#visual-effect-templates)
- [Complete Feature Examples](#complete-feature-examples)

---

## 🔌 API ENDPOINT TEMPLATES

### Template 1: Simple POST Endpoint
**File:** `NEXUS_UE5_API.py`

```python
# Add this Pydantic model at the top with other models
class YourRequestModel(BaseModel):
    """Request model for your endpoint"""
    required_field: str
    optional_field: Optional[str] = None
    numerical_field: Optional[int] = 0

class YourResponseModel(BaseModel):
    """Response model for your endpoint"""
    status: str
    data: Dict
    message: Optional[str] = None

# Add this endpoint with other @app.post() routes
@app.post("/api/your_endpoint", response_model=YourResponseModel)
async def your_endpoint(request: YourRequestModel):
    """
    Purpose: [Describe what this endpoint does]
    
    Args:
        request: YourRequestModel with required fields
        
    Returns:
        YourResponseModel with status and data
        
    Example:
        POST /api/your_endpoint
        {
            "required_field": "value",
            "optional_field": "optional value"
        }
    """
    try:
        # 1. Validate input
        if not request.required_field:
            raise HTTPException(
                status_code=400,
                detail="Missing required_field"
            )
        
        # 2. Process your logic here
        result = {
            "processed": request.required_field,
            "optional": request.optional_field
        }
        
        # 3. Call AI backend if needed (example)
        # ai_response = await call_your_ai_function(request.required_field)
        # result["ai_data"] = ai_response
        
        # 4. Return success response
        return YourResponseModel(
            status="success",
            data=result,
            message="Operation completed successfully"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
        
    except Exception as e:
        # Log and return 500 for unexpected errors
        logger.error(f"Error in your_endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
```

### Template 2: Streaming/WebSocket Endpoint

```python
# Add WebSocket endpoint for real-time updates
@app.websocket("/ws/your_stream")
async def your_websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for streaming data
    
    Usage from UE5:
        ws = websocket.connect("ws://localhost:8000/ws/your_stream")
    """
    await websocket.accept()
    
    try:
        while True:
            # 1. Receive data from client
            data = await websocket.receive_text()
            
            # 2. Process the data
            result = await process_data(data)
            
            # 3. Send response back
            await websocket.send_json({
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011, reason=str(e))
```

### Template 3: GET Endpoint with Query Parameters

```python
@app.get("/api/get_data")
async def get_data(
    query: str,
    limit: int = 10,
    offset: int = 0,
    filter_type: Optional[str] = None
):
    """
    GET endpoint with query parameters
    
    Example:
        GET /api/get_data?query=test&limit=5&filter_type=recent
    """
    try:
        # 1. Validate parameters
        if limit > 100:
            raise HTTPException(
                status_code=400,
                detail="Limit cannot exceed 100"
            )
        
        # 2. Fetch data based on parameters
        results = []
        # Add your data fetching logic here
        
        # 3. Return paginated results
        return {
            "status": "success",
            "query": query,
            "results": results,
            "limit": limit,
            "offset": offset,
            "total": len(results)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Template 4: File Upload Endpoint

```python
from fastapi import File, UploadFile

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = None
):
    """
    Handle file uploads
    
    Example:
        POST /api/upload
        Content-Type: multipart/form-data
        file: [binary data]
        description: "Optional description"
    """
    try:
        # 1. Validate file type
        allowed_types = ["image/png", "image/jpeg", "application/pdf"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not allowed"
            )
        
        # 2. Read file content
        content = await file.read()
        
        # 3. Save file (example)
        file_path = f"D:\\AIArm\\uploads\\{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 4. Return success
        return {
            "status": "success",
            "filename": file.filename,
            "size": len(content),
            "path": file_path,
            "description": description
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🎮 UE5 PYTHON FUNCTION TEMPLATES

### Template 1: Blueprint-Callable Function
**File:** `NEXUS_UE5_PROJECT\Content\Python\NexusAI_Interface.py`

```python
import unreal
import requests
import json
from typing import Optional

# Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30

@unreal.uclass()
class NexusAIBlueprintLibrary(unreal.BlueprintFunctionLibrary):
    """
    Blueprint-callable Python functions for Nexus AI
    """
    
    @unreal.ufunction(static=True, meta=dict(Category="Nexus AI"))
    def your_blueprint_function(parameter: str) -> str:
        """
        [Describe what this function does]
        
        This function can be called from any Blueprint:
        1. Add 'Nexus AI' category in Blueprint
        2. Search for 'Your Blueprint Function'
        3. Connect input parameter
        4. Use return value
        
        Args:
            parameter: Input string from Blueprint
            
        Returns:
            Result string to Blueprint
        """
        try:
            # 1. Validate input
            if not parameter:
                unreal.log_warning("Empty parameter provided")
                return "Error: Empty parameter"
            
            # 2. Call API
            response = requests.post(
                f"{API_BASE_URL}/api/your_endpoint",
                json={"required_field": parameter},
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            
            # 3. Parse response
            data = response.json()
            
            # 4. Return result
            return data.get("message", "Success")
            
        except requests.exceptions.Timeout:
            error_msg = "API request timed out"
            unreal.log_error(error_msg)
            return f"Error: {error_msg}"
            
        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to API server"
            unreal.log_error(error_msg)
            return f"Error: {error_msg}"
            
        except Exception as e:
            error_msg = f"Function failed: {str(e)}"
            unreal.log_error(error_msg)
            return f"Error: {error_msg}"
```

### Template 2: Async Task for Long Operations

```python
@unreal.uclass()
class NexusAIAsyncTask(unreal.BlueprintFunctionLibrary):
    """
    Async task that won't block the game thread
    """
    
    @unreal.ufunction(static=True, meta=dict(Category="Nexus AI", Latent=True, LatentInfo="latent_info"))
    def async_ai_request(
        parameter: str,
        latent_info: unreal.LatentActionInfo
    ) -> str:
        """
        Async Blueprint function (shows loading indicator)
        
        Usage in Blueprint:
        1. This node will have a clock icon
        2. Execution continues after request completes
        3. Use for long-running operations
        """
        import threading
        
        result = {"value": ""}
        
        def do_request():
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/your_endpoint",
                    json={"required_field": parameter},
                    timeout=60  # Longer timeout for async
                )
                result["value"] = response.json()["message"]
            except Exception as e:
                result["value"] = f"Error: {str(e)}"
                unreal.log_error(f"Async request failed: {e}")
        
        # Execute in background thread
        thread = threading.Thread(target=do_request)
        thread.start()
        thread.join()  # Wait for completion
        
        return result["value"]
```

### Template 3: Event Dispatcher (Callback System)

```python
@unreal.uclass()
class NexusAIEventSystem(unreal.BlueprintFunctionLibrary):
    """
    Event system for AI response callbacks
    """
    
    # Store callbacks
    _callbacks = {}
    
    @unreal.ufunction(static=True, meta=dict(Category="Nexus AI"))
    def register_response_callback(callback_id: str) -> bool:
        """
        Register a callback to receive AI responses
        
        Usage:
        1. Call this to register
        2. When AI responds, your callback will be triggered
        3. Implement the callback in Blueprint
        """
        try:
            # Store callback reference
            NexusAIEventSystem._callbacks[callback_id] = True
            unreal.log(f"Registered callback: {callback_id}")
            return True
            
        except Exception as e:
            unreal.log_error(f"Failed to register callback: {e}")
            return False
    
    @unreal.ufunction(static=True, meta=dict(Category="Nexus AI"))
    def trigger_response_event(callback_id: str, message: str) -> None:
        """
        Trigger a registered callback with data
        
        Internal use - called when AI response arrives
        """
        if callback_id in NexusAIEventSystem._callbacks:
            # In a real implementation, you'd dispatch to Blueprint event
            unreal.log(f"Triggering callback {callback_id} with: {message}")
            # Blueprint event dispatcher call would go here
```

---

## 🌌 3D ELEMENT CREATION TEMPLATES

### Template 1: Spawn Holographic Display

```python
def create_holographic_display(
    location: unreal.Vector,
    rotation: unreal.Rotator,
    text: str,
    size: float = 1.0
) -> Optional[unreal.Actor]:
    """
    Spawn a holographic text display in 3D space
    
    Args:
        location: World position (X, Y, Z)
        rotation: World rotation (Pitch, Yaw, Roll)
        text: Text to display
        size: Scale multiplier
        
    Returns:
        Spawned actor or None if failed
    """
    try:
        # 1. Get editor world
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            unreal.log_error("Could not get editor world")
            return None
        
        # 2. Load Blueprint class
        blueprint_path = "/Game/Blueprints/BP_HologramDisplay"
        blueprint = unreal.EditorAssetLibrary.load_asset(blueprint_path)
        
        if not blueprint:
            unreal.log_error(f"Could not load blueprint: {blueprint_path}")
            return None
        
        # 3. Spawn actor
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            blueprint.generated_class(),
            location,
            rotation
        )
        
        if not actor:
            unreal.log_error("Failed to spawn actor")
            return None
        
        # 4. Set properties
        actor.set_actor_scale3d(unreal.Vector(size, size, size))
        
        # 5. Call Blueprint function to set text
        # Note: The Blueprint must have a function called "SetDisplayText"
        unreal.BlueprintFunctionLibrary.call_function_by_name(
            actor,
            "SetDisplayText",
            text
        )
        
        unreal.log(f"Created holographic display at {location}")
        return actor
        
    except Exception as e:
        unreal.log_error(f"Error creating holographic display: {e}")
        return None
```

### Template 2: Create Particle Effect

```python
def spawn_particle_effect(
    location: unreal.Vector,
    effect_type: str,
    duration: float = 2.0,
    scale: float = 1.0
) -> Optional[unreal.ParticleSystemComponent]:
    """
    Spawn a particle system effect
    
    Args:
        location: World position
        effect_type: Name of effect ("ai_thinking", "agent_activate", etc.)
        duration: How long effect lasts (seconds)
        scale: Size multiplier
        
    Returns:
        Particle system component or None
    """
    try:
        # 1. Map effect type to particle system asset
        effect_map = {
            "ai_thinking": "/Game/Effects/PS_AIThinking",
            "agent_activate": "/Game/Effects/PS_AgentActivate",
            "data_flow": "/Game/Effects/PS_DataFlow",
            "success": "/Game/Effects/PS_Success",
            "error": "/Game/Effects/PS_Error"
        }
        
        particle_path = effect_map.get(effect_type)
        if not particle_path:
            unreal.log_error(f"Unknown effect type: {effect_type}")
            return None
        
        # 2. Load particle system
        particle_system = unreal.EditorAssetLibrary.load_asset(particle_path)
        if not particle_system:
            unreal.log_error(f"Could not load particle system: {particle_path}")
            return None
        
        # 3. Spawn particle system
        world = unreal.EditorLevelLibrary.get_editor_world()
        component = unreal.GameplayStatics.spawn_emitter_at_location(
            world,
            particle_system,
            location,
            unreal.Rotator(0, 0, 0),
            unreal.Vector(scale, scale, scale),
            True  # Auto destroy
        )
        
        # 4. Set duration
        if component and duration > 0:
            # Component will auto-destroy after duration
            component.set_auto_activate(True)
        
        unreal.log(f"Spawned {effect_type} effect at {location}")
        return component
        
    except Exception as e:
        unreal.log_error(f"Error spawning particle effect: {e}")
        return None
```

### Template 3: Create 3D Agent Avatar

```python
def create_agent_avatar(
    agent_name: str,
    position_index: int
) -> Optional[unreal.Actor]:
    """
    Create a 3D avatar for an AI agent
    
    Args:
        agent_name: Name of agent ("CodeAgent", "MusicAgent", etc.)
        position_index: Position in circular formation (0-7)
        
    Returns:
        Spawned avatar actor or None
    """
    try:
        # 1. Calculate position in circular formation
        import math
        radius = 500.0  # Distance from center
        angle = (position_index / 8.0) * 2 * math.pi
        
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = 100.0  # Height above ground
        
        location = unreal.Vector(x, y, z)
        rotation = unreal.Rotator(0, math.degrees(angle) + 90, 0)
        
        # 2. Map agent to Blueprint
        agent_blueprints = {
            "CodeAgent": "/Game/Agents/BP_CodeAgent",
            "MusicAgent": "/Game/Agents/BP_MusicAgent",
            "ImageAgent": "/Game/Agents/BP_ImageAgent",
            "StoryAgent": "/Game/Agents/BP_StoryAgent",
            "ResearchAgent": "/Game/Agents/BP_ResearchAgent"
        }
        
        blueprint_path = agent_blueprints.get(agent_name)
        if not blueprint_path:
            unreal.log_warning(f"Unknown agent: {agent_name}, using default")
            blueprint_path = "/Game/Agents/BP_DefaultAgent"
        
        # 3. Load and spawn
        blueprint = unreal.EditorAssetLibrary.load_asset(blueprint_path)
        if not blueprint:
            unreal.log_error(f"Could not load agent blueprint: {blueprint_path}")
            return None
        
        world = unreal.EditorLevelLibrary.get_editor_world()
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            blueprint.generated_class(),
            location,
            rotation
        )
        
        if actor:
            # 4. Set agent name tag
            actor.set_actor_label(f"Agent_{agent_name}_{position_index}")
            
            # 5. Play spawn animation
            unreal.BlueprintFunctionLibrary.call_function_by_name(
                actor,
                "PlaySpawnAnimation",
                None
            )
            
            unreal.log(f"Created {agent_name} avatar at position {position_index}")
        
        return actor
        
    except Exception as e:
        unreal.log_error(f"Error creating agent avatar: {e}")
        return None
```

---

## 🤖 AI AGENT INTEGRATION TEMPLATES

### Template 1: Add New AI Agent to API

**File:** `NEXUS_UE5_API.py`

```python
# Add to your agent definitions section

class NewAgentModel(BaseModel):
    """Configuration for new AI agent"""
    name: str = "NewAgent"
    description: str = "Description of what this agent does"
    capabilities: List[str] = ["capability1", "capability2"]
    enabled: bool = True

# Add agent activation endpoint
@app.post("/api/agent/new_agent/activate")
async def activate_new_agent(request: dict):
    """
    Activate the new AI agent
    
    Example:
        POST /api/agent/new_agent/activate
        {
            "task": "Task description",
            "parameters": {"param1": "value1"}
        }
    """
    try:
        # 1. Validate agent is available
        agent_info = NewAgentModel()
        if not agent_info.enabled:
            raise HTTPException(
                status_code=503,
                detail="Agent is currently disabled"
            )
        
        # 2. Extract task and parameters
        task = request.get("task", "")
        parameters = request.get("parameters", {})
        
        # 3. Call your AI implementation
        # This is where you integrate with your actual AI system
        result = await process_with_new_agent(task, parameters)
        
        # 4. Notify all connected interfaces
        await notify_interfaces({
            "event": "agent_activated",
            "agent": "NewAgent",
            "status": "processing"
        })
        
        # 5. Return result
        return {
            "status": "success",
            "agent": "NewAgent",
            "result": result,
            "task": task
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating new agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_with_new_agent(task: str, parameters: dict) -> dict:
    """
    Your actual AI processing logic for this agent
    
    Replace this with your real implementation
    """
    # Example: Call Ollama, OpenAI, or your custom AI
    try:
        # Placeholder implementation
        result = {
            "output": f"Processed: {task}",
            "parameters_used": parameters,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Agent processing error: {e}")
        raise
```

### Template 2: Multi-Agent Coordination

```python
class AgentCoordinator:
    """
    Coordinates multiple AI agents working together
    """
    
    def __init__(self):
        self.active_agents = {}
        self.task_queue = []
    
    async def delegate_task(
        self,
        task: str,
        required_capabilities: List[str]
    ) -> dict:
        """
        Automatically select and delegate to appropriate agent(s)
        
        Args:
            task: Task description
            required_capabilities: What capabilities are needed
            
        Returns:
            Combined results from all agents
        """
        try:
            # 1. Find suitable agents
            suitable_agents = self._find_agents_by_capability(
                required_capabilities
            )
            
            if not suitable_agents:
                return {
                    "status": "error",
                    "message": "No agents available with required capabilities"
                }
            
            # 2. Distribute task among agents
            results = {}
            for agent_name in suitable_agents:
                agent_result = await self._run_agent(agent_name, task)
                results[agent_name] = agent_result
            
            # 3. Combine results
            combined = self._combine_agent_results(results)
            
            return {
                "status": "success",
                "agents_used": suitable_agents,
                "individual_results": results,
                "combined_result": combined
            }
            
        except Exception as e:
            logger.error(f"Agent coordination error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _find_agents_by_capability(
        self,
        required_capabilities: List[str]
    ) -> List[str]:
        """Find all agents that have the required capabilities"""
        # Implement your agent selection logic
        return ["CodeAgent", "ResearchAgent"]  # Example
    
    async def _run_agent(self, agent_name: str, task: str) -> dict:
        """Execute a specific agent"""
        # Implement your agent execution logic
        return {"output": f"{agent_name} result for: {task}"}
    
    def _combine_agent_results(self, results: dict) -> str:
        """Combine multiple agent outputs intelligently"""
        # Implement your result combination logic
        combined = "\n\n".join([
            f"{agent}: {result['output']}"
            for agent, result in results.items()
        ])
        return combined

# Add coordinator instance
agent_coordinator = AgentCoordinator()

# Add endpoint to use coordinator
@app.post("/api/agents/coordinate")
async def coordinate_agents(request: dict):
    """
    Intelligently distribute task among multiple agents
    
    Example:
        POST /api/agents/coordinate
        {
            "task": "Create a web app with music",
            "required_capabilities": ["coding", "music_generation"]
        }
    """
    try:
        task = request.get("task", "")
        capabilities = request.get("required_capabilities", [])
        
        result = await agent_coordinator.delegate_task(task, capabilities)
        
        return result
        
    except Exception as e:
        logger.error(f"Coordination error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🎨 VISUAL EFFECT TEMPLATES

### Template 1: Smooth Camera Movement

```python
def animate_camera_to_position(
    target_location: unreal.Vector,
    target_rotation: unreal.Rotator,
    duration: float = 2.0,
    ease_type: str = "smooth"
) -> bool:
    """
    Smoothly move camera to new position
    
    Args:
        target_location: Destination position
        target_rotation: Destination rotation
        duration: Animation time in seconds
        ease_type: "linear", "smooth", "ease_in", "ease_out"
        
    Returns:
        True if animation started successfully
    """
    try:
        # 1. Get player camera
        player_controller = unreal.GameplayStatics.get_player_controller(
            unreal.EditorLevelLibrary.get_editor_world(),
            0
        )
        
        if not player_controller:
            unreal.log_error("Could not get player controller")
            return False
        
        # 2. Get current camera position
        current_location = player_controller.get_actor_location()
        current_rotation = player_controller.get_control_rotation()
        
        # 3. Create camera animation Blueprint
        # Note: This requires a Blueprint implementation
        # The Blueprint should handle the actual interpolation
        
        # 4. Trigger the animation
        # In Blueprint, use "Set View Target with Blend"
        unreal.log(f"Starting camera animation to {target_location}")
        
        return True
        
    except Exception as e:
        unreal.log_error(f"Camera animation error: {e}")
        return False
```

### Template 2: Progressive Text Reveal

```python
import asyncio
from typing import Callable

class TextAnimator:
    """
    Animate text revealing character by character
    """
    
    @staticmethod
    async def reveal_text(
        full_text: str,
        update_callback: Callable[[str], None],
        char_delay: float = 0.05
    ) -> None:
        """
        Reveal text one character at a time
        
        Args:
            full_text: Complete text to reveal
            update_callback: Function to call with partial text
            char_delay: Delay between characters (seconds)
        """
        try:
            revealed = ""
            for char in full_text:
                revealed += char
                update_callback(revealed)
                await asyncio.sleep(char_delay)
            
        except Exception as e:
            unreal.log_error(f"Text animation error: {e}")

# Usage in API endpoint
@app.post("/api/interface/{interface_id}/animate_text")
async def animate_text_display(interface_id: str, request: dict):
    """
    Display text with animation effect
    
    Example:
        POST /api/interface/ue5_main/animate_text
        {
            "text": "Your AI response here",
            "speed": "normal"
        }
    """
    try:
        text = request.get("text", "")
        speed = request.get("speed", "normal")
        
        # Map speed to delay
        speed_map = {
            "slow": 0.1,
            "normal": 0.05,
            "fast": 0.02
        }
        char_delay = speed_map.get(speed, 0.05)
        
        # Define callback to update display
        def update_display(partial_text: str):
            # Send update to interface
            # In real implementation, you'd send via WebSocket or polling
            pass
        
        # Start animation
        await TextAnimator.reveal_text(text, update_display, char_delay)
        
        return {"status": "complete"}
        
    except Exception as e:
        logger.error(f"Text animation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🔄 COMPLETE FEATURE EXAMPLES

### Example 1: Add "Voice Command" Feature (Complete)

**Step 1: Add API Endpoint**
```python
# In NEXUS_UE5_API.py

class VoiceCommandRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    interface_id: str

@app.post("/api/voice/command")
async def process_voice_command(request: VoiceCommandRequest):
    """
    Process voice command and return AI response
    """
    try:
        # 1. Decode audio
        import base64
        audio_bytes = base64.b64decode(request.audio_data)
        
        # 2. Convert speech to text (placeholder - use your STT service)
        # text = await speech_to_text(audio_bytes)
        text = "example command"  # Replace with actual STT
        
        # 3. Process with AI
        ai_response = await process_ai_message(text)
        
        # 4. Notify interface
        await notify_interface(request.interface_id, {
            "event": "voice_command_processed",
            "transcription": text,
            "response": ai_response
        })
        
        return {
            "status": "success",
            "transcription": text,
            "response": ai_response
        }
        
    except Exception as e:
        logger.error(f"Voice command error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Step 2: Add UE5 Python Function**
```python
# In NexusAI_Interface.py

@unreal.uclass()
class NexusVoiceCommands(unreal.BlueprintFunctionLibrary):
    
    @unreal.ufunction(static=True, meta=dict(Category="Nexus AI|Voice"))
    def send_voice_command(audio_file_path: str) -> str:
        """
        Send voice command to AI
        
        Args:
            audio_file_path: Path to recorded audio file
            
        Returns:
            AI response text
        """
        try:
            import base64
            
            # 1. Read audio file
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
            
            # 2. Encode to base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # 3. Send to API
            response = requests.post(
                f"{API_BASE_URL}/api/voice/command",
                json={
                    "audio_data": audio_base64,
                    "interface_id": "ue5_main"
                },
                timeout=60
            )
            response.raise_for_status()
            
            # 4. Return AI response
            data = response.json()
            return data["response"]
            
        except Exception as e:
            error_msg = f"Voice command failed: {str(e)}"
            unreal.log_error(error_msg)
            return f"Error: {error_msg}"
```

**Step 3: Create Blueprint Microphone Widget** (Pseudocode)
```
Blueprint: BP_VoiceCommandWidget
- Button "Press to Speak"
- On Click:
  1. Start recording audio (UE5 audio capture)
  2. Show "Listening..." indicator
  3. On release: Stop recording
  4. Save audio to temp file
  5. Call Python: NexusVoiceCommands.SendVoiceCommand(file_path)
  6. Display response in holographic display
```

### Example 2: Add "Agent Status Dashboard" (Complete)

**Step 1: Add API Endpoint**
```python
# In NEXUS_UE5_API.py

@app.get("/api/agents/status")
async def get_agents_status():
    """
    Get current status of all AI agents
    """
    try:
        agents_status = {
            "CodeAgent": {
                "active": True,
                "tasks_completed": 42,
                "current_task": "Writing Python script",
                "uptime": "2h 15m"
            },
            "MusicAgent": {
                "active": False,
                "tasks_completed": 15,
                "current_task": None,
                "uptime": "0h 0m"
            },
            # Add other agents...
        }
        
        return {
            "status": "success",
            "agents": agents_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Status retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Step 2: Add UE5 Update Function**
```python
# In NexusAI_Interface.py

@unreal.uclass()
class NexusDashboard(unreal.BlueprintFunctionLibrary):
    
    _dashboard_actors = {}
    
    @unreal.ufunction(static=True, meta=dict(Category="Nexus AI|Dashboard"))
    def update_agent_dashboard() -> bool:
        """
        Update the 3D agent status dashboard
        
        Call this periodically (e.g., every 5 seconds) from Blueprint
        """
        try:
            # 1. Fetch agent status
            response = requests.get(
                f"{API_BASE_URL}/api/agents/status",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            # 2. Update each agent display
            for agent_name, status in data["agents"].items():
                NexusDashboard._update_agent_display(
                    agent_name,
                    status
                )
            
            return True
            
        except Exception as e:
            unreal.log_error(f"Dashboard update failed: {e}")
            return False
    
    @staticmethod
    def _update_agent_display(agent_name: str, status: dict):
        """Update individual agent's 3D display"""
        try:
            # Find or create agent display actor
            actor = NexusDashboard._dashboard_actors.get(agent_name)
            
            if actor and actor.is_valid():
                # Update display with new status
                status_text = f"{agent_name}\n"
                status_text += f"Active: {'Yes' if status['active'] else 'No'}\n"
                status_text += f"Tasks: {status['tasks_completed']}\n"
                
                if status['current_task']:
                    status_text += f"Current: {status['current_task']}"
                
                # Call Blueprint function to update text
                unreal.BlueprintFunctionLibrary.call_function_by_name(
                    actor,
                    "UpdateStatusText",
                    status_text
                )
            
        except Exception as e:
            unreal.log_error(f"Display update error for {agent_name}: {e}")
```

**Step 3: Create Auto-Update Blueprint**
```
Blueprint: BP_DashboardManager
- Event BeginPlay:
  1. Set Timer: Every 5 seconds
     - Call: NexusDashboard.UpdateAgentDashboard()
  2. Create initial dashboard layout
  3. Position agent displays in grid

- On Dashboard Update Success:
  1. Trigger pulse animation on updated displays
  2. Play subtle sound effect
```

---

## 📝 USAGE CHECKLIST

Before using any template:

1. **Copy the entire template** - Don't modify while copying
2. **Replace placeholder names**:
   - `your_endpoint` → actual endpoint name
   - `YourRequestModel` → actual model name
   - `your_function` → actual function name
3. **Update paths** - Verify all file paths are correct
4. **Add your logic** - Replace placeholder comments with real code
5. **Test incrementally** - Test each addition before adding more
6. **Add error handling** - Keep all try/except blocks
7. **Update documentation** - Add docstrings for your specific use case

---

## 🎯 QUICK DECISION TREE

**"Where should I add this feature?"**

```
Is it a new API endpoint?
└─ YES → Use API Endpoint Template in NEXUS_UE5_API.py

Does Blueprint need to call it?
└─ YES → Use Blueprint-Callable Template in NexusAI_Interface.py

Does it create 3D elements?
└─ YES → Use 3D Element Template in NexusAI_Interface.py

Is it a new AI agent?
└─ YES → Use AI Agent Integration Template in NEXUS_UE5_API.py

Does it need visual effects?
└─ YES → Use Visual Effect Template in NexusAI_Interface.py

Is it a complete new feature?
└─ YES → Use Complete Feature Example (combine multiple templates)
```

---

*Remember: Always test in isolation before integrating into the full system!*

**Template Version: 1.0**
**Last Updated: 2025-10-24**
**For: Cline AI Assistant - Nexus AI System**
