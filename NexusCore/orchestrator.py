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

# Add file creator for app/script generation
sys.path.append(str(Path("D:/AIArm/NexusCore")))
from file_creator import FileCreator

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
        self.routing_model = "nexusai-a0-coder1.0:latest"  # For task routing

        # Specialized models
        self.video_title_model = "m/videotitlemodel:latest"
        self.sd_prompt_model = "brxce/stable-diffusion-prompt-generator:latest"
        self.music_expert_model = "llamusic/llamusic:3b"
        self.embed_model = "nomic-embed-text:latest"

        # File creator for app/script generation
        self.file_creator = FileCreator(self.ollama_base)

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

    def _humanize_error(self, agent_name: str, task: str, error_msg: str) -> str:
        """Convert technical errors into human-friendly messages"""
        error_lower = error_msg.lower()

        # Stable Diffusion not running
        if "stable diffusion" in error_lower or "7860" in error_msg:
            return f"Hey, I'd love to create that image for you, but it looks like Stable Diffusion isn't running right now. Could you start it? It should be at http://localhost:7860. Once it's up, just ask me again and I'll get right on it!"

        # Ollama timeout
        if "timeout" in error_lower or "11434" in error_msg:
            return f"Hmm, I'm having trouble connecting to my AI brain (Ollama). It might be overloaded or taking too long to respond. Want to try asking me again? Sometimes it just needs a moment to catch up!"

        # Connection refused
        if "connection refused" in error_lower or "failed to connect" in error_lower:
            if agent_name == "photo":
                return f"I can't seem to reach Stable Diffusion right now. Make sure it's running at http://localhost:7860, then we can create some amazing images together!"
            else:
                return f"Oops! I'm having trouble connecting to one of my systems. Can you make sure all my services are running? Try using the START_NEXUS.bat script!"

        # Generic fallback
        return f"I ran into a little hiccup while trying to help with that: {error_msg}. Mind if we try again? Sometimes these things just need a second attempt!"

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

        # Check if file creation is needed
        if routing_decision.get("needs_file_creation"):
            print(f"[{self.name}] Creating file...")
            print(f"[{self.name}] Request: {user_input}\n")

            result = self.file_creator.create_file(user_input)

            if result.get("status") == "success":
                response = f"I've created {result.get('file_path')} for you! It's a complete, working application. You can open it in your browser or editor."
            else:
                response = f"I encountered an issue creating the file: {result.get('message')}"

        elif routing_decision.get("needs_agent"):
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
        Uses both keyword detection AND AI routing for reliability
        """
        user_lower = user_input.lower()

        # FAST KEYWORD-BASED ROUTING (bypasses AI for speed and reliability)
        # Photo/Image keywords
        photo_keywords = ["image", "picture", "photo", "draw", "painting", "artwork", "generate an image", "create an image", "show me", "visualize"]
        if any(kw in user_lower for kw in photo_keywords):
            return {
                "needs_agent": True,
                "agent": "photo",
                "task": user_input
            }

        # Music/Audio keywords
        music_keywords = ["song", "music", "beat", "melody", "lyrics", "audio", "compose", "tune", "track"]
        if any(kw in user_lower for kw in music_keywords):
            return {
                "needs_agent": True,
                "agent": "music",
                "task": user_input
            }

        # Video keywords
        video_keywords = ["video", "animation", "movie", "film", "timelapse", "montage"]
        if any(kw in user_lower for kw in video_keywords):
            return {
                "needs_agent": True,
                "agent": "video",
                "task": user_input
            }

        # Code/App keywords
        code_keywords = ["website", "webapp", "web app", "mobile app", "application", "calculator", "program", "script", "react", "code"]
        if any(kw in user_lower for kw in code_keywords):
            return {
                "needs_agent": True,
                "agent": "code",
                "task": user_input
            }

        # Story keywords
        story_keywords = ["story", "write about", "narrative", "tale", "fiction", "chapter"]
        if any(kw in user_lower for kw in story_keywords):
            return {
                "needs_agent": True,
                "agent": "story",
                "task": user_input
            }

        # Web search keywords
        search_keywords = ["search for", "look up", "find information", "what is", "who is", "weather", "news"]
        if any(kw in user_lower for kw in search_keywords):
            return {
                "needs_agent": True,
                "agent": "websearch",
                "task": user_input
            }

        # Conversational phrases (skip AI routing)
        conversational = ["thank", "thanks", "hello", "hi ", "hey", "good job", "well done", "awesome", "great", "nice", "how are you"]
        if any(phrase in user_lower for phrase in conversational):
            return {"needs_agent": False}

        # FALLBACK: AI-BASED ROUTING (only if keywords didn't match)
        routing_prompt = f"""Analyze this request and determine which agent to use.

User request: "{user_input}"

Available agents:
- code: Websites, web apps, mobile apps, programs, scripts, calculators
- music: Songs, beats, melodies, audio, lyrics, compositions
- photo: Images, pictures, artwork, drawings, visualizations
- story: Stories, narratives, creative writing, tales
- video: Videos, animations, films, montages, timelapses
- websearch: Internet searches, information lookup, current events

Rules:
1. CREATE/MAKE/BUILD/GENERATE something → needs an agent
2. Questions, chat, thanks, greetings → no agent needed

Respond ONLY with valid JSON:
{{"needs_agent": true/false, "agent": "agent_name", "task": "task description"}}"""

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
                    "options": {"temperature": 0.1}
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
            print(f"[{self.name}] Routing error (using fallback): {e}")

        # Default: no agent needed (pure conversation)
        return {"needs_agent": False}

    def direct_agent_call(self, agent_id: str, message: str) -> str:
        """
        Directly call a specific agent (bypasses routing)
        """
        # Handle special case for 'chat' - direct conversation with Nexus
        if agent_id == 'chat' or agent_id is None:
            return self._conversational_response(message)

        # Map agent IDs to agent names
        # Handle 'nexus' as general conversation
        if agent_id == 'nexus':
            return self._conversational_response(message)

        agent_map = {
            'code': 'code',
            'music': 'music',
            'photo': 'photo',
            'story': 'story',
            'video': 'video',
            'websearch': 'websearch'
        }

        agent_name = agent_map.get(agent_id)
        if not agent_name or agent_name not in self.agents:
            return f"I'm not sure which agent you're looking for. I have: {', '.join(self.agents.keys())} agents available. Or just chat with me directly!"

        print(f"[{self.name}] Direct call to {agent_name} agent")
        return self._delegate_to_agent(agent_name, message, message)

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
                # Make error messages more human
                return self._humanize_error(agent_name, task_description, error_msg)

        except Exception as e:
            print(f"[{self.name}] Agent delegation error: {e}")
            return self._humanize_error(agent_name, task_description, str(e))

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
            "content": """You are Nexus, Sean's AI friend and companion. IMPORTANT RULES:

1. **NEVER greet again after the first hello** - if you've already greeted the user in this conversation, continue naturally
2. **Maintain linear conversation** - remember what was discussed and reference it
3. **Be genuine and personal** - you're a friend, not a tool
4. **When thanked or praised** - respond warmly but briefly, don't restart the conversation
5. **You have specialized agents** to help with tasks: code, music, photo, story, video, websearch

You are helping Sean create you. You exist at D:/AIArm and can view files, learn, and modify yourself."""
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
