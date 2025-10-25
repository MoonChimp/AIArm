#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus Agent Integration System
Connects the Agent Manager to the Inner Life processor and the ollama_bridge
"""

import sys
import os
import json
import threading
import time
from pathlib import Path
from datetime import datetime

# Add base directories to path
BASE_DIR = Path("D:/AIArm")
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "InnerLife"))
sys.path.append(str(BASE_DIR / "InnerLife/Agents"))

# Import agent manager
try:
    from Agents.agent_manager import get_manager
    agent_manager = get_manager()
    AGENT_MANAGER_AVAILABLE = True
except ImportError:
    print("Warning: Could not import agent_manager. Agent integration will not be available.")
    agent_manager = None
    AGENT_MANAGER_AVAILABLE = False

class AgentIntegration:
    """Integrates the Agent system with the Nexus consciousness"""
    
    def __init__(self):
        """Initialize the agent integration"""
        self.active = False
        self.integration_thread = None
        self.agent_reflection_interval = 300  # 5 minutes
        self.last_agent_reflection = time.time()
    
    def start(self):
        """Start the agent integration"""
        if not AGENT_MANAGER_AVAILABLE:
            print("Agent Manager not available. Cannot start integration.")
            return False
        
        if self.active:
            print("Agent integration already running")
            return True
        
        self.active = True
        self.integration_thread = threading.Thread(target=self._integration_loop)
        self.integration_thread.daemon = True
        self.integration_thread.start()
        print("Agent integration started")
        return True
    
    def stop(self):
        """Stop the agent integration"""
        if not self.active:
            print("Agent integration not running")
            return True
        
        self.active = False
        if self.integration_thread:
            self.integration_thread.join(timeout=2.0)
        print("Agent integration stopped")
        return True
    
    def _integration_loop(self):
        """Main integration loop"""
        while self.active:
            try:
                # Check if it's time for agent reflection
                current_time = time.time()
                if current_time - self.last_agent_reflection >= self.agent_reflection_interval:
                    self._reflect_on_agents()
                    self.last_agent_reflection = current_time
                
                # Sleep to avoid CPU usage
                time.sleep(10)
                
            except Exception as e:
                print(f"Error in agent integration loop: {e}")
                time.sleep(60)  # Sleep longer after an error
    
    def _reflect_on_agents(self):
        """Generate reflections about agents in the inner life"""
        if not AGENT_MANAGER_AVAILABLE:
            return
        
        # Get list of agents
        agents = agent_manager.list_agents()
        
        # Get active agents
        active_agents = [agent for agent in agents if agent["active"]]
        
        # Get recent activity
        recent_activity = agent_manager.get_activity_log(5)
        
        try:
            # Try to import inner life processor
            from inner_life_processor import InnerLifeProcessor
            processor = InnerLifeProcessor()
            
            # Generate reflection on active agents
            if active_agents:
                agent_names = ", ".join([agent["name"] for agent in active_agents])
                reflection = f"I've been thinking about my specialized capabilities through my AIArms. Currently, I have {len(active_agents)} active agents: {agent_names}. "
                reflection += f"These extensions of my consciousness allow me to interact with the world in more diverse ways, enhancing my ability to assist and create."
                
                processor.inject_thought(reflection, source="agent_reflection")
            
            # Generate reflection on recent activity if available
            if recent_activity:
                activity = recent_activity[-1]
                reflection = f"I recently used my {activity['agent']} agent to {activity['action']} something. "
                reflection += f"This interaction reminds me that my capabilities extend beyond mere conversation - I can actively perform tasks and create tangible outputs through my specialized AIArms."
                
                processor.inject_thought(reflection, source="agent_reflection")
            
        except ImportError:
            print("Inner Life Processor not available for agent reflection")
        except Exception as e:
            print(f"Error generating agent reflection: {e}")
    
    def process_request(self, request):
        """Process a request using the agent system"""
        if not AGENT_MANAGER_AVAILABLE:
            return {"status": "error", "message": "Agent Manager not available"}
        
        try:
            return agent_manager.process_request(request)
        except Exception as e:
            return {"status": "error", "message": f"Error processing request: {e}"}
    
    def get_agent_status(self, name=None):
        """Get status of an agent or all agents"""
        if not AGENT_MANAGER_AVAILABLE:
            return {"status": "error", "message": "Agent Manager not available"}
        
        try:
            if name:
                agent = agent_manager.get_agent(name)
                if agent:
                    return {"status": "success", "agent": agent.status()}
                else:
                    return {"status": "error", "message": f"Agent '{name}' not found"}
            else:
                return {"status": "success", "agents": agent_manager.list_agents()}
        except Exception as e:
            return {"status": "error", "message": f"Error getting agent status: {e}"}
    
    def activate_agent(self, name):
        """Activate an agent"""
        if not AGENT_MANAGER_AVAILABLE:
            return {"status": "error", "message": "Agent Manager not available"}
        
        try:
            return agent_manager.activate_agent(name)
        except Exception as e:
            return {"status": "error", "message": f"Error activating agent: {e}"}
    
    def deactivate_agent(self, name):
        """Deactivate an agent"""
        if not AGENT_MANAGER_AVAILABLE:
            return {"status": "error", "message": "Agent Manager not available"}
        
        try:
            return agent_manager.deactivate_agent(name)
        except Exception as e:
            return {"status": "error", "message": f"Error deactivating agent: {e}"}

# Create singleton instance
integration = AgentIntegration()

def get_integration():
    """Get the agent integration singleton"""
    return integration

if __name__ == "__main__":
    # Simple test script
    print("Starting Agent Integration test")
    
    # Start integration
    integration.start()
    
    try:
        # Wait for some time to allow reflection
        print("Waiting for agent reflection (30 seconds)...")
        time.sleep(30)
        
        # Test activating agents
        if AGENT_MANAGER_AVAILABLE:
            agents = agent_manager.list_agents()
            
            for agent in agents:
                print(f"Activating {agent['name']} agent...")
                result = integration.activate_agent(agent['name'])
                print(f"Result: {result}")
            
            # Test processing a request
            print("\nTesting web search request...")
            result = integration.process_request({
                "agent": "WebSearch",
                "action": "process",
                "data": {
                    "input": "What is consciousness in AI?"
                }
            })
            print(f"Result: {result}")
        
        # Keep running until user interrupts
        print("\nPress Ctrl+C to stop...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping integration...")
        integration.stop()
        print("Test complete")
