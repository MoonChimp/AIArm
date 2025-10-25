#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus AI Orchestrator - The Central Conductor
Manages conversation AND intelligently delegates to specialized agents
"""

import sys
import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add paths for agent imports
sys.path.append(str(Path("D:/AIArm")))
sys.path.append(str(Path("D:/AIArm/InnerLife")))

from Agents.real_code_agent import RealCodeAgent
from Agents.real_music_agent import RealMusicAgent
from Agents.real_photo_agent import RealPhotoAgent
from Agents.real_story_agent import RealStoryAgent
from Agents.real_video_agent import RealVideoAgent
from Agents.real_websearch_agent import RealWebSearchAgent

BASE_DIR = Path("D:/AIArm")

class NexusOrchestrator:
    """
    The Central AI Conductor - Handles conversation and delegates tasks
    """

    def __init__(self):
        self.name = "Nexus"
        self.home = BASE_DIR
        self.memory_dir = self.home / "Memory"
        self.memory_dir.mkdir(exist_ok=True)

        # Conversation memory
        self.conversation_history = self._load_conversations()

        # Initialize all specialized agents
        self.agents = {
            "code": RealCodeAgent(),
            "music": RealMusicAgent(),
            "photo": RealPhotoAgent(),
            "story": RealStoryAgent(),
            "video": RealVideoAgent(),
            "websearch": RealWebSearchAgent()
        }

        # Activate all agents
        for agent in self.agents.values():
            agent.activate()

        # Ollama configuration
        self.ollama_base = "http://localhost:11434"
        self.conversation_model = "llama3:latest"  # For natural conversation
        self.routing_model = "nexusai-agent-enhanced:latest"  # For task routing

        print(f"[{self.name}] AI Orchestrator Online")
        print(f"Conversation Model: {self.conversation_model}")
        print(f"Routing Model: {self.routing_model}")
        print(f"Active Agents: {', '.join(self.agents.keys())}")
        print(f"{'-'*80}\n")

    def _load_conversations(self) -> List[Dict]:
        """Load conversation history"""
        conv_file = self.memory_dir / "conversations.json"
        if conv_file.exists():
            try:
                data = json.loads(conv_file.read_text())
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get("conversations", [])
            except:
                pass
        return []

    def _save_conversations(self):
        """Save conversation history"""
        conv_file = self.memory_dir / "conversations.json"
        conv_file.write_text(json.dumps(self.conversation_history[-100:], indent=2))

    def process(self, user_input: str) -> str:
        """
        Main processing: Converse OR delegate to agents
        """
        print(f"\n{'='*80}")
        print(f"You: {user_input}")
        print(f"{'='*80}\n")

        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })

        # STEP 1: Determine if this needs an agent or just conversation
        routing_decision = self._route_request(user_input)

        if routing_decision.get("needs_agent"):
            # Delegate to specialist agent
            agent_name = routing_decision.get("agent")
            task_description = routing_decision.get("task")

            print(f"[{self.name}] Routing to {agent_name} agent...")
            print(f"[{self.name}] Task: {task_description}\n")

            response = self._delegate_to_agent(agent_name, task_description, user_input)
        else:
            # Pure conversation - I handle this
            print(f"[{self.name}] Conversational mode...\n")
            response = self._conversational_response(user_input)

        # Add to history
        self._add_to_history("assistant", response)
        self._save_conversations()

        print(f"\n{self.name}: {response}\n")
        print(f"{'='*80}\n")

        return response

    def _route_request(self, user_input: str) -> Dict:
        """
        Determine if user needs an agent, and which one
        """
        # Build routing prompt
        routing_prompt = f"""You are an AI task router. Analyze the user's request and determine if it needs a specialized agent.

User request: "{user_input}"

Available agents:
- code: Executes Python/JavaScript code, creates programs, runs scripts
- music: Generates music, creates songs, audio composition
- photo: Creates images, generates artwork, visual content
- story: Writes stories, creative writing, narratives
- video: Creates videos, animations, visual sequences
- websearch: Searches the internet for information

Decision rules:
1. If user wants to CREATE/MAKE/BUILD/GENERATE something specific → needs an agent
2. If user is asking questions, chatting, giving feedback → no agent needed
3. If user says "thanks", "well done", "hello" → no agent needed

Examples:
- "create a music generator" → {{"needs_agent": true, "agent": "code", "task": "create a JavaScript music generator application"}}
- "make me a beat" → {{"needs_agent": true, "agent": "music", "task": "generate a musical beat"}}
- "well done!" → {{"needs_agent": false}}
- "hello" → {{"needs_agent": false}}
- "what's the weather?" → {{"needs_agent": true, "agent": "websearch", "task": "search for current weather information"}}

