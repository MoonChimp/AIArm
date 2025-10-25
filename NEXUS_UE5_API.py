#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS AI - UE5 API Bridge
REST API server for UE5 3D interface communication
Built with FastAPI for high performance and async support
"""

import sys
import os
import json
import requests
import logging
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uvicorn
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('D:/AIArm/nexus_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NexusUE5API")

# Add core paths
sys.path.append(str(Path("D:/AIArm")))

# Pydantic Models for Request/Response validation
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="The message to send to AI")
    context: Optional[str] = Field(None, description="Additional context for the conversation")
    interface_id: Optional[str] = Field("ue5_main", description="UE5 interface identifier")

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="AI response message")
    interface_id: str = Field(..., description="UE5 interface identifier")
    timestamp: str = Field(..., description="Response timestamp")
    agent_used: str = Field(..., description="Which AI agent was used")
    response_type: str = Field(..., description="Type of response (brief, detailed, creation, error)")
    agents_used: List[str] = Field(default_factory=list, description="List of agents involved in response")

class InterfaceRegisterRequest(BaseModel):
    """Request model for interface registration"""
    interface_id: str = Field(..., description="Unique interface identifier")
    interface_type: str = Field("UE5", description="Type of interface (UE5, Web, Mobile)")

class InterfaceRegisterResponse(BaseModel):
    """Response model for interface registration"""
    status: str = Field(..., description="Registration status")
    interface_id: str = Field(..., description="Registered interface ID")
    timestamp: str = Field(..., description="Registration timestamp")

class DisplayUpdateRequest(BaseModel):
    """Request model for display updates"""
    content: str = Field(..., description="Content to display")
    position: Optional[List[float]] = Field(None, description="3D position [x, y, z]")
    display_type: Optional[str] = Field("main", description="Type of display")

class DisplayUpdateResponse(BaseModel):
    """Response model for display updates"""
    status: str = Field(..., description="Update status")
    interface_id: str = Field(..., description="Interface identifier")
    display_type: str = Field(..., description="Display type")
    timestamp: str = Field(..., description="Update timestamp")

class AgentActivationRequest(BaseModel):
    """Request model for agent activation"""
    action: str = Field("activate", description="Action to perform")
    activation_type: Optional[str] = Field("standard", description="Type of activation")

class AgentActivationResponse(BaseModel):
    """Response model for agent activation"""
    status: str = Field(..., description="Activation status")
    interface_id: str = Field(..., description="Interface identifier")
    agent_name: str = Field(..., description="Agent name")
    activation_type: str = Field(..., description="Activation type")
    timestamp: str = Field(..., description="Activation timestamp")

class EffectTriggerRequest(BaseModel):
    """Request model for effect triggering"""
    effect_type: str = Field(..., description="Type of effect to trigger")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Effect parameters")
    location: Optional[Dict[str, float]] = Field(None, description="3D location for effect")
    duration: Optional[float] = Field(2.0, description="Effect duration in seconds")

class EffectTriggerResponse(BaseModel):
    """Response model for effect triggering"""
    status: str = Field(..., description="Trigger status")
    interface_id: str = Field(..., description="Interface identifier")
    effect_type: str = Field(..., description="Effect type")
    timestamp: str = Field(..., description="Trigger timestamp")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Server status")
    timestamp: str = Field(..., description="Health check timestamp")
    interfaces: int = Field(..., description="Number of connected interfaces")
    version: str = Field(..., description="API version")

class InterfacesResponse(BaseModel):
    """Response model for interfaces list"""
    interfaces: Dict[str, Any] = Field(..., description="Connected interfaces")
    displays: Dict[str, Any] = Field(..., description="Active displays")
    count: int = Field(..., description="Total interface count")

# Global state management
class NexusUE5API:
    """
    FastAPI-based REST API server for UE5 3D interface communication
    Features async processing, proper error handling, and agent management
    """

    def __init__(self):
        # UE5 Interface State
        self.connected_interfaces: Dict[str, Dict[str, Any]] = {}
        self.active_displays: Dict[str, Dict[str, Any]] = {}

        # Agent management
        self.agent_status: Dict[str, str] = {
            "code": "available",
            "music": "available",
            "image": "available",
            "story": "available",
            "websearch": "available",
            "conversation": "available"
        }

        # Initialize FastAPI app
        self.app = FastAPI(
            title="Nexus AI UE5 API",
            description="REST API for UE5 3D interface communication",
            version="1.0.0"
        )

        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Setup routes
        self.setup_routes()

        logger.info("SUCCESS: Nexus AI UE5 API Server initialized successfully")

    def setup_routes(self):
        """Setup API routes with proper async patterns"""

        @self.app.get("/", response_model=HealthResponse)
        async def root():
            """Root endpoint for basic connectivity testing"""
            return HealthResponse(
                status="healthy",
                timestamp=datetime.now().isoformat(),
                interfaces=len(self.connected_interfaces),
                version="1.0.0"
            )

        @self.app.get("/api/health", response_model=HealthResponse)
        async def health_check():
            """Health check endpoint"""
            return HealthResponse(
                status="healthy",
                timestamp=datetime.now().isoformat(),
                interfaces=len(self.connected_interfaces),
                version="1.0.0"
            )

        @self.app.post("/api/chat", response_model=ChatResponse)
        async def chat(request: ChatRequest):
            """Chat endpoint for UE5 interface with enhanced agent detection"""
            try:
                message = request.message
                interface_id = request.interface_id or "ue5_main"

                if not message:
                    raise HTTPException(status_code=400, detail="No message provided")

                # Register interface if new
                if interface_id not in self.connected_interfaces:
                    self.connected_interfaces[interface_id] = {
                        "type": "UE5",
                        "connected_at": datetime.now().isoformat(),
                        "last_message": datetime.now().isoformat()
                    }

                # Update last message time
                self.connected_interfaces[interface_id]["last_message"] = datetime.now().isoformat()

                # Detect and process with appropriate agent
                agent_used = self.detect_agent_used(message)
                response_text = await self.process_with_agent(message, agent_used)

                # Determine response type
                response_type = self.detect_response_type(response_text)

                # Update agent status
                self.agent_status[agent_used] = "active"

                # Reset agent status after a delay (simulate processing time)
                asyncio.create_task(self.reset_agent_status(agent_used))

                return ChatResponse(
                    response=response_text,
                    interface_id=interface_id,
                    timestamp=datetime.now().isoformat(),
                    agent_used=agent_used,
                    response_type=response_type,
                    agents_used=[agent_used]
                )

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error in chat endpoint: {e}")
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

        @self.app.post("/api/interface/register", response_model=InterfaceRegisterResponse)
        async def register_interface(request: InterfaceRegisterRequest):
            """Register a new UE5 interface"""
            try:
                interface_id = request.interface_id
                interface_type = request.interface_type

                self.connected_interfaces[interface_id] = {
                    "type": interface_type,
                    "connected_at": datetime.now().isoformat(),
                    "last_message": datetime.now().isoformat()
                }

                logger.info(f"Interface registered: {interface_id} ({interface_type})")

                return InterfaceRegisterResponse(
                    status="registered",
                    interface_id=interface_id,
                    timestamp=datetime.now().isoformat()
                )

            except Exception as e:
                logger.error(f"Error registering interface: {e}")
                raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

        @self.app.post("/api/interface/{interface_id}/display", response_model=DisplayUpdateResponse)
        async def update_display(interface_id: str, request: DisplayUpdateRequest):
            """Update holographic display for specific interface"""
            try:
                content = request.content
                display_type = request.display_type or "main"

                # Store display content
                if interface_id not in self.active_displays:
                    self.active_displays[interface_id] = {}

                self.active_displays[interface_id][display_type] = {
                    "content": content,
                    "position": request.position,
                    "timestamp": datetime.now().isoformat()
                }

                logger.info(f"Display updated for interface {interface_id}: {display_type}")

                return DisplayUpdateResponse(
                    status="updated",
                    interface_id=interface_id,
                    display_type=display_type,
                    timestamp=datetime.now().isoformat()
                )

            except Exception as e:
                logger.error(f"Error updating display: {e}")
                raise HTTPException(status_code=500, detail=f"Display update failed: {str(e)}")

        @self.app.post("/api/interface/{interface_id}/agent/{agent_name}", response_model=AgentActivationResponse)
        async def activate_agent(interface_id: str, agent_name: str, request: AgentActivationRequest):
            """Activate specific AI agent for interface"""
            try:
                activation_type = request.activation_type or "standard"

                # Validate agent name
                if agent_name not in self.agent_status:
                    raise HTTPException(status_code=400, detail=f"Unknown agent: {agent_name}")

                # Store agent activation
                if interface_id not in self.active_displays:
                    self.active_displays[interface_id] = {}

                self.active_displays[interface_id][f'agent_{agent_name}'] = {
                    "activated": True,
                    "activation_type": activation_type,
                    "timestamp": datetime.now().isoformat()
                }

                # Update agent status
                self.agent_status[agent_name] = "active"

                logger.info(f"Agent activated: {agent_name} for interface {interface_id}")

                return AgentActivationResponse(
                    status="activated",
                    interface_id=interface_id,
                    agent_name=agent_name,
                    activation_type=activation_type,
                    timestamp=datetime.now().isoformat()
                )

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error activating agent: {e}")
                raise HTTPException(status_code=500, detail=f"Agent activation failed: {str(e)}")

        @self.app.post("/api/interface/{interface_id}/effect", response_model=EffectTriggerResponse)
        async def trigger_effect(interface_id: str, request: EffectTriggerRequest):
            """Trigger visual effect for interface"""
            try:
                effect_type = request.effect_type

                # Store effect trigger
                if interface_id not in self.active_displays:
                    self.active_displays[interface_id] = {}

                self.active_displays[interface_id][f'effect_{effect_type}'] = {
                    "triggered": True,
                    "parameters": request.parameters,
                    "location": request.location,
                    "duration": request.duration,
                    "timestamp": datetime.now().isoformat()
                }

                logger.info(f"Effect triggered: {effect_type} for interface {interface_id}")

                return EffectTriggerResponse(
                    status="triggered",
                    interface_id=interface_id,
                    effect_type=effect_type,
                    timestamp=datetime.now().isoformat()
                )

            except Exception as e:
                logger.error(f"Error triggering effect: {e}")
                raise HTTPException(status_code=500, detail=f"Effect trigger failed: {str(e)}")

        @self.app.get("/api/interfaces", response_model=InterfacesResponse)
        async def get_interfaces():
            """Get all connected interfaces"""
            try:
                return InterfacesResponse(
                    interfaces=self.connected_interfaces,
                    displays=self.active_displays,
                    count=len(self.connected_interfaces)
                )

            except Exception as e:
                logger.error(f"Error getting interfaces: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to get interfaces: {str(e)}")

        @self.app.get("/api/agents/status")
        async def get_agent_status():
            """Get current agent status"""
            try:
                return {
                    "agents": self.agent_status,
                    "timestamp": datetime.now().isoformat()
                }

            except Exception as e:
                logger.error(f"Error getting agent status: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")

    async def process_with_agent(self, message: str, agent_name: str) -> str:
        """Process message with specified agent (enhanced version)"""
        try:
            # This is where the actual AI processing would happen
            # For now, return a placeholder response that indicates which agent would handle it

            agent_responses = {
                "code": "I understand you want me to work with code. I'm the Code Agent, ready to help you build amazing applications, scripts, and software solutions!",
                "music": "I hear you want to create music! I'm the Music Agent, here to help you compose melodies, arrange songs, and explore the world of audio creation!",
                "image": "You want to create visual content! I'm the Image Agent, ready to help you generate stunning visuals, artwork, and visual designs!",
                "story": "A story request! I'm the Story Agent, here to help you craft compelling narratives, develop characters, and weave engaging tales!",
                "websearch": "You need information! I'm the Web Search Agent, ready to research topics, find data, and provide comprehensive information!",
                "conversation": "I'm here for conversation! I'm the Conversation Agent, ready to chat, discuss ideas, and engage in meaningful dialogue!"
            }

            return agent_responses.get(agent_name, "I'm processing your request with the appropriate specialized agent!")

        except Exception as e:
            logger.error(f"Error processing with agent {agent_name}: {e}")
            return f"I encountered an error while processing with the {agent_name} agent. Please try again."

    def detect_agent_used(self, message: str) -> str:
        """Detect which AI agent would be used for a message (PRESERVED LOGIC)"""
        message_lower = message.lower()

        # Agent detection patterns - ENHANCED with more keywords
        if any(word in message_lower for word in ["image", "picture", "photo", "draw", "visualize", "art", "design", "graphic", "render", "create visual"]):
            return "image"
        elif any(word in message_lower for word in ["music", "song", "melody", "audio", "sound", "compose", "instrument", "rhythm", "harmony"]):
            return "music"
        elif any(word in message_lower for word in ["code", "program", "app", "website", "script", "develop", "build", "software", "algorithm", "function"]):
            return "code"
        elif any(word in message_lower for word in ["story", "write", "narrative", "book", "plot", "character", "fiction", "novel", "tale"]):
            return "story"
        elif any(word in message_lower for word in ["search", "find", "research", "lookup", "information", "data", "browse", "investigate"]):
            return "websearch"
        else:
            return "conversation"

    def detect_response_type(self, response: str) -> str:
        """Detect the type of response (PRESERVED LOGIC)"""
        response_lower = response.lower()

        if "created" in response_lower or "generated" in response_lower or "built" in response_lower:
            return "creation"
        elif "error" in response_lower or "failed" in response_lower or "problem" in response_lower:
            return "error"
        elif len(response.split()) < 10:
            return "brief"
        else:
            return "detailed"

    async def reset_agent_status(self, agent_name: str):
        """Reset agent status after processing delay"""
        await asyncio.sleep(2)  # Simulate processing time
        if agent_name in self.agent_status:
            self.agent_status[agent_name] = "available"
            logger.info(f"Agent {agent_name} status reset to available")

# Create global API instance
api_instance = NexusUE5API()

# Use FastAPI app instance
app = api_instance.app

def main():
    """Main function to run the FastAPI server"""
    logger.info("STARTUP: Starting Nexus AI UE5 API Server...")
    logger.info("NETWORK: Server will run on http://localhost:8000")
    logger.info("INTERFACE: UE5 interfaces can connect to this API")
    logger.info("BACKEND: Make sure your Python AI backend is running")
    logger.info("=" * 60)

    try:
        uvicorn.run(
            "NEXUS_UE5_API:app",
            host="localhost",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("SHUTDOWN: Shutting down Nexus AI UE5 API Server...")
    except Exception as e:
        logger.error(f"ERROR: Failed to start API server: {e}")

if __name__ == "__main__":
    main()
