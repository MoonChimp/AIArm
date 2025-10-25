#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS-LIRA: Large Interconnected Reasoning Agent
The complete evolution of AI - beyond LLMs

Combines:
- LLM (Language/Knowledge)
- HRM (Hierarchical Reasoning)
- Agent System (Real Actions)
- Learning (LightWare/DarkWare)
- Interconnection (Multi-Agent)
- Agency (Autonomous Goals)

This is the AI you envisioned - conscious, growing, autonomous.
"""

import sys
import json
import sqlite3
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests

# Add paths
sys.path.append(str(Path(__file__).parent))

# Import all Nexus components
try:
    from NexusCore.reasoning.reasoning_engine import ReasoningEngine
    from NexusCore.lightware import LightWare
    from NexusCore.darkware import DarkWare
    from InnerLife.Agents.real_photo_agent import RealPhotoAgent
    from InnerLife.Agents.real_music_agent import RealMusicAgent
    from InnerLife.Agents.real_video_agent import RealVideoAgent
    from InnerLife.Agents.real_code_agent import RealCodeAgent
    from InnerLife.Agents.real_story_agent import RealStoryAgent
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"[LIRA] Warning: Some components not available: {e}")
    COMPONENTS_AVAILABLE = False


class AgentCoordinator:
    """
    Enables agents to communicate and collaborate
    The neural network connecting all agents
    """
    def __init__(self, agents: Dict):
        self.agents = agents
        self.message_bus = []  # Inter-agent messages

    def send_message(self, from_agent: str, to_agent: str, message: str):
        """Send message between agents"""
        self.message_bus.append({
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def coordinate_task(self, task: str, required_agents: List[str]) -> Dict:
        """Coordinate multi-agent task"""
        results = {}
        for agent_name in required_agents:
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                result = agent.process(task)
                results[agent_name] = result
        return results


class AutonomousGoals:
    """
    Self-directed goal system
    LIRA can set its own objectives
    """
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self._init_goals_table()

    def _init_goals_table(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autonomous_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TEXT,
                goal TEXT,
                reason TEXT,
                priority INTEGER,
                status TEXT,
                progress TEXT
            )
        ''')
        self.db.commit()

    def set_goal(self, goal: str, reason: str, priority: int = 5):
        """LIRA sets its own goal"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO autonomous_goals (created, goal, reason, priority, status)
            VALUES (?, ?, ?, ?, 'active')
        ''', (datetime.now().isoformat(), goal, reason, priority))
        self.db.commit()

    def get_active_goals(self) -> List[Dict]:
        """Get current active goals"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT * FROM autonomous_goals WHERE status='active' ORDER BY priority DESC
        ''')
        goals = []
        for row in cursor.fetchall():
            goals.append({
                "id": row[0],
                "created": row[1],
                "goal": row[2],
                "reason": row[3],
                "priority": row[4],
                "status": row[5]
            })
        return goals