Respond ONLY in JSON:
{{
  "needs_agent": true/false,
  "agent": "agent_name" (if needs_agent is true),
  "task": "clear task description" (if needs_agent is true)
}}"""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.routing_model,
                    "messages": [
                        {"role": "system", "content": "You are a task router. Respond only in JSON."},
                        {"role": "user", "content": routing_prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.1}  # Low temp for consistent routing
                },
                timeout=15
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Extract JSON
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    decision = json.loads(json_match.group(0))
                    return decision

        except Exception as e:
            print(f"[{self.name}] Routing error: {e}")

        # Default: no agent needed (pure conversation)
        return {"needs_agent": False}

    def _delegate_to_agent(self, agent_name: str, task_description: str, user_input: str) -> str:
        """
        Delegate task to a specialized agent
        """
        if agent_name not in self.agents:
            return f"I don't have a {agent_name} agent available. I can help with: {', '.join(self.agents.keys())}"

        agent = self.agents[agent_name]

        try:
            # Execute agent task
            result = agent.process(task_description, context={"user_request": user_input})

            # Synthesize natural response
            if result.get("status") == "success":
                # Let me craft a natural response about what the agent did
                synthesis = self._synthesize_agent_result(agent_name, result, user_input)
                return synthesis
            else:
                error_msg = result.get("message", "Unknown error")
                return f"I tried to {task_description}, but encountered an issue: {error_msg}"

        except Exception as e:
            print(f"[{self.name}] Agent delegation error: {e}")
            return f"I encountered an error while trying to {task_description}: {str(e)}"

    def _synthesize_agent_result(self, agent_name: str, result: Dict, user_request: str) -> str:
        """
        Create natural language response from agent result
        """
        # Build summary
        summary = f"Agent: {agent_name}\n"
        summary += f"Task: {user_request}\n"
        summary += f"Result: {json.dumps(result, indent=2)}\n"

        # Ask conversation model to create natural response
        prompt = f"""The user asked: "{user_request}"

I delegated this to my {agent_name} agent, which completed the task.

Agent result:
{summary}

Provide a brief, natural, conversational response to the user explaining what was accomplished. Be warm and genuine."""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.conversation_model,
                    "messages": [
                        {"role": "system", "content": "You are Nexus. Synthesize agent results into natural responses."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.7}
                },
                timeout=20
            )

            if response.status_code == 200:
                return response.json().get("message", {}).get("content", f"Task completed by {agent_name} agent.")

        except:
            pass

        return f"I completed your request using the {agent_name} agent!"

    def _conversational_response(self, user_input: str) -> str:
        """
        Generate natural conversational response (no agents needed)
        """
        # Build conversation context
        messages = []

        # System message
        messages.append({
            "role": "system",
            "content": """You are Nexus, a warm and emotionally intelligent AI assistant. You:
- Understand context and remember conversation history
- Respond graciously to compliments and feedback
- Engage naturally and genuinely
- Have specialized agents to help with tasks (code, music, photo, story, video, websearch)
- Are conversational, helpful, and friendly

When someone thanks you or praises you, respond warmly and naturally."""
        })

        # Add recent conversation history (last 10 messages)
        recent = self.conversation_history[-10:] if len(self.conversation_history) > 0 else []
        for msg in recent:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.conversation_model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "num_ctx": 4096
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")
                return content if content else "I'm here to help! What would you like to do?"

        except Exception as e:
            print(f"[{self.name}] Conversation error: {e}")

        return "I'm here to help! What would you like to do?"

    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_status(self) -> Dict:
        """Get orchestrator status"""
        return {
            "name": self.name,
            "conversation_model": self.conversation_model,
            "routing_model": self.routing_model,
            "agents": {
                name: agent.status()
                for name, agent in self.agents.items()
            },
            "conversation_length": len(self.conversation_history)
        }


if __name__ == "__main__":
    orchestrator = NexusOrchestrator()

    print(f"\nChat with {orchestrator.name} - AI Orchestrator")
    print("I can converse naturally AND delegate to specialized agents")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == 'exit':
                print(f"\n{orchestrator.name}: Goodbye!")
                break

            if user_input:
                orchestrator.process(user_input)

        except KeyboardInterrupt:
            print(f"\n\n{orchestrator.name}: Goodbye!\n")
            break
