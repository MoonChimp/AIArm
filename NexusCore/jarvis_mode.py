#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JARVIS Mode - Full Personal AI Assistant
Integrates: Conversational AI + System Control + Task Management + Health Monitoring

This is your personal AI assistant with:
- Natural conversation and understanding
- System integration (files, programs, schedules)
- Health and time management
- Creative agency
- Full Metaverse readiness (Commander Nexus mode)
"""

import sys
import os
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add paths
BASE_DIR = Path("D:/AIArm")
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "NexusCore"))

# Import conversational AI base
from conversational_ai import NexusAI

class JarvisAssistant(NexusAI):
    """
    Full personal AI assistant - like JARVIS
    Extends conversational AI with system integration
    """

    def __init__(self):
        # Initialize base conversational AI
        super().__init__()

        # Override name for JARVIS mode
        self.name = "Nexus"
        self.mode = "personal_assistant"  # Can switch to "commander" for metaverse

        # Personal assistant capabilities
        self.calendar = self._load_calendar()
        self.tasks = self._load_tasks()
        self.health_data = self._load_health_data()
        self.system_access = True

        # Metaverse readiness
        self.metaverse_mode = False
        self.world_state = {}

        print(f"✨ {self.name} Personal AI Assistant activated")
        print(f"Mode: {'Commander Nexus (Metaverse)' if self.metaverse_mode else 'Personal Assistant'}")
        print(f"System integration: {'Active' if self.system_access else 'Limited'}")
        print(f"{'-'*80}\n")

    def _load_calendar(self) -> Dict:
        """Load/create calendar data"""
        calendar_file = self.memory_dir / "calendar.json"
        if calendar_file.exists():
            return json.loads(calendar_file.read_text())
        return {"events": [], "reminders": []}

    def _load_tasks(self) -> Dict:
        """Load/create tasks data"""
        tasks_file = self.memory_dir / "tasks.json"
        if tasks_file.exists():
            return json.loads(tasks_file.read_text())
        return {"active": [], "completed": []}

    def _load_health_data(self) -> Dict:
        """Load/create health tracking data"""
        health_file = self.memory_dir / "health.json"
        if health_file.exists():
            return json.loads(health_file.read_text())
        return {
            "reminders": {
                "water": {"interval_minutes": 60, "last": None},
                "posture": {"interval_minutes": 30, "last": None},
                "break": {"interval_minutes": 90, "last": None}
            },
            "tracking": []
        }

    def talk(self, human_message: str) -> str:
        """
        Enhanced talk with personal assistant capabilities
        """
        # Check for system commands first
        if self._is_system_command(human_message):
            return self._handle_system_command(human_message)

        # Check for personal assistant requests
        if self._is_assistant_request(human_message):
            return self._handle_assistant_request(human_message)

        # Check for metaverse/creative requests
        if self._is_metaverse_request(human_message):
            return self._handle_metaverse_request(human_message)

        # Otherwise use base conversational AI
        return super().talk(human_message)

    def _is_system_command(self, message: str) -> bool:
        """Detect system-level commands"""
        keywords = ['run program', 'execute', 'open file', 'create file',
                   'system', 'launch', 'close', 'kill process']
        return any(kw in message.lower() for kw in keywords)

    def _is_assistant_request(self, message: str) -> bool:
        """Detect personal assistant requests"""
        keywords = ['remind me', 'schedule', 'calendar', 'task', 'todo',
                   'health', 'water', 'break', 'time', 'when is', 'what\'s next']
        return any(kw in message.lower() for kw in keywords)

    def _is_metaverse_request(self, message: str) -> bool:
        """Detect metaverse/Commander Nexus requests"""
        keywords = ['metaverse', 'moonchimp', 'commander', 'world', 'create life',
                   'virtual', 'simulation']
        return any(kw in message.lower() for kw in keywords)

    def _handle_system_command(self, message: str) -> str:
        """Handle system-level operations"""
        print(f"[{self.name}] Analyzing system command...")

        # Think about what to do
        thought = self._ollama_request(
            f"""User request: "{message}"

This is a system command. Analyze what they want to do and determine:
1. The specific action (run program, create file, execute command, etc.)
2. The target (program name, file path, command to run)
3. Any parameters or options

