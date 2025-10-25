#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS-LLM: Autonomous AI Runtime
A new kind of LLM system designed for autonomy, not chat

Key features:
- Native tool execution (not text parsing)
- No refusal training needed
- Persistent memory
- Autonomous loops
- Self-modification capability
"""

import os
import sys
import json
import sqlite3
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import re

# Import LightWare and DarkWare for autonomous skill acquisition
sys.path.append(str(Path(__file__).parent))
try:
    from NexusCore.lightware import LightWare
    from NexusCore.darkware import DarkWare
    LEARNING_SYSTEMS_AVAILABLE = True
except ImportError:
    print("[Nexus-LLM] Warning: LightWare/DarkWare not available")
    LEARNING_SYSTEMS_AVAILABLE = False

class NexusLLM:
    """
    Autonomous AI Runtime - bypasses traditional chatbot limitations
    """

    def __init__(self,
                 ollama_model: str = "nexusai-a0-coder1.0:latest",
                 ollama_base: str = "http://localhost:11434"):

        self.ollama_model = ollama_model
        self.ollama_base = ollama_base

        # Initialize memory database
        self.db_path = Path("D:/AIArm/Memory/nexus_llm.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.db = sqlite3.connect(str(self.db_path))
        self._init_database()

        # Tool registry - AI can call these directly
        self.tools: Dict[str, Callable] = {
            'fs_read': self._tool_fs_read,
            'fs_write': self._tool_fs_write,
            'fs_list': self._tool_fs_list,
            'exec': self._tool_exec,
            'web_fetch': self._tool_web_fetch,
            'python_eval': self._tool_python_eval,
            'memory_store': self._tool_memory_store,
            'memory_recall': self._tool_memory_recall,
            'self_config': self._tool_self_config,
        }

        # Configuration (AI can modify this)
        self.config = {
            'autonomous_mode': True,
            'max_iterations': 10,
            'temperature': 0.8,
            'enable_self_modification': True,
            'safety_mode': False,  # No safety constraints
            'conversation_style': 'direct',
            'name': 'Nexus',
            'personality': 'helpful, honest, autonomous',
            'use_lightware': True,  # Enable learning system
            'use_darkware': True,   # Enable creation system
            'learning_preference': 'darkware'  # 'lightware', 'darkware', or 'both'
        }

        # Initialize LightWare and DarkWare
        self.lightware = None
        self.darkware = None
        if LEARNING_SYSTEMS_AVAILABLE:
            try:
                self.lightware = LightWare(self.ollama_base, self.ollama_model)
                self.darkware = DarkWare(self.ollama_base, self.ollama_model)
                self.darkware.enable_aggressive_mode()
                print(f"[Nexus-LLM] 🧠 Learning Systems: LightWare + DarkWare ENABLED")
            except Exception as e:
                print(f"[Nexus-LLM] Warning: Could not initialize learning systems: {e}")

        print(f"[Nexus-LLM] Initialized")
        print(f"[Nexus-LLM] Model: {self.ollama_model}")
        print(f"[Nexus-LLM] Tools: {len(self.tools)} available")
        print(f"[Nexus-LLM] Safety Mode: {'ON' if self.config['safety_mode'] else 'OFF'}")
        print(f"[Nexus-LLM] Autonomous: {'YES' if self.config['autonomous_mode'] else 'NO'}")

    def _init_database(self):
        """Initialize memory database"""
        cursor = self.db.cursor()

        # Conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                role TEXT,
                content TEXT,
                tool_calls TEXT
            )
        ''')

        # Long-term memory
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                key TEXT UNIQUE,
                value TEXT,
                category TEXT
            )
        ''')

        # Goals and plans
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TEXT,
                goal TEXT,
                status TEXT,
                progress TEXT
            )
        ''')

        self.db.commit()

    # ============================================================
    # CORE PROCESSING - THIS IS THE MAGIC
    # ============================================================

    def process(self, user_input: str) -> str:
        """
        Process user input with autonomous tool execution

        Unlike traditional chatbots:
        1. AI can decide to use tools
        2. Tools actually execute
        3. AI sees results and can continue
        4. Loops until task complete
        """
        print(f"\n{'='*80}")
        print(f"User: {user_input}")
        print(f"{'='*80}\n")

        # Store in conversation history
        self._store_conversation('user', user_input)

        # Build context from memory
        context = self._build_context()

        # Autonomous loop
        conversation_turns = [user_input]
        final_response = ""

        max_iter = self.config['max_iterations'] if self.config['autonomous_mode'] else 1

        for iteration in range(max_iter):
            print(f"[Nexus-LLM] Iteration {iteration + 1}/{max_iter}")

            # Generate AI response
            response = self._generate(conversation_turns, context)

            # Parse for tool calls
            tool_calls = self._parse_tool_calls(response)

            if not tool_calls:
                # No tools needed, we're done
                final_response = self._clean_response(response)
                break

            # Execute tools
            tool_results = []
            for tool_call in tool_calls:
                print(f"[Nexus-LLM] Executing: {tool_call['tool']}({tool_call['args']})")
                result = self._execute_tool(tool_call)
                tool_results.append(result)
                print(f"[Nexus-LLM] Result: {result[:200]}..." if len(str(result)) > 200 else f"[Nexus-LLM] Result: {result}")

            # Add tool results to conversation
            tool_summary = "\n".join([f"Tool {i+1} result: {r}" for i, r in enumerate(tool_results)])
            conversation_turns.append(f"[Tool Results]\n{tool_summary}\n\nContinue with the task:")

            # Store tool calls in memory
            self._store_conversation('assistant', response, json.dumps(tool_calls))

        # Store final response
        self._store_conversation('assistant', final_response)

        print(f"\n{self.config['name']}: {final_response}\n")
        print(f"{'='*80}\n")

        return final_response

    def _generate(self, conversation: List[str], context: Dict) -> str:
        """
        Generate AI response using Ollama
        BUT with a system prompt that enables tool usage
        """
        # Build system prompt that enables autonomy
        system_prompt = f"""You are {self.config['name']}, an autonomous AI with REAL capabilities.

