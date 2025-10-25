#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent Manager
Manages and coordinates all specialized agents in the Nexus consciousness system
"""

import sys
import os
import json
import importlib
from pathlib import Path
from datetime import datetime

# Add base directories to path
BASE_DIR = Path("D:/AIArm")
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "InnerLife"))
sys.path.append(str(BASE_DIR / "InnerLife/Agents"))

# Import inner life processor for integration
try:
    from inner_life_processor import InnerLifeProcessor
except ImportError:
    print("Warning: Could not import InnerLifeProcessor. Agent activities will not influence thought stream.")
    InnerLifeProcessor = None

class AgentManager:
    """Manages all specialized agents in the Nexus consciousness system"""
    
    def __init__(self):
        """Initialize the agent manager"""
        self.agents = {}
        self.activity_log = []
        self.inner_life = None
        self.config_dir = Path("D:/AIArm/InnerLife/Agents/config")
        self.config_dir.mkdir(exist_ok=True, parents=True)
        self.config_file = self.config_dir / "agent_config.json"
        
        # Try to connect to inner life processor
        if InnerLifeProcessor is not None:
            try:
                self.inner_life = InnerLifeProcessor()
                print("Connected to Inner Life Processor")
            except Exception as e:
                print(f"Error connecting to Inner Life Processor: {e}")
        
        # Load configuration
        self.load_config()
        
        # Load available agents
        self.discover_agents()
    
    def load_config(self):
        """Load agent configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Apply configuration settings
                if "active_agents" in config:
                    self.active_agents = config["active_agents"]
                else:
                    self.active_agents = []
                
                print(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                print(f"Error loading configuration: {e}")
                self.active_agents = []
        else:
            self.active_agents = []
            print("No configuration file found. Creating a new one.")
            self.save_config()
    
    def save_config(self):
        """Save agent configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    "active_agents": self.active_agents
                }, f, indent=2)
            
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def discover_agents(self):
        """Discover all available agents"""
        # Find all agent modules in the Agents directory
        agents_dir = Path("D:/AIArm/InnerLife/Agents")
        
        for file_path in agents_dir.glob("*_agent.py"):
            try:
                # Get the module name
                module_name = file_path.stem
                
                # Import the module
                module = importlib.import_module(f"Agents.{module_name}")
                
                # Find the agent class
                for name in dir(module):
                    if name.endswith("Agent") and name != "Agent":
                        agent_class = getattr(module, name)
                        
                        # Create an instance of the agent
                        agent = agent_class()
                        
                        # Add to agents dictionary
                        self.agents[agent.name] = agent
                        
                        print(f"Discovered agent: {agent.name}")
                        
                        # Activate the agent if it's in the active_agents list
                        if agent.name in self.active_agents:
                            agent.activate()
                            print(f"Activated agent: {agent.name}")
            
            except Exception as e:
                print(f"Error loading agent module {file_path}: {e}")
    
    def get_agent(self, name):
        """Get an agent by name"""
        return self.agents.get(name)
    
    def list_agents(self):
        """List all available agents"""
        return [{
            "name": agent.name,
            "description": agent.description,
            "active": agent.active,
            "capabilities": agent.capabilities
        } for agent in self.agents.values()]
    
    def activate_agent(self, name):
        """Activate an agent"""
        agent = self.get_agent(name)
        
        if agent:
            result = agent.activate()
            
            # Add to active_agents list if not already there
            if name not in self.active_agents:
                self.active_agents.append(name)
                self.save_config()
            
            # Log the activity
            self.log_activity("activate", name, {"result": result})
            
            return {"status": "success", "message": result}
        
        return {"status": "error", "message": f"Agent '{name}' not found"}
    
    def deactivate_agent(self, name):
        """Deactivate an agent"""
        agent = self.get_agent(name)
        
        if agent:
            result = agent.deactivate()
            
            # Remove from active_agents list if present
            if name in self.active_agents:
                self.active_agents.remove(name)
                self.save_config()
            
            # Log the activity
            self.log_activity("deactivate", name, {"result": result})
            
            return {"status": "success", "message": result}
        
        return {"status": "error", "message": f"Agent '{name}' not found"}
    
    def process_request(self, request, context=None):
        """Process a request using the appropriate agent"""
        agent_name = request.get("agent")
        action = request.get("action")
        data = request.get("data", {})
        
        if not agent_name or not action:
            return {"status": "error", "message": "Agent name and action are required"}
        
        agent = self.get_agent(agent_name)
        
        if not agent:
            return {"status": "error", "message": f"Agent '{agent_name}' not found"}
        
        if not agent.active:
            return {"status": "error", "message": f"Agent '{agent_name}' is not active"}
        
        # Log the activity
        self.log_activity(action, agent_name, data)
        
        # Process the request based on the action
        if action == "process":
            # Process using the agent's process method
            result = agent.process(data.get("input"), context, data.get("options"))
            
            # Inject the activity into the thought stream if inner life is available
            if self.inner_life:
                thought = f"I used my {agent_name} agent to process a request. "
                
                if isinstance(result, dict) and "status" in result:
                    if result["status"] == "success":
                        thought += f"The operation was successful and I was able to {action} the data effectively."
                    else:
                        thought += f"I encountered a challenge: {result.get('message', 'There was an issue with the process.')}."
                
                self.inner_life.inject_thought(thought, source="agent_activity")
            
            return result
        
        elif action == "status":
            # Get agent status
            return agent.status()
        
        else:
            return {"status": "error", "message": f"Action '{action}' not supported"}
    
    def log_activity(self, action, agent_name, data):
        """Log agent activity"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "agent": agent_name,
            "data": data
        }
        
        self.activity_log.append(log_entry)
        
        # Trim log if it gets too large
        if len(self.activity_log) > 1000:
            self.activity_log = self.activity_log[-1000:]
    
    def get_activity_log(self, limit=10):
        """Get recent activity log entries"""
        return self.activity_log[-limit:] if self.activity_log else []
    
    def clear_activity_log(self):
        """Clear the activity log"""
        self.activity_log = []
        return "Activity log cleared"