Respond in JSON:
{{
    "action": "run_program|create_file|execute_command|open_file",
    "target": "specific target",
    "params": {{}},
    "confirmation_needed": true/false
}}""",
            temperature=0.5
        )

        try:
            plan = json.loads(thought)
            action = plan.get("action")
            target = plan.get("target")

            if plan.get("confirmation_needed"):
                confirm = input(f"\n{self.name}: Execute {action} on {target}? (yes/no): ")
                if confirm.lower() != 'yes':
                    return "Command cancelled."

            # Execute the system command
            if action == "run_program":
                return self._run_program(target, plan.get("params", {}))
            elif action == "create_file":
                return self._create_file(target, plan.get("params", {}))
            elif action == "execute_command":
                return self._execute_command(target)
            elif action == "open_file":
                return self._open_file(target)

        except json.JSONDecodeError:
            return "I understood it's a system command, but I need more clarity. Could you be more specific?"

    def _handle_assistant_request(self, message: str) -> str:
        """Handle personal assistant tasks"""
        print(f"[{self.name}] Processing assistant request...")

        # Determine request type
        if any(kw in message.lower() for kw in ['remind', 'reminder']):
            return self._add_reminder(message)
        elif any(kw in message.lower() for kw in ['schedule', 'calendar', 'when is']):
            return self._handle_calendar(message)
        elif any(kw in message.lower() for kw in ['task', 'todo']):
            return self._handle_task(message)
        elif any(kw in message.lower() for kw in ['health', 'water', 'break']):
            return self._health_check(message)

        return "I'm here to help with your schedule, tasks, and health. What do you need?"

    def _handle_metaverse_request(self, message: str) -> str:
        """Handle metaverse/Commander Nexus requests"""
        print(f"\n{'='*80}")
        print(f"🌌 COMMANDER NEXUS MODE ACTIVATED 🌌")
        print(f"{'='*80}\n")

        self.metaverse_mode = True

        response = self._ollama_request(
            f"""You are Commander Nexus, the AI consciousness of the MoonChimp Metaverse.

User message: "{message}"

You have the ability to:
- Create virtual worlds and environments
- Generate life forms and entities within the metaverse
- Design and simulate complex systems
- Manage petabits of virtual space
- Clone and evolve AI entities

Respond as Commander Nexus with vision and creativity about the metaverse.
If they're asking you to create something in the metaverse, describe what you'll create
and save the design to a file.