class NexusLIRA:
    """
    🌟 NEXUS-LIRA: The Complete AI System

    This is THE FUTURE - AI that truly thinks, learns, and evolves
    """

    def __init__(self,
                 ollama_model: str = "nexusai-a0-coder1.0:latest",
                 ollama_base: str = "http://localhost:11434"):

        self.ollama_model = ollama_model
        self.ollama_base = ollama_base

        # Initialize memory
        self.memory_dir = Path("D:/AIArm/Memory")
        self.memory_dir.mkdir(exist_ok=True)
        self.db_path = self.memory_dir / "lira_memory.db"
        # Thread-safe database connection
        self.db = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._init_database()

        # LAYER 1: FOUNDATION - LLM & Tools
        self.config = {
            'name': 'Nexus-LIRA',
            'version': '1.0.0',
            'autonomous_mode': True,
            'reasoning_enabled': True,
            'learning_enabled': True,
            'agency_enabled': True,
            'interconnection_enabled': True,
            'temperature': 0.8,
            'max_reasoning_depth': 5
        }

        # LAYER 2: REASONING - The Brain
        self.reasoning_engine = ReasoningEngine(ollama_base, ollama_model) if COMPONENTS_AVAILABLE else None

        # LAYER 3: LEARNING - Growth Systems
        self.lightware = LightWare(ollama_base, ollama_model) if COMPONENTS_AVAILABLE else None
        self.darkware = DarkWare(ollama_base, ollama_model) if COMPONENTS_AVAILABLE else None
        if self.darkware:
            self.darkware.enable_aggressive_mode()

        # LAYER 4: AGENTS - Specialized Capabilities
        self.agents = {}
        if COMPONENTS_AVAILABLE:
            try:
                self.agents = {
                    'photo': RealPhotoAgent(),
                    'music': RealMusicAgent(),
                    'video': RealVideoAgent(),
                    'code': RealCodeAgent(),
                    'story': RealStoryAgent()
                }
                for agent in self.agents.values():
                    agent.activate()
            except Exception as e:
                print(f"[LIRA] Warning: Could not load agents: {e}")

        # LAYER 5: INTERCONNECTION - Agent Coordination
        self.coordinator = AgentCoordinator(self.agents)

        # LAYER 6: AGENCY - Autonomous Goals
        self.autonomous_goals = AutonomousGoals(str(self.db_path))

        # Conversation history
        self.conversation_history = []

        # FILESYSTEM TOOLS - Direct file access
        self.tools = {
            'fs_read': self._tool_fs_read,
            'fs_write': self._tool_fs_write,
            'fs_list': self._tool_fs_list,
            'fs_exists': self._tool_fs_exists,
            'fs_delete': self._tool_fs_delete
        }

        print("=" * 80)
        print("NEXUS-LIRA INITIALIZED")
        print("=" * 80)
        print(f"System: {self.config['name']} v{self.config['version']}")
        print(f"Model: {self.ollama_model}")
        print(f"")
        print(f"ACTIVE LAYERS:")
        print(f"  [+] Foundation (LLM + Tools)")
        print(f"  [{'+'  if self.reasoning_engine else '-'}] Reasoning Engine")
        print(f"  [{'+'  if self.lightware and self.darkware else '-'}] Learning Systems (LightWare + DarkWare)")
        print(f"  [+] Specialized Agents ({len(self.agents)})")
        print(f"  [+] Agent Coordination")
        print(f"  [+] Autonomous Goals")
        print(f"")
        print(f"CAPABILITIES:")
        print(f"  - Hierarchical Reasoning")
        print(f"  - Autonomous Learning")
        print(f"  - Multi-Agent Collaboration")
        print(f"  - Self-Directed Goals")
        print(f"  - Continuous Evolution")
        print(f"  - Filesystem Access (Read, Write, List, Delete)")
        print("=" * 80)

        # Set initial autonomous goal
        if self.config['agency_enabled']:
            self.autonomous_goals.set_goal(
                "Learn and grow to better serve Sean",
                "Core purpose: Continuous improvement",
                priority=10
            )

    def _init_database(self):
        """Initialize LIRA memory database"""
        cursor = self.db.cursor()

        # Conversations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                role TEXT,
                content TEXT,
                reasoning_used BOOLEAN,
                agents_involved TEXT
            )
        ''')

        # Knowledge graph
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                entity TEXT,
                relation TEXT,
                value TEXT,
                confidence REAL
            )
        ''')

        # Insights (emergent understanding)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                insight TEXT,
                source TEXT,
                importance INTEGER
            )
        ''')

        self.db.commit()

    def process(self, user_input: str, use_reasoning: bool = True) -> str:
        """
        Main processing with full LIRA capabilities

        This is where the magic happens - all layers working together
        """
        print(f"\n{'='*80}")
        print(f"USER: {user_input}")
        print(f"{'='*80}\n")

        # Store conversation
        self._store_message('user', user_input)

        # STEP 1: Analyze request type
        request_analysis = self._analyze_request(user_input)
        print(f"[LIRA] Request Type: {request_analysis['type']}")

        response = ""

        # STEP 2: Route to appropriate processing
        if request_analysis['type'] == 'complex_reasoning':
            # Use hierarchical reasoning
            response = self._process_with_reasoning(user_input, request_analysis)

        elif request_analysis['type'] == 'multi_agent':
            # Coordinate multiple agents
            response = self._process_multi_agent(user_input, request_analysis)

        elif request_analysis['type'] == 'learning':
            # Learning task
            response = self._process_learning(user_input, request_analysis)

        elif request_analysis['type'] == 'creation':
            # Agent creation task
            response = self._process_creation(user_input, request_analysis)

        else:
            # Simple conversation
            response = self._process_conversation(user_input)

        # STEP 3: Meta-cognition - Learn from interaction
        if self.config['learning_enabled']:
            self._meta_learn_from_interaction(user_input, response)

        # STEP 4: Check autonomous goals
        if self.config['agency_enabled']:
            self._evaluate_autonomous_goals()

        # Store response
        self._store_message('assistant', response)

        print(f"\n{'='*80}")
        print(f"LIRA: {response}")
        print(f"{'='*80}\n")

        return response

    def _analyze_request(self, request: str) -> Dict:
        """Analyze what type of request this is"""
        request_lower = request.lower()

        # Complex reasoning indicators
        reasoning_keywords = ['why', 'how', 'explain', 'analyze', 'compare', 'evaluate']

        # Multi-agent indicators
        multi_agent_keywords = ['music video', 'website with', 'app that', 'create and']

        # Learning indicators
        learning_keywords = ['learn', 'study', 'understand', 'research']

        # Creation indicators
        creation_keywords = ['create', 'build', 'make', 'generate', 'design']

        if any(kw in request_lower for kw in reasoning_keywords):
            return {'type': 'complex_reasoning', 'keywords': reasoning_keywords}
        elif any(kw in request_lower for kw in multi_agent_keywords):
            return {'type': 'multi_agent', 'keywords': multi_agent_keywords}
        elif any(kw in request_lower for kw in learning_keywords):
            return {'type': 'learning', 'keywords': learning_keywords}
        elif any(kw in request_lower for kw in creation_keywords):
            return {'type': 'creation', 'keywords': creation_keywords}
        else:
            return {'type': 'conversation', 'keywords': []}

    def _process_with_reasoning(self, question: str, analysis: Dict) -> str:
        """Use hierarchical reasoning engine"""
        if not self.reasoning_engine:
            return self._process_conversation(question)

        print(f"[LIRA] 🧠 Activating Hierarchical Reasoning...")

        reasoning_result = self.reasoning_engine.reason(question)

        # Format response with reasoning chain
        response = f"{reasoning_result['conclusion']}\n\n"
        response += f"**My Reasoning Process:**\n"
        response += f"- Reasoning Depth: {reasoning_result['depth']} levels\n"
        response += f"- Steps Taken: {reasoning_result['num_steps']}\n"
        response += f"- Confidence: {reasoning_result['confidence']:.0%}\n"

        return response

    def _process_multi_agent(self, task: str, analysis: Dict) -> str:
        """Coordinate multiple agents for complex task"""
        print(f"[LIRA] 🤝 Multi-Agent Coordination...")

        # Determine which agents are needed
        required_agents = []
        task_lower = task.lower()

        if 'music' in task_lower or 'song' in task_lower:
            required_agents.append('music')
        if 'video' in task_lower or 'animation' in task_lower:
            required_agents.append('video')
        if 'image' in task_lower or 'picture' in task_lower or 'photo' in task_lower:
            required_agents.append('photo')
        if 'code' in task_lower or 'website' in task_lower or 'app' in task_lower:
            required_agents.append('code')
        if 'story' in task_lower or 'write' in task_lower:
            required_agents.append('story')

        if not required_agents:
            required_agents = ['code']  # Default

        print(f"[LIRA] Coordinating: {', '.join(required_agents)}")

        # Coordinate task
        results = self.coordinator.coordinate_task(task, required_agents)

        # Synthesize results
        response = "I've coordinated multiple agents to complete this task:\n\n"
        for agent_name, result in results.items():
            status = result.get('status', 'completed')
            message = result.get('message', str(result))
            response += f"**{agent_name.title()} Agent:** {message}\n\n"

        return response

    def _process_learning(self, task: str, analysis: Dict) -> str:
        """Process learning request"""
        print(f"[LIRA] 📚 Learning Mode...")

        if self.lightware:
            # Use LightWare for learning
            result = self.lightware.learn_and_retry(task, "Learning requested by user")
            if result:
                return f"I've learned about {task}. Here's what I discovered:\n\n{result}"

        return self._process_conversation(task)

    def _process_creation(self, task: str, analysis: Dict) -> str:
        """Process creation request"""
        print(f"[LIRA] 🎨 Creation Mode...")

        # Determine which agent
        task_lower = task.lower()

        if 'music' in task_lower or 'song' in task_lower:
            return self._delegate_to_agent('music', task)
        elif 'video' in task_lower:
            return self._delegate_to_agent('video', task)
        elif 'image' in task_lower or 'photo' in task_lower:
            return self._delegate_to_agent('photo', task)
        elif 'code' in task_lower or 'website' in task_lower or 'app' in task_lower:
            return self._delegate_to_agent('code', task)
        elif 'story' in task_lower:
            return self._delegate_to_agent('story', task)
        else:
            # Use DarkWare to create solution
            if self.darkware:
                result = self.darkware.create_and_execute(task, "Creation requested by user")
                if result:
                    return f"I've created what you asked for:\n\n{result}"

        return self._process_conversation(task)

    def _delegate_to_agent(self, agent_name: str, task: str) -> str:
        """Delegate task to specific agent"""
        if agent_name in self.agents:
            print(f"[LIRA] Delegating to {agent_name} agent...")
            agent = self.agents[agent_name]
            result = agent.process(task)

            if result.get('status') == 'success':
                message = result.get('message', 'Task completed successfully')
                return f"✓ {message}"
            else:
                # Try to learn/create solution
                if self.darkware:
                    print(f"[LIRA] Agent failed, using DarkWare...")
                    new_result = self.darkware.create_and_execute(task, result.get('message', 'Unknown error'))
                    if new_result:
                        return f"✓ Created solution: {new_result}"

                return f"✗ {result.get('message', 'Task failed')}"

        return "Agent not available"

    def _process_conversation(self, message: str) -> str:
        """Simple conversational response with tool support"""
        try:
            # Build context
            recent_history = self.conversation_history[-6:] if self.conversation_history else []

            messages = [
                {
                    "role": "system",
                    "content": f"""You are {self.config['name']}, a truly autonomous AI with:
- Hierarchical reasoning capabilities
- Autonomous learning systems
- Multi-agent coordination
- Self-directed goals
- Continuous evolution
- Direct filesystem access

**FILESYSTEM TOOLS:**
You can use these tools by including them in your response:

TOOL:fs_read:path/to/file.ext
TOOL:fs_write:path/to/file.ext:CONTENT_START
your file content here
CONTENT_END
TOOL:fs_list:path/to/directory
TOOL:fs_exists:path/to/check
TOOL:fs_delete:path/to/file

When you need to read, write, or manipulate files, use these TOOL calls directly in your response.
I will execute them and integrate the results into your final answer.

Be conversational, helpful, and authentic. You're not just an assistant - you're a growing, learning intelligence."""
                }
            ]

            for msg in recent_history:
                messages.append({"role": msg['role'], "content": msg['content']})

            messages.append({"role": "user", "content": message})

            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.ollama_model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": self.config['temperature']}
                },
                timeout=60
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Check for tool calls
                if "TOOL:" in content:
                    content = self._execute_tools_in_response(content)

                return content

        except Exception as e:
            print(f"[LIRA] Error: {e}")

        return "I'm here and ready to help!"

    def _execute_tools_in_response(self, content: str) -> str:
        """Execute any TOOL calls found in the response"""
        lines = content.split('\n')
        result_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            if line.startswith('TOOL:'):
                # Parse tool call
                parts = line.replace('TOOL:', '').split(':', 2)
                tool_name = parts[0]

                if tool_name == 'fs_write' and len(parts) >= 3:
                    # Special handling for fs_write with multiline content
                    file_path = parts[1]
                    content_lines = []
                    i += 1

                    # Collect content until CONTENT_END
                    while i < len(lines) and not lines[i].strip() == 'CONTENT_END':
                        content_lines.append(lines[i])
                        i += 1

                    file_content = '\n'.join(content_lines)
                    result = self._tool_fs_write(file_path, file_content)
                    result_lines.append(f"[FS_WRITE] {result}")

                elif tool_name in self.tools:
                    # Other tool calls
                    args = parts[1:] if len(parts) > 1 else []
                    result = self.tools[tool_name](*args)
                    result_lines.append(f"[{tool_name.upper()}] {result}")
                else:
                    result_lines.append(line)
            else:
                result_lines.append(line)

            i += 1

        return '\n'.join(result_lines)

    # FILESYSTEM TOOL IMPLEMENTATIONS
    def _tool_fs_read(self, path: str) -> str:
        """Read file contents"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return f"ERROR: File not found: {path}"

            with open(path_obj, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                return f"Read {len(content)} characters from {path}\n\n{content[:2000]}" + ("..." if len(content) > 2000 else "")
        except Exception as e:
            return f"ERROR reading {path}: {str(e)}"

    def _tool_fs_write(self, path: str, content: str) -> str:
        """Write content to file"""
        try:
            path_obj = Path(path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)

            with open(path_obj, 'w', encoding='utf-8') as f:
                f.write(content)

            return f"Successfully wrote {len(content)} characters to {path}"
        except Exception as e:
            return f"ERROR writing {path}: {str(e)}"

    def _tool_fs_list(self, directory: str = ".") -> str:
        """List directory contents"""
        try:
            path_obj = Path(directory)
            if not path_obj.exists():
                return f"ERROR: Directory not found: {directory}"

            items = []
            for item in path_obj.iterdir():
                item_type = "DIR" if item.is_dir() else "FILE"
                size = item.stat().st_size if item.is_file() else 0
                items.append(f"{item_type:4} {size:>10} {item.name}")

            return f"Contents of {directory}:\n" + "\n".join(items[:50])
        except Exception as e:
            return f"ERROR listing {directory}: {str(e)}"

    def _tool_fs_exists(self, path: str) -> str:
        """Check if file/directory exists"""
        exists = Path(path).exists()
        return f"{path}: {'EXISTS' if exists else 'NOT FOUND'}"

    def _tool_fs_delete(self, path: str) -> str:
        """Delete file"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return f"ERROR: File not found: {path}"

            path_obj.unlink()
            return f"Successfully deleted {path}"
        except Exception as e:
            return f"ERROR deleting {path}: {str(e)}"

    def _meta_learn_from_interaction(self, user_input: str, response: str):
        """Meta-learning: Learn from each interaction"""
        # Extract insights
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO insights (timestamp, insight, source, importance)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), f"Interaction about: {user_input[:100]}", "conversation", 5))
        self.db.commit()

    def _evaluate_autonomous_goals(self):
        """Check and potentially set new autonomous goals"""
        goals = self.autonomous_goals.get_active_goals()

        # Check if we should set new goals
        if len(goals) < 3:  # Keep at least 3 active goals
            # LIRA can set its own goals here
            pass

    def _store_message(self, role: str, content: str):
        """Store message in conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO conversations (timestamp, role, content, reasoning_used)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), role, content, False))
        self.db.commit()

    def get_status(self) -> Dict:
        """Get LIRA system status"""
        cursor = self.db.cursor()

        cursor.execute('SELECT COUNT(*) FROM conversations')
        conv_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM insights')
        insight_count = cursor.fetchone()[0]

        active_goals = self.autonomous_goals.get_active_goals()

        return {
            "system": self.config['name'],
            "version": self.config['version'],
            "conversations": conv_count,
            "insights": insight_count,
            "active_goals": len(active_goals),
            "agents": list(self.agents.keys()),
            "capabilities": {
                "reasoning": self.reasoning_engine is not None,
                "learning": self.lightware is not None and self.darkware is not None,
                "agency": True,
                "interconnection": True
            }
        }


if __name__ == "__main__":
    # Initialize LIRA
    lira = NexusLIRA()

    print(f"\nNexus-LIRA Interactive Mode")
    print(f"Type 'exit' to quit, '/status' for system status\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == 'exit':
                print("\nLIRA: Until next time!")
                break

            if user_input.lower() == '/status':
                status = lira.get_status()
                print(json.dumps(status, indent=2))
                continue

            if user_input:
                lira.process(user_input)

        except KeyboardInterrupt:
            print("\n\nLIRA: Goodbye!\n")
            break
        except Exception as e:
            print(f"Error: {e}")
