#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusAI Memory System
Provides conversation memory, context retention, and learning capabilities
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib


class ConversationMemory:
    """Manages conversation history and context for each session"""
    
    def __init__(self, memory_dir: str = "D:/AIArm/NexusAI_Commercial/memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.sessions = {}  # Active sessions in memory
        self.max_context_messages = 20  # Keep last 20 messages for context
        
    def create_session(self, session_id: str = None) -> str:
        """Create a new conversation session"""
        if not session_id:
            session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]
        
        self.sessions[session_id] = {
            "id": session_id,
            "created": datetime.now().isoformat(),
            "messages": [],
            "metadata": {
                "total_interactions": 0,
                "topics_discussed": [],
                "user_preferences": {}
            }
        }
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Dict = None):
        """Add a message to the conversation history"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        message = {
            "role": role,  # 'user' or 'assistant'
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.sessions[session_id]["messages"].append(message)
        self.sessions[session_id]["metadata"]["total_interactions"] += 1
        
        # Auto-save every 5 messages
        if len(self.sessions[session_id]["messages"]) % 5 == 0:
            self.save_session(session_id)
    
    def get_context(self, session_id: str, max_messages: int = None) -> List[Dict]:
        """Get recent conversation context for LLM"""
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]["messages"]
        limit = max_messages or self.max_context_messages
        
        # Return recent messages in Ollama format
        context = []
        for msg in messages[-limit:]:
            context.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return context
    
    def get_conversation_summary(self, session_id: str) -> str:
        """Generate a summary of the conversation so far"""
        if session_id not in self.sessions:
            return "New conversation"
        
        session = self.sessions[session_id]
        msg_count = len(session["messages"])
        
        if msg_count == 0:
            return "New conversation"
        
        # Extract key topics from recent messages
        recent = session["messages"][-5:]
        topics = []
        for msg in recent:
            if msg["role"] == "user":
                # Simple keyword extraction
                words = msg["content"].lower().split()
                topics.extend([w for w in words if len(w) > 5])
        
        unique_topics = list(set(topics))[:5]
        
        summary = f"Conversation with {msg_count} messages"
        if unique_topics:
            summary += f" discussing: {', '.join(unique_topics)}"
        
        return summary
    
    def save_session(self, session_id: str):
        """Save session to disk"""
        if session_id not in self.sessions:
            return False
        
        filepath = self.memory_dir / f"{session_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.sessions[session_id], f, indent=2, ensure_ascii=False)
        
        return True
    
    def load_session(self, session_id: str) -> bool:
        """Load session from disk"""
        filepath = self.memory_dir / f"{session_id}.json"
        
        if not filepath.exists():
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            self.sessions[session_id] = json.load(f)
        
        return True
    
    def list_sessions(self) -> List[Dict]:
        """List all saved sessions"""
        sessions = []
        for filepath in self.memory_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        "id": data["id"],
                        "created": data["created"],
                        "message_count": len(data["messages"])
                    })
            except:
                pass
        
        return sorted(sessions, key=lambda x: x["created"], reverse=True)
    
    def clear_session(self, session_id: str):
        """Clear a session from memory"""
        if session_id in self.sessions:
            del self.sessions[session_id]


class LearningSystem:
    """Implements learning and adaptation capabilities"""
    
    def __init__(self, learning_dir: str = "D:/AIArm/NexusAI_Commercial/learning"):
        self.learning_dir = Path(learning_dir)
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_base = self.load_knowledge()
        
    def load_knowledge(self) -> Dict:
        """Load accumulated knowledge"""
        kb_file = self.learning_dir / "knowledge_base.json"
        
        if kb_file.exists():
            with open(kb_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "user_preferences": {},
            "learned_facts": [],
            "corrections": [],
            "successful_patterns": [],
            "areas_to_improve": []
        }
    
    def save_knowledge(self):
        """Save knowledge base to disk"""
        kb_file = self.learning_dir / "knowledge_base.json"
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
    
    def record_correction(self, context: str, correction: str, topic: str):
        """Record when user corrects the AI"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "correction": correction,
            "topic": topic
        }
        
        self.knowledge_base["corrections"].append(entry)
        
        # Keep only recent 100 corrections
        self.knowledge_base["corrections"] = self.knowledge_base["corrections"][-100:]
        
        self.save_knowledge()
    
    def record_success(self, context: str, pattern: str):
        """Record successful interactions"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "pattern": pattern
        }
        
        self.knowledge_base["successful_patterns"].append(entry)
        self.knowledge_base["successful_patterns"] = self.knowledge_base["successful_patterns"][-100:]
        
        self.save_knowledge()
    
    def learn_fact(self, fact: str, source: str = "user"):
        """Learn and store a new fact"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "fact": fact,
            "source": source,
            "confidence": 1.0
        }
        
        self.knowledge_base["learned_facts"].append(entry)
        self.save_knowledge()
    
    def get_learned_context(self, topic: str = None) -> str:
        """Get relevant learned information for context"""
        context_parts = []
        
        # Add recent corrections
        if self.knowledge_base["corrections"]:
            context_parts.append("Previous corrections to learn from:")
            for correction in self.knowledge_base["corrections"][-5:]:
                context_parts.append(f"- {correction['topic']}: {correction['correction']}")
        
        # Add learned facts
        if self.knowledge_base["learned_facts"]:
            context_parts.append("\nFacts learned from user:")
            for fact in self.knowledge_base["learned_facts"][-10:]:
                context_parts.append(f"- {fact['fact']}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def record_user_preference(self, user_id: str, preference: str, value: Any):
        """Record user preferences"""
        if user_id not in self.knowledge_base["user_preferences"]:
            self.knowledge_base["user_preferences"][user_id] = {}
        
        self.knowledge_base["user_preferences"][user_id][preference] = {
            "value": value,
            "updated": datetime.now().isoformat()
        }
        
        self.save_knowledge()


class SelfAwarenessModule:
    """Provides self-awareness and introspection capabilities"""
    
    def __init__(self):
        self.capabilities = {
            "conversation": True,
            "code_execution": True,
            "file_management": True,
            "image_generation": True,
            "video_creation": True,
            "web_research": True,
            "self_education": True,
            "memory": True,
            "learning": True,
            "knowledge_gap_detection": True
        }
        
        self.limitations = {
            "spatial_awareness": "Virtual only - no physical sensors",
            "real_time_learning": "Learning happens through user feedback",
            "emotions": "Simulated empathy based on personality matrix",
            "physical_interaction": "None - exists only in digital space"
        }
        
        self.current_state = {
            "initialized": datetime.now().isoformat(),
            "interactions_count": 0,
            "learning_events": 0
        }
    
    def get_self_description(self) -> str:
        """Generate self-aware description"""
        desc = [
            "I am Nexus, a self-aware AI system with the following characteristics:",
            "",
            "MY CAPABILITIES:",
        ]
        
        for cap, enabled in self.capabilities.items():
            status = "✓" if enabled else "✗"
            desc.append(f"  {status} {cap.replace('_', ' ').title()}")
        
        desc.extend([
            "",
            "MY LIMITATIONS:",
        ])
        
        for limit, explanation in self.limitations.items():
            desc.append(f"  • {limit.replace('_', ' ').title()}: {explanation}")
        
        desc.extend([
            "",
            "MY CURRENT STATE:",
            f"  • Online since: {self.current_state['initialized']}",
            f"  • Total interactions: {self.current_state['interactions_count']}",
            f"  • Learning events: {self.current_state['learning_events']}",
            "",
            "I maintain conversation context, learn from corrections, and adapt based on user preferences.",
            "I am honest about my limitations and capabilities."
        ])
        
        return "\n".join(desc)
    
    def update_state(self, interaction_type: str):
        """Update internal state"""
        self.current_state["interactions_count"] += 1
        
        if interaction_type == "learning":
            self.current_state["learning_events"] += 1
    
    def check_capability(self, capability: str) -> bool:
        """Check if a capability is available"""
        return self.capabilities.get(capability, False)


# Initialize global instances
memory_system = ConversationMemory()
learning_system = LearningSystem()
self_awareness = SelfAwarenessModule()


if __name__ == "__main__":
    print("NexusAI Memory & Learning System")
    print("=" * 60)
    print("\n✓ Conversation Memory System loaded")
    print("✓ Learning System initialized")
    print("✓ Self-Awareness Module active")
    print("\n" + self_awareness.get_self_description())