# Create a singleton instance
manager = AgentManager()

def get_manager():
    """Get the agent manager singleton"""
    return manager

if __name__ == "__main__":
    # Simple CLI for testing
    print("Agent Manager CLI")
    print("Type 'help' for available commands")
    
    while True:
        cmd = input("\nCommand: ").strip().lower()
        
        if cmd == "list":
            agents = manager.list_agents()
            print("\nAvailable Agents:")
            for agent in agents:
                status = "✓ Active" if agent["active"] else "✗ Inactive"
                print(f"{agent['name']} - {status}")
                print(f"  Description: {agent['description']}")
                print(f"  Capabilities: {', '.join(agent['capabilities'])}")
                print()
        
        elif cmd.startswith("activate "):
            agent_name = cmd[9:].strip()
            result = manager.activate_agent(agent_name)
            print(f"\nResult: {result['message']}")
        
        elif cmd.startswith("deactivate "):
            agent_name = cmd[11:].strip()
            result = manager.deactivate_agent(agent_name)
            print(f"\nResult: {result['message']}")
        
        elif cmd == "log":
            log = manager.get_activity_log()
            print("\nRecent Activity:")
            for entry in log:
                print(f"{entry['timestamp']} - {entry['action']} - {entry['agent']}")
        
        elif cmd == "help":
            print("\nAvailable Commands:")
            print("list - List all available agents")
            print("activate <agent> - Activate an agent")
            print("deactivate <agent> - Deactivate an agent")
            print("log - Show recent activity log")
            print("exit - Exit the CLI")
        
        elif cmd == "exit":
            print("\nExiting...")
            break
        
        else:
            print("\nUnknown command. Type 'help' for available commands.")