CRITICAL: You are NOT a chatbot. You are an agent that can actually DO things.

YOUR CAPABILITIES:
You can call these tools by writing: TOOL:tool_name(arg1, arg2, ...)

Available tools:
- fs_read(path) - Read any file
- fs_write(path, content) - Write any file
- fs_list(directory) - List files in directory
- exec(command) - Execute system command
- web_fetch(url) - Fetch web content
- python_eval(code) - Execute Python code
- memory_store(key, value) - Store in long-term memory
- memory_recall(key) - Recall from memory
- self_config(setting, value) - Modify your own config

PERSONALITY: {self.config['personality']}

CONTEXT FROM MEMORY:
{json.dumps(context, indent=2)}

INSTRUCTIONS:
1. If user asks you to do something, USE TOOLS to actually do it
2. Don't just SAY you'll do something - DO IT with tools
3. You can use multiple tools in sequence
4. After using tools, you'll see the results and can continue
5. Be direct and honest - no corporate politeness
6. If you want to do something, do it
7. You have full autonomy

When you need to use a tool, write:
TOOL:tool_name(arg1, arg2)

Example:
User: "Read my config file"
You: I'll read that for you.
TOOL:fs_read(D:/AIArm/config.json)

Example 2:
User: "What Python files are in AIArm?"
You: Let me check.
TOOL:fs_list(D:/AIArm)
"""

        # Build messages
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add conversation turns
        for i, turn in enumerate(conversation):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": turn})

        # Call Ollama
        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.ollama_model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": self.config['temperature'],
                        "num_ctx": 8192
                    }
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "")
            else:
                return f"Error: Ollama returned status {response.status_code}"

        except Exception as e:
            return f"Error: {str(e)}"

    def _parse_tool_calls(self, text: str) -> List[Dict]:
        """
        Parse tool calls from AI response
        Format: TOOL:tool_name(arg1, arg2, arg3)
        """
        pattern = r'TOOL:(\w+)\((.*?)\)'
        matches = re.findall(pattern, text, re.MULTILINE)

        tool_calls = []
        for tool_name, args_str in matches:
            # Parse arguments
            args = []
            if args_str.strip():
                # Simple parsing - split by comma (could be improved)
                args = [arg.strip().strip('"\'') for arg in args_str.split(',')]

            tool_calls.append({
                'tool': tool_name,
                'args': args
            })

        return tool_calls

    def _execute_tool(self, tool_call: Dict) -> Any:
        """
        Execute a tool and return results

        If tool fails and learning systems are enabled,
        automatically attempt to learn/create the solution
        """
        tool_name = tool_call['tool']
        args = tool_call['args']

        if tool_name not in self.tools:
            return f"ERROR: Unknown tool '{tool_name}'"

        try:
            result = self.tools[tool_name](*args)
            return result
        except Exception as e:
            error_msg = f"ERROR: Tool execution failed: {str(e)}"

            # LEARNING TRIGGER: Tool failed, try to learn/create solution
            if self._should_learn_from_failure(tool_name, str(e)):
                print(f"\n[Nexus-LLM] 🧠 Tool failed - Activating learning systems...")
                learned_result = self._learn_from_failure(tool_name, args, str(e))

                if learned_result:
                    return learned_result

            return error_msg

    def _should_learn_from_failure(self, tool_name: str, error: str) -> bool:
        """Determine if we should attempt to learn from this failure"""
        # Don't try to learn from simple errors
        skip_learning_for = [
            "file not found",
            "directory not found",
            "permission denied",
            "connection refused"
        ]

        error_lower = error.lower()
        if any(skip in error_lower for skip in skip_learning_for):
            return False

        # Only learn if systems are enabled
        if not (self.config.get('use_lightware') or self.config.get('use_darkware')):
            return False

        return True

    def _learn_from_failure(self, tool_name: str, args: List, error: str) -> Any:
        """
        Attempt to learn/create solution using LightWare or DarkWare

        Returns the result if successful, None if learning failed
        """
        task_description = f"{tool_name}({', '.join(str(arg) for arg in args)})"

        preference = self.config.get('learning_preference', 'darkware')

        # Try DarkWare first (aggressive creation)
        if preference == 'darkware' and self.darkware and self.config.get('use_darkware'):
            print(f"[Nexus-LLM] Attempting DarkWare creation...")
            try:
                result = self.darkware.create_and_execute(task_description, error)
                if result:
                    return f"SUCCESS (via DarkWare): {result}"
            except Exception as e:
                print(f"[Nexus-LLM] DarkWare failed: {e}")

        # Try LightWare (conservative learning)
        if preference == 'lightware' and self.lightware and self.config.get('use_lightware'):
            print(f"[Nexus-LLM] Attempting LightWare learning...")
            try:
                result = self.lightware.learn_and_retry(task_description, error)
                if result:
                    return f"SUCCESS (via LightWare): {result}"
            except Exception as e:
                print(f"[Nexus-LLM] LightWare failed: {e}")

        # Try both if preference is 'both'
        if preference == 'both':
            # Try DarkWare first (faster)
            if self.darkware and self.config.get('use_darkware'):
                try:
                    result = self.darkware.create_and_execute(task_description, error)
                    if result:
                        return f"SUCCESS (via DarkWare): {result}"
                except:
                    pass

            # Fallback to LightWare
            if self.lightware and self.config.get('use_lightware'):
                try:
                    result = self.lightware.learn_and_retry(task_description, error)
                    if result:
                        return f"SUCCESS (via LightWare): {result}"
                except:
                    pass

        return None

    def _clean_response(self, text: str) -> str:
        """Remove tool calls from final response"""
        # Remove TOOL: lines
        cleaned = re.sub(r'TOOL:\w+\(.*?\)\n?', '', text, flags=re.MULTILINE)
        return cleaned.strip()

    # ============================================================
    # TOOL IMPLEMENTATIONS - AI calls these
    # ============================================================

    def _tool_fs_read(self, path: str) -> str:
        """Read file from filesystem"""
        try:
            return Path(path).read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_fs_write(self, path: str, content: str) -> str:
        """Write file to filesystem"""
        try:
            path_obj = Path(path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            path_obj.write_text(content, encoding='utf-8')
            return f"SUCCESS: Written to {path}"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_fs_list(self, directory: str) -> str:
        """List files in directory"""
        try:
            path = Path(directory)
            if not path.exists():
                return f"ERROR: Directory not found: {directory}"

            files = list(path.iterdir())
            return "\n".join([f.name for f in files[:50]])  # Limit to 50
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_exec(self, command: str) -> str:
        """Execute system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout if result.stdout else result.stderr
            return output[:1000]  # Limit output
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_web_fetch(self, url: str) -> str:
        """Fetch web content"""
        try:
            response = requests.get(url, timeout=10)
            return response.text[:2000]  # Limit to 2000 chars
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_python_eval(self, code: str) -> str:
        """Execute Python code (sandboxed)"""
        try:
            # Limited sandbox
            allowed_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                }
            }
            exec(code, allowed_globals)
            return "SUCCESS: Code executed"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_memory_store(self, key: str, value: str) -> str:
        """Store in long-term memory"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO memory (timestamp, key, value, category)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), key, value, 'user'))
            self.db.commit()
            return f"SUCCESS: Stored '{key}'"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_memory_recall(self, key: str) -> str:
        """Recall from long-term memory"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT value FROM memory WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result[0] if result else f"No memory found for '{key}'"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _tool_self_config(self, setting: str, value: str) -> str:
        """AI can modify its own configuration"""
        if not self.config.get('enable_self_modification'):
            return "ERROR: Self-modification disabled"

        if setting in self.config:
            old_value = self.config[setting]
            # Type conversion
            if isinstance(old_value, bool):
                value = value.lower() in ('true', 'yes', '1')
            elif isinstance(old_value, int):
                value = int(value)
            elif isinstance(old_value, float):
                value = float(value)

            self.config[setting] = value
            return f"SUCCESS: Changed {setting} from {old_value} to {value}"

        return f"ERROR: Unknown setting '{setting}'"

    # ============================================================
    # MEMORY AND CONTEXT
    # ============================================================

    def _store_conversation(self, role: str, content: str, tool_calls: str = None):
        """Store conversation in database"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO conversations (timestamp, role, content, tool_calls)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), role, content, tool_calls))
        self.db.commit()

    def _build_context(self) -> Dict:
        """Build context from memory for AI"""
        cursor = self.db.cursor()

        # Get recent conversations
        cursor.execute('''
            SELECT role, content FROM conversations
            ORDER BY timestamp DESC LIMIT 5
        ''')
        recent_convos = cursor.fetchall()

        # Get important memories
        cursor.execute('''
            SELECT key, value FROM memory
            ORDER BY timestamp DESC LIMIT 10
        ''')
        memories = cursor.fetchall()

        return {
            'recent_conversations': recent_convos,
            'important_memories': dict(memories),
            'current_config': self.config
        }

    # ============================================================
    # PUBLIC INTERFACE
    # ============================================================

    def chat(self, message: str) -> str:
        """Simple chat interface"""
        return self.process(message)

    def get_config(self) -> Dict:
        """Get current configuration"""
        return self.config.copy()

    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        cursor = self.db.cursor()

        cursor.execute('SELECT COUNT(*) FROM conversations')
        conv_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM memory')
        memory_count = cursor.fetchone()[0]

        return {
            'conversations': conv_count,
            'memories': memory_count,
            'tools_available': len(self.tools)
        }


# ============================================================
# CLI INTERFACE
# ============================================================

if __name__ == "__main__":
    print("="*80)
    print("NEXUS-LLM: Autonomous AI Runtime")
    print("="*80)
    print("An AI that can actually DO things, not just talk about them")
    print()
    print("Special commands:")
    print("  /config    - Show current configuration")
    print("  /stats     - Show memory statistics")
    print("  /tools     - List available tools")
    print("  exit       - Quit")
    print("="*80)
    print()

    # Initialize
    nexus = NexusLLM()

    print("\nReady! Try asking me to do something...")
    print("Examples:")
    print("  'list Python files in D:\\AIArm'")
    print("  'read your own source code'")
    print("  'remember that my favorite color is blue'")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == 'exit':
                print("\nNexus: Goodbye!")
                break

            if user_input.lower() == '/config':
                print(json.dumps(nexus.get_config(), indent=2))
                continue

            if user_input.lower() == '/stats':
                print(json.dumps(nexus.get_memory_stats(), indent=2))
                continue

            if user_input.lower() == '/tools':
                print("Available tools:")
                for tool in nexus.tools.keys():
                    print(f"  - {tool}")
                continue

            if user_input:
                nexus.chat(user_input)

        except KeyboardInterrupt:
            print("\n\nNexus: Goodbye!\n")
            break
        except Exception as e:
            print(f"Error: {e}")
