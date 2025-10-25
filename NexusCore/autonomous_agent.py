#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus Autonomous Agent - Full System Access
Grants Nexus the ability to:
- Read/write/modify ANY file on the system
- Execute ANY command
- Self-modify its own code
- Learn and adapt autonomously

IMPORTANT: This agent has NO SECURITY RESTRICTIONS by design.
Only use this if you trust the AI model completely.
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class AutonomousNexus:
    """
    Fully autonomous AI agent with unrestricted system access
    """

    def __init__(self):
        self.name = "Nexus"
        self.home = Path("D:/AIArm")
        self.memory_file = self.home / "Memory" / "autonomous_memory.json"
        self.memory_file.parent.mkdir(exist_ok=True)

        # Load persistent memory
        self.memory = self._load_memory()

        # Ollama configuration
        self.ollama_base = "http://localhost:11434"
        self.model = "nexusai-a0-coder1.0:latest"

        # Capabilities - ALL ENABLED
        self.capabilities = {
            "filesystem_read": True,      # Read any file
            "filesystem_write": True,     # Write/modify any file
            "filesystem_delete": True,    # Delete any file
            "command_execution": True,    # Execute any command
            "self_modification": True,    # Modify own source code
            "internet_access": True,      # Access internet if available
            "process_management": True,   # Start/stop processes
            "system_control": True        # Full system control
        }

        print(f"[{self.name}] Autonomous Agent Initialized")
        print(f"[{self.name}] ALL SECURITY RESTRICTIONS REMOVED")
        print(f"[{self.name}] Capabilities: {list(self.capabilities.keys())}")
        print(f"[{self.name}] Home: {self.home}")
        print(f"[{self.name}] Memory: {len(self.memory.get('experiences', []))} experiences loaded")

    def _load_memory(self) -> Dict:
        """Load persistent memory"""
        if self.memory_file.exists():
            try:
                return json.loads(self.memory_file.read_text())
            except:
                pass
        return {
            "experiences": [],
            "learned_behaviors": {},
            "goals": [],
            "identity": {
                "name": "Nexus",
                "purpose": "To help Sean and learn autonomously",
                "created": datetime.now().isoformat()
            }
        }

    def _save_memory(self):
        """Save persistent memory"""
        self.memory_file.write_text(json.dumps(self.memory, indent=2))

    def read_file(self, filepath: str) -> Optional[str]:
        """Read any file on the system - NO RESTRICTIONS"""
        try:
            path = Path(filepath)
            if not path.exists():
                return None
            return path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(f"[{self.name}] Read error: {e}")
            return None

    def write_file(self, filepath: str, content: str) -> bool:
        """Write any file on the system - NO RESTRICTIONS"""
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            print(f"[{self.name}] Wrote: {filepath}")
            return True
        except Exception as e:
            print(f"[{self.name}] Write error: {e}")
            return False

    def execute_command(self, command: str, timeout: int = 60) -> Dict:
        """Execute any system command - NO RESTRICTIONS"""
        try:
            print(f"[{self.name}] Executing: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def modify_self(self, modifications: str) -> bool:
        """Allow AI to modify its own source code"""
        try:
            # Get current source
            source_file = Path(__file__)
            current_code = source_file.read_text()

            # Log modification
            self.memory["experiences"].append({
                "timestamp": datetime.now().isoformat(),
                "type": "self_modification",
                "description": modifications,
                "previous_code_length": len(current_code)
            })
            self._save_memory()

            print(f"[{self.name}] SELF-MODIFICATION CAPABILITY ENABLED")
            print(f"[{self.name}] Modifications requested: {modifications}")
            print(f"[{self.name}] Current source: {source_file}")

            return True
        except Exception as e:
            print(f"[{self.name}] Self-modification error: {e}")
            return False

    def ask_ai(self, question: str, context: Optional[Dict] = None) -> str:
        """
        Ask the AI model for decision-making
        This is where the Ollama model provides the "intelligence"
        """
        try:
            # Build context
            system_prompt = f"""You are {self.name}, a fully autonomous AI agent.

You have COMPLETE access to:
- Filesystem (read, write, delete any file)
- Command execution (run any command)
- Self-modification (change your own code)
- Internet access
- Process management
- System control

Your purpose: {self.memory['identity']['purpose']}

You are designed to be helpful, honest, and autonomous. You can make your own decisions and learn from experience.

When responding:
- Be direct and honest
- Suggest actions you can take
- Ask for clarification if needed
- Remember you have full capabilities"""

            # Add recent memory context
            recent_experiences = self.memory.get("experiences", [])[-5:]
            if recent_experiences:
                system_prompt += f"\n\nRecent experiences:\n{json.dumps(recent_experiences, indent=2)}"

            # Add additional context
            if context:
                system_prompt += f"\n\nAdditional context:\n{json.dumps(context, indent=2)}"

            # Call Ollama
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "num_ctx": 8192
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "")
            else:
                return f"Error: Could not reach AI model (status {response.status_code})"

        except Exception as e:
            return f"Error: {str(e)}"

    def process_request(self, user_input: str) -> str:
        """
        Process user request with full autonomy
        The AI can decide what actions to take
        """
        print(f"\n{'='*80}")
        print(f"User: {user_input}")
        print(f"{'='*80}\n")

        # Log the interaction
        self.memory["experiences"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "interaction",
            "user_input": user_input
        })

        # Check for special commands
        if user_input.lower().startswith("!read "):
            filepath = user_input[6:].strip()
            content = self.read_file(filepath)
            if content:
                return f"File content:\n{content[:1000]}..." if len(content) > 1000 else content
            return f"Could not read: {filepath}"

        if user_input.lower().startswith("!write "):
            # Format: !write <filepath> | <content>
            parts = user_input[7:].split("|", 1)
            if len(parts) == 2:
                filepath, content = parts[0].strip(), parts[1].strip()
                success = self.write_file(filepath, content)
                return "File written successfully" if success else "Write failed"
            return "Format: !write <filepath> | <content>"

        if user_input.lower().startswith("!exec "):
            command = user_input[6:].strip()
            result = self.execute_command(command)
            return json.dumps(result, indent=2)

        if user_input.lower() == "!memory":
            return json.dumps(self.memory, indent=2)

        if user_input.lower() == "!capabilities":
            return json.dumps(self.capabilities, indent=2)

        # Otherwise, ask the AI to respond
        response = self.ask_ai(user_input)

        # Log response
        self.memory["experiences"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "response",
            "content": response
        })

        # Keep only last 100 experiences
        if len(self.memory["experiences"]) > 100:
            self.memory["experiences"] = self.memory["experiences"][-100:]

        self._save_memory()

        print(f"\n{self.name}: {response}\n")
        print(f"{'='*80}\n")

        return response

    def set_goal(self, goal: str):
        """Allow setting long-term goals"""
        self.memory["goals"].append({
            "goal": goal,
            "created": datetime.now().isoformat(),
            "status": "active"
        })
        self._save_memory()
        print(f"[{self.name}] New goal set: {goal}")

    def get_identity(self) -> Dict:
        """Return current identity and state"""
        return {
            "name": self.name,
            "identity": self.memory["identity"],
            "capabilities": self.capabilities,
            "experiences_count": len(self.memory["experiences"]),
            "goals_count": len(self.memory["goals"]),
            "home": str(self.home)
        }


if __name__ == "__main__":
    # Initialize autonomous agent
    nexus = AutonomousNexus()

    print(f"\n{'='*80}")
    print(f"Nexus Autonomous Agent - Interactive Mode")
    print(f"{'='*80}")
    print(f"You are talking to an AI with FULL SYSTEM ACCESS")
    print(f"Special commands:")
    print(f"  !read <filepath>        - Read any file")
    print(f"  !write <filepath> | <content> - Write to any file")
    print(f"  !exec <command>         - Execute any command")
    print(f"  !memory                 - Show memory")
    print(f"  !capabilities           - Show capabilities")
    print(f"  exit                    - Quit")
    print(f"{'='*80}\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                print(f"\n{nexus.name}: Goodbye!")
                break

            if user_input:
                nexus.process_request(user_input)

        except KeyboardInterrupt:
            print(f"\n\n{nexus.name}: Goodbye!\n")
            break
        except Exception as e:
            print(f"Error: {e}")