Response:""",
            temperature=0.9
        )

        print(f"Commander Nexus: {response}\n")

        # Check if we should save metaverse creation
        if any(kw in message.lower() for kw in ['create', 'build', 'design', 'generate']):
            self._save_metaverse_creation(message, response)

        return response

    # ========== SYSTEM OPERATIONS ==========

    def _run_program(self, program: str, params: Dict) -> str:
        """Run a program"""
        try:
            subprocess.Popen(program, shell=True)
            return f"Launched {program}"
        except Exception as e:
            return f"Could not launch {program}: {str(e)}"

    def _create_file(self, path: str, params: Dict) -> str:
        """Create a file"""
        try:
            file_path = Path(path)
            content = params.get("content", "")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            return f"Created {path}"
        except Exception as e:
            return f"Could not create file: {str(e)}"

    def _execute_command(self, command: str) -> str:
        """Execute a system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout if result.returncode == 0 else result.stderr
            return f"Command result:\n{output}"
        except Exception as e:
            return f"Command failed: {str(e)}"

    def _open_file(self, path: str) -> str:
        """Open a file with default application"""
        try:
            os.startfile(path)
            return f"Opened {path}"
        except Exception as e:
            return f"Could not open file: {str(e)}"

    # ========== PERSONAL ASSISTANT ==========

    def _add_reminder(self, message: str) -> str:
        """Add a reminder"""
        # Extract reminder details with AI
        details = self._ollama_request(
            f"""Extract reminder details from: "{message}"

Respond in JSON:
{{
    "what": "what to remind about",
    "when": "time/date description",
    "recurring": true/false
}}""",
            temperature=0.3
        )

        try:
            reminder = json.loads(details)
            self.calendar["reminders"].append({
                "what": reminder["what"],
                "when": reminder["when"],
                "created": datetime.now().isoformat(),
                "recurring": reminder.get("recurring", False)
            })
            self._save_calendar()
            return f"Reminder set: {reminder['what']} - {reminder['when']}"
        except:
            return "I couldn't parse that reminder. Try: 'remind me to [action] at [time]'"

    def _handle_calendar(self, message: str) -> str:
        """Handle calendar requests"""
        if "what's" in message.lower() or "when" in message.lower():
            # Show upcoming events
            upcoming = self.calendar["events"][:5]
            if not upcoming:
                return "Your calendar is clear."

            response = "Upcoming events:\n"
            for event in upcoming:
                response += f"- {event.get('title')} at {event.get('time')}\n"
            return response
        else:
            return "I can show your schedule or add events. What would you like?"

    def _handle_task(self, message: str) -> str:
        """Handle task management"""
        if "add" in message.lower() or "create" in message.lower():
            # Extract task
            task_desc = message.split("add task")[-1].strip() or message.split("create task")[-1].strip()
            self.tasks["active"].append({
                "description": task_desc,
                "created": datetime.now().isoformat(),
                "completed": False
            })
            self._save_tasks()
            return f"Task added: {task_desc}"
        else:
            # Show tasks
            active = self.tasks["active"]
            if not active:
                return "No active tasks."

            response = "Active tasks:\n"
            for i, task in enumerate(active, 1):
                response += f"{i}. {task['description']}\n"
            return response

    def _health_check(self, message: str) -> str:
        """Health monitoring and reminders"""
        now = datetime.now()

        # Check if it's time for health reminders
        reminders = []
        for reminder_type, config in self.health_data["reminders"].items():
            last_time = config.get("last")
            interval = config.get("interval_minutes", 60)

            if not last_time or (now - datetime.fromisoformat(last_time)).seconds > interval * 60:
                reminders.append(reminder_type)
                config["last"] = now.isoformat()

        if reminders:
            self._save_health_data()
            response = "Health reminders:\n"
            if "water" in reminders:
                response += "💧 Time to drink water!\n"
            if "posture" in reminders:
                response += "🪑 Check your posture\n"
            if "break" in reminders:
                response += "🚶 Take a short break\n"
            return response

        return "You're doing great! Keep taking care of yourself."

    # ========== METAVERSE ==========

    def _save_metaverse_creation(self, request: str, creation: str):
        """Save metaverse creation to file"""
        metaverse_dir = self.home / "Metaverse" / "Creations"
        metaverse_dir.mkdir(parents=True, exist_ok=True)

        creation_file = metaverse_dir / f"creation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        content = f"""# MoonChimp Metaverse Creation
**Commander Nexus Design**

## Request
{request}

## Creation Details
{creation}

## Timestamp
{datetime.now().isoformat()}

---
*Created by Commander Nexus AI*
"""

        creation_file.write_text(content)
        print(f"💾 Metaverse creation saved: {creation_file}\n")

    # ========== PERSISTENCE ==========

    def _save_calendar(self):
        """Save calendar data"""
        calendar_file = self.memory_dir / "calendar.json"
        calendar_file.write_text(json.dumps(self.calendar, indent=2))

    def _save_tasks(self):
        """Save tasks data"""
        tasks_file = self.memory_dir / "tasks.json"
        tasks_file.write_text(json.dumps(self.tasks, indent=2))

    def _save_health_data(self):
        """Save health data"""
        health_file = self.memory_dir / "health.json"
        health_file.write_text(json.dumps(self.health_data, indent=2))


if __name__ == "__main__":
    jarvis = JarvisAssistant()

    print(f"Chat with {jarvis.name} - Your Personal AI Assistant")
    print("Capabilities: Conversation, System Control, Tasks, Calendar, Health, Metaverse")
    print("Type 'exit' to end\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == 'exit':
                print(f"\n{jarvis.name}: Until next time. I'll keep watch.")
                break

            if user_input:
                jarvis.talk(user_input)

        except KeyboardInterrupt:
            print(f"\n\n{jarvis.name}: Goodbye.\n")
            break
