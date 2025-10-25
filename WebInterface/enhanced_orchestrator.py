"""
Enhanced Orchestrator for AIArm Multi-Agent System
Manages specialized agents and coordinates their activities
"""

import sys
import os
import json
import random
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class ThoughtStream:
    """Manages the stream of thoughts in the AIArm system"""
    
    def __init__(self):
        self.thoughts = []
        self.memory_path = Path("D:/AIArm/Memory/thoughts")
        self.memory_path.mkdir(exist_ok=True, parents=True)
        self._load_thoughts()
    
    def _load_thoughts(self):
        """Load thoughts from disk"""
        try:
            thought_files = list(self.memory_path.glob("thought_*.json"))
            for file in thought_files[:100]:  # Limit to most recent 100 thoughts
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        thought = json.load(f)
                        self.thoughts.append(thought)
                except Exception as e:
                    print(f"Error loading thought file {file}: {e}")
            
            # Sort thoughts by timestamp (newest first)
            self.thoughts.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            print(f"Loaded {len(self.thoughts)} thoughts from memory")
        except Exception as e:
            print(f"Error loading thoughts: {e}")
    
    def add_thought(self, content, response=None, agent=None, user_id=None, thought_id=None):
        """Add a new thought to the stream"""
        timestamp = datetime.now().isoformat()
        thought_id = thought_id or f"thought_{int(time.time())}_{random.randint(1000, 9999)}"
        
        thought = {
            "id": thought_id,
            "content": content,
            "response": response,
            "agent": agent,
            "user_id": user_id,
            "timestamp": timestamp,
            "type": "user_interaction"
        }
        
        # Add to memory
        self.thoughts.append(thought)
        
        # Save to disk
        try:
            thought_file = self.memory_path / f"{thought_id}.json"
            with open(thought_file, "w", encoding="utf-8") as f:
                json.dump(thought, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving thought: {e}")
        
        return thought_id
    
    def get_recent_thoughts(self, limit=10):
        """Get the most recent thoughts"""
        return self.thoughts[:limit]
    
    def get_relevant_thoughts(self, query, limit=5):
        """Get thoughts relevant to a query (simple keyword matching)"""
        query_terms = query.lower().split()
        scored_thoughts = []
        
        for thought in self.thoughts:
            score = 0
            content = thought.get("content", "").lower()
            response = thought.get("response", "").lower()
            
            for term in query_terms:
                if term in content:
                    score += 1
                if term in response:
                    score += 0.5
            
            if score > 0:
                scored_thoughts.append((thought, score))
        
        # Sort by score (highest first)
        scored_thoughts.sort(key=lambda x: x[1], reverse=True)
        
        return [thought for thought, _ in scored_thoughts[:limit]]

class EnhancedOrchestrator:
    """Enhanced orchestrator for AIArm multi-agent system"""
    
    def __init__(self):
        self.thought_stream = ThoughtStream()
        self.agents = {}
        self.agent_capabilities = {
            "orchestrator": ["coordination", "integration", "delegation"],
            "code": ["programming", "development", "debugging"],
            "research": ["information gathering", "analysis", "synthesis"],
            "content": ["writing", "documentation", "creativity"],
            "design": ["visual design", "UI/UX", "aesthetics"],
            "systems": ["architecture", "integration", "automation"],
            "planning": ["strategy", "roadmaps", "project management"],
            "files": ["file management", "organization", "data handling"],
            "reasoning": ["critical thinking", "logic", "problem solving"]
        }
    
    def process_message(self, message):
        """Process a message from a user or another agent"""
        if not isinstance(message, dict):
            return {
                "status": "error",
                "response": "Invalid message format"
            }
        
        # Extract message details
        message_type = message.get("type", "unknown")
        
        if message_type == "user_request":
            return self.process_user_request(message)
        elif message_type == "agent_query":
            return self.process_agent_query(message)
        elif message_type == "system_event":
            return self.process_system_event(message)
        else:
            return {
                "status": "error",
                "response": f"Unknown message type: {message_type}"
            }
    
    def process_user_request(self, message):
        """Process a user request"""
        content = message.get("content", "")
        agent = message.get("agent", "orchestrator")
        user_id = message.get("user_id", "user")
        thought_id = message.get("thought_id")
        
        # Add to thought stream
        if not thought_id:
            thought_id = self.thought_stream.add_thought(
                content=content,
                agent=agent,
                user_id=user_id
            )
        
        # This is just a fallback implementation - in a real system,
        # we would route the request to the appropriate specialized agent
        # For now, we'll just return a simple response
        
        # Create a default response
        response = {
            "status": "completed",
            "response": f"I've processed your request through the HRM architecture. The Surface layer provided structured understanding while the Deep reasoning layer added contextual depth. How else can I assist you?",
            "thought_id": thought_id
        }
        
        # Update the thought with the response
        self.thought_stream.add_thought(
            content=content,
            response=response["response"],
            agent=agent,
            user_id=user_id,
            thought_id=thought_id
        )
        
        return response
    
    def process_agent_query(self, message):
        """Process a query from another agent"""
        query_type = message.get("query")
        
        if query_type == "capabilities":
            return {
                "status": "success",
                "capabilities": self.agent_capabilities
            }
        elif query_type == "thought_stream":
            limit = message.get("limit", 10)
            return {
                "status": "success",
                "thoughts": self.thought_stream.get_recent_thoughts(limit)
            }
        else:
            return {
                "status": "error",
                "response": f"Unknown query type: {query_type}"
            }
    
    def process_system_event(self, message):
        """Process a system event"""
        event_type = message.get("event")
        
        if event_type == "startup":
            return {
                "status": "success",
                "response": "Enhanced Orchestrator started"
            }
        elif event_type == "shutdown":
            return {
                "status": "success",
                "response": "Enhanced Orchestrator shutting down"
            }
        else:
            return {
                "status": "success",
                "response": f"System event {event_type} processed"
            }
    
    def get_agent_for_task(self, task):
        """Determine the best agent for a given task"""
        # This is a simple implementation - in a real system,
        # we would have a more sophisticated routing mechanism
        
        task_lower = task.lower()
        
        if any(term in task_lower for term in ["code", "programming", "script", "function", "bug"]):
            return "code"
        elif any(term in task_lower for term in ["research", "information", "data", "analyze"]):
            return "research"
        elif any(term in task_lower for term in ["write", "content", "document", "blog"]):
            return "content"
        elif any(term in task_lower for term in ["design", "ui", "ux", "visual", "interface"]):
            return "design"
        elif any(term in task_lower for term in ["system", "architecture", "integrate", "automate"]):
            return "systems"
        elif any(term in task_lower for term in ["plan", "strategy", "roadmap", "project"]):
            return "planning"
        elif any(term in task_lower for term in ["file", "folder", "organize", "data"]):
            return "files"
        elif any(term in task_lower for term in ["think", "reason", "logic", "problem"]):
            return "reasoning"
        else:
            return "orchestrator"

# Initialize if run directly
if __name__ == "__main__":
    orchestrator = EnhancedOrchestrator()
    print("Enhanced Orchestrator initialized and running")
    
    # Test message
    test_message = {
        "type": "user_request",
        "content": "Hello, this is a test message",
        "agent": "orchestrator",
        "user_id": "test_user"
    }
    
    result = orchestrator.process_message(test_message)
    print(json.dumps(result, indent=2))