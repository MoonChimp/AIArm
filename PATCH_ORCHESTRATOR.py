#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PATCH: Add file creation capability to existing orchestrator
Run this to update orchestrator.py with file creation support
"""

import re
from pathlib import Path

orchestrator_file = Path("D:/AIArm/NexusCore/orchestrator.py")
content = orchestrator_file.read_text()

# Patch 1: Add FileCreator import after other imports
import_patch = """from Agents.real_websearch_agent import RealWebSearchAgent

# Add file creator for app/script generation
sys.path.append(str(Path("D:/AIArm/NexusCore")))
from file_creator import FileCreator

BASE_DIR = Path("D:/AIArm")"""

content = content.replace(
    "from Agents.real_websearch_agent import RealWebSearchAgent\n\nBASE_DIR = Path(\"D:/AIArm\")",
    import_patch
)

# Patch 2: Add file_creator instance in __init__
init_patch = """        # Activate all agents
        for agent in self.agents.values():
            agent.activate()

        # File creator for app/script generation
        self.file_creator = FileCreator(self.ollama_base)

        # Ollama configuration"""

content = content.replace(
    "        # Activate all agents\n        for agent in self.agents.values():\n            agent.activate()\n\n        # Ollama configuration",
    init_patch
)

# Patch 3: Update routing to handle "create" requests
routing_examples = '''Examples:
- "create a music generator" → {"needs_agent": false, "needs_file_creation": true, "file_type": "music_app"}
- "make me a beat" → {"needs_agent": true, "agent": "music", "task": "generate a musical beat"}
- "well done!" → {"needs_agent": false}
- "hello" → {"needs_agent": false}
- "what's the weather?" → {"needs_agent": true, "agent": "websearch", "task": "search for current weather information"}
- "create a calculator app" → {"needs_agent": false, "needs_file_creation": true, "file_type": "calculator_app"}

When user says CREATE/MAKE/BUILD an APP/TOOL/PROGRAM → set needs_file_creation: true
When user wants CONTENT (music, photo, story) → use the appropriate agent

Respond ONLY in JSON:
{
  "needs_agent": true/false,
  "agent": "agent_name" (if needs_agent is true),
  "task": "clear task description" (if needs_agent is true),
  "needs_file_creation": true/false,
  "file_type": "description" (if needs_file_creation is true)
}'''

old_examples = '''Examples:
- "create a music generator" → {"needs_agent": true, "agent": "code", "task": "create a JavaScript music generator application"}
- "make me a beat" → {"needs_agent": true, "agent": "music", "task": "generate a musical beat"}
- "well done!" → {"needs_agent": false}
- "hello" → {"needs_agent": false}
- "what's the weather?" → {"needs_agent": true, "agent": "websearch", "task": "search for current weather information"}

Respond ONLY in JSON:
{
  "needs_agent": true/false,
  "agent": "agent_name" (if needs_agent is true),
  "task": "clear task description" (if needs_agent is true)
}'''

content = content.replace(old_examples, routing_examples)

# Patch 4: Update process() to handle file creation
process_check = '''        # STEP 1: Determine if this needs an agent or just conversation
        routing_decision = self._route_request(user_input)

        if routing_decision.get("needs_agent"):'''

process_patch = '''        # STEP 1: Determine if this needs an agent or just conversation
        routing_decision = self._route_request(user_input)

        # Check if file creation is needed
        if routing_decision.get("needs_file_creation"):
            print(f"[{self.name}] Creating file...")
            print(f"[{self.name}] Request: {user_input}\\n")

            result = self.file_creator.create_file(user_input)

            if result.get("status") == "success":
                response = f"I've created {result.get('file_path')} for you! It's a complete, working application. You can open it in your browser or editor."
            else:
                response = f"I encountered an issue creating the file: {result.get('message')}"

        elif routing_decision.get("needs_agent"):'''

content = content.replace(process_check, process_patch)

# Save patched version
orchestrator_file.write_text(content)

print("✅ Orchestrator patched successfully!")
print("File creation capability added.")
print("\nRestart the API server to apply changes:")
print("  Press Ctrl+C in PowerShell")
print("  Run: .\\RUN_API_DEBUG.ps1")
