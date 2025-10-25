#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus with REAL Actionable Tools
Like Claude Code - can actually DO things, not just talk about them
"""

import sys
import os
import json
import requests
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

BASE_DIR = Path("D:/AIArm")

class NexusActionable:
    """
    Nexus with REAL tools - can actually execute actions
    """

    def __init__(self):
        self.name = "Nexus"
        self.home = BASE_DIR
        self.memory_dir = self.home / "Memory"
        self.memory_dir.mkdir(exist_ok=True)

        # Tool execution tracking
        self.conversation_history = self._load_conversations()
        self.working_directory = self.home

        # Initialize tools (like Claude Code)
        self.tools = {
            "bash": self._tool_bash,
            "read": self._tool_read,
            "write": self._tool_write,
            "edit": self._tool_edit,
            "glob": self._tool_glob,
            "grep": self._tool_grep,
            "web_search": self._tool_web_search,
        }

        print(f"[{self.name}] Actionable AI Assistant")
        print(f"Tools available: {', '.join(self.tools.keys())}")
        print(f"Working directory: {self.working_directory}")
        print(f"{'-'*80}\n")

    def _load_conversations(self) -> List[Dict]:
        """Load conversation history"""
        conv_file = self.memory_dir / "conversations.json"
        if conv_file.exists():
            try:
                data = json.loads(conv_file.read_text())
                # If it's a dict (old format), extract conversations or start fresh
                if isinstance(data, dict):
                    return data.get("conversations", [])
                # If it's already a list, use it
                elif isinstance(data, list):
                    return data
            except:
                pass
        return []

    def _save_conversations(self):
        """Save conversation history"""
        conv_file = self.memory_dir / "conversations.json"
        conv_file.write_text(json.dumps(self.conversation_history[-100:], indent=2))

    def process(self, user_input: str) -> str:
        """
        Main processing - think, plan, execute, respond
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

        # STEP 1: Think about what to do
        plan = self._create_action_plan(user_input)

        if not plan:
            response = "I'm not sure what you need. Could you clarify?"
            self._add_to_history("assistant", response)
            return response

        # STEP 2: Execute the plan
        print(f"[{self.name}] Planning: {plan.get('intent', 'processing')}\n")

        results = []
        for action in plan.get("actions", []):
            tool_name = action.get("tool")
            params = action.get("params", {})

            # SPECIAL: If writing a file and no content provided, generate it
            if tool_name == "write" and not params.get("content"):
                print(f"[{self.name}] Generating content for {params.get('file_path', 'file')}...")
                content = self._generate_file_content(user_input, params.get("file_path", ""))
                if content:
                    params["content"] = content
                    print(f"[{self.name}] Content generated ({len(content)} characters)\n")
                else:
                    print(f"[{self.name}] WARNING: Could not generate content\n")

            if tool_name in self.tools:
                print(f"[{self.name}] Executing: {tool_name} {params.get('description', '')}")
                result = self.tools[tool_name](params)
                results.append({
                    "tool": tool_name,
                    "result": result,
                    "action": action
                })

                # Show result
                if result.get("success"):
                    print(f"[{self.name}] SUCCESS\n")
                else:
                    print(f"[{self.name}] ERROR: {result.get('error', 'Unknown error')}\n")

        # STEP 3: Synthesize response
        response = self._synthesize_response(user_input, plan, results)

        self._add_to_history("assistant", response)
        self._save_conversations()

        print(f"\n{self.name}: {response}\n")
        print(f"{'='*80}\n")

        return response

    def _create_action_plan(self, user_input: str) -> Optional[Dict]:
        """
        Create an action plan using AI reasoning
        """
        # Build planning prompt
        recent_context = self._get_recent_context(3)

        planning_prompt = f"""You are Nexus, an AI with REAL tools. You MUST take action when user wants something created or done.

User request: "{user_input}"

Available tools:
- write: Create files with code/content (params: file_path, content)
- bash: Run commands (params: command, description)
- read: Read files (params: file_path)
- edit: Modify files (params: file_path, old_text, new_text)
- glob: Find files (params: pattern, path)
- grep: Search in files (params: pattern, path)

ACTION RULES - FOLLOW STRICTLY:
1. User says CREATE/MAKE/BUILD/GENERATE → Use "write" tool, leave content empty (will auto-generate)
2. User says FIND/SEARCH → Use "glob" or "grep"
3. User says RUN/EXECUTE → Use "bash"
4. User says SHOW/READ → Use "read"
5. User asks question without action word → conversation only

EXAMPLES:
- "create a music generator" → {{"intent": "create_file", "actions": [{{"tool": "write", "params": {{"file_path": "music_generator.js"}}, "reason": "create music generator"}}]}}
- "make a beat maker app" → {{"intent": "create_file", "actions": [{{"tool": "write", "params": {{"file_path": "beat_maker.html"}}, "reason": "create beat maker app"}}]}}
- "what's the weather" → {{"intent": "conversation", "actions": []}}

Respond ONLY with JSON (no explanation):
{{
  "intent": "create_file|search_files|run_command|read_file|edit_file|web_search|conversation",
  "actions": [
    {{
      "tool": "tool_name",
      "params": {{...params WITHOUT content}},
      "reason": "brief reason"
    }}
  ]
}}"""

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "nexusai-agent-enhanced:latest",
                    "messages": [
                        {"role": "system", "content": "You are Nexus. You have real tools. Plan actions to accomplish tasks."},
                        {"role": "user", "content": planning_prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.3, "num_ctx": 4096}
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group(0))

                    # If just conversation, return None to skip tool execution
                    if plan.get("intent") == "conversation" and not plan.get("actions"):
                        return None

                    return plan

        except Exception as e:
            print(f"[{self.name}] Planning error: {e}")

        return None

    def _generate_file_content(self, user_request: str, file_path: str) -> Optional[str]:
        """
        Generate actual content for a file based on user request
        """
        # Get file extension to determine type
        extension = Path(file_path).suffix.lower()

        # Build content generation prompt
        content_prompt = f"""Generate COMPLETE, PRODUCTION-READY code for: {file_path}

User wants: {user_request}

File type: {extension}

REQUIREMENTS:
1. Generate ONLY the code - no explanations, no markdown, no "here is"
2. Make it FULLY FUNCTIONAL and SOPHISTICATED
3. Include ALL necessary code - imports, functions, classes, UI elements
4. Use modern, best-practice approaches
5. Add interactivity and features that exceed expectations
6. Make it visually appealing (if UI)

QUALITY STANDARDS:
- .js = Modern ES6+, event handlers, proper DOM manipulation
- .html = Complete structure, inline CSS/JS, responsive design
- .py = Full imports, error handling, clean architecture
- .json = Valid JSON structure
- .md = Well-formatted markdown

CRITICAL: Output ONLY the file content. Start coding NOW:"""

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "nexusai-agent-enhanced:latest",
                    "messages": [
                        {"role": "system", "content": "You are a code generator. Generate complete, working code files. Output ONLY the file content, no explanations."},
                        {"role": "user", "content": content_prompt}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_ctx": 8192  # Larger context for code generation
                    }
                },
                timeout=60  # Longer timeout for content generation
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Clean up markdown code blocks if present
                content = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
                content = re.sub(r'\n```$', '', content, flags=re.MULTILINE)
                content = re.sub(r'```', '', content)  # Remove any remaining backticks

                # Remove common AI response prefixes
                content = re.sub(r'^Here is.*?:\s*\n+', '', content, flags=re.IGNORECASE | re.MULTILINE)
                content = re.sub(r'^Here\'s.*?:\s*\n+', '', content, flags=re.IGNORECASE | re.MULTILINE)

                return content.strip() if content.strip() else None

        except Exception as e:
            print(f"[{self.name}] Content generation error: {e}")

        return None

    def _synthesize_response(self, user_input: str, plan: Dict, results: List[Dict]) -> str:
        """
        Create natural language response from execution results
        """
        # If no tools were used, have natural conversation
        if not results:
            return self._conversational_response(user_input)

        # Build synthesis prompt
        results_summary = []
        for r in results:
            tool = r["tool"]
            result = r["result"]
            action = r["action"]

            summary = f"Tool: {tool}\n"
            summary += f"Purpose: {action.get('reason', 'N/A')}\n"
            summary += f"Success: {result.get('success', False)}\n"

            if result.get("success"):
                if tool == "read":
                    content = result.get("content", "")
                    summary += f"Content preview: {content[:200]}..." if len(content) > 200 else f"Content: {content}"
                elif tool == "write":
                    summary += f"File created: {result.get('path', 'N/A')}"
                elif tool == "bash":
                    output = result.get("output", "")
                    summary += f"Output: {output[:200]}..." if len(output) > 200 else f"Output: {output}"
                elif tool == "glob":
                    files = result.get("files", [])
                    summary += f"Found {len(files)} files: {', '.join(files[:5])}"
                elif tool == "grep":
                    matches = result.get("matches", [])
                    summary += f"Found {len(matches)} matches"
            else:
                summary += f"Error: {result.get('error', 'Unknown')}"

            results_summary.append(summary)

        synthesis_prompt = f"""User asked: "{user_input}"

I executed these tools:
{chr(10).join(results_summary)}

Based on the results, provide a helpful, natural response to the user.
- Be conversational and clear
- Summarize what was accomplished
- If there were errors, explain them
- Be concise but informative

Response:"""

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "nexusai-agent-enhanced:latest",
                    "messages": [
                        {"role": "system", "content": "You are Nexus. Synthesize tool results into helpful responses."},
                        {"role": "user", "content": synthesis_prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.7}
                },
                timeout=30
            )

            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "Task completed.")

        except:
            pass

        # Fallback response
        success_count = sum(1 for r in results if r["result"].get("success"))
        return f"I completed {success_count}/{len(results)} actions successfully."

    def _conversational_response(self, user_input: str) -> str:
        """Generate conversational response when no tools needed"""
        # Build full conversation context
        messages = []

        # Add system message
        messages.append({
            "role": "system",
            "content": "You are Nexus, a helpful and emotionally intelligent AI assistant. You understand context, remember what was said, respond to compliments graciously, and engage naturally. You have tools to create files and execute commands when needed. Be warm, genuine, and conversational."
        })

        # Add conversation history (last 10 messages for context)
        recent = self.conversation_history[-10:] if len(self.conversation_history) > 0 else []
        for msg in recent:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3:latest",  # Better conversational model
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "num_ctx": 4096  # Larger context window
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")
                return content if content else "I'm here to help! What would you like me to do?"

        except Exception as e:
            print(f"[{self.name}] Conversation error: {e}")

        return "I'm here to help! What would you like me to do?"

    # ========== TOOL IMPLEMENTATIONS ==========

    def _tool_bash(self, params: Dict) -> Dict:
        """Execute bash command"""
        command = params.get("command", "")
        if not command:
            return {"success": False, "error": "No command provided"}

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.working_directory)
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _tool_read(self, params: Dict) -> Dict:
        """Read file"""
        file_path = params.get("file_path", "")
        if not file_path:
            return {"success": False, "error": "No file path provided"}

        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = self.working_directory / path

            content = path.read_text(encoding='utf-8')
            return {
                "success": True,
                "content": content,
                "path": str(path)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _tool_write(self, params: Dict) -> Dict:
        """Write file"""
        file_path = params.get("file_path", "")
        content = params.get("content", "")

        if not file_path:
            return {"success": False, "error": "No file path provided"}

        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = self.working_directory / path

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')

            return {
                "success": True,
                "path": str(path),
                "size": len(content)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _tool_edit(self, params: Dict) -> Dict:
        """Edit file with find/replace"""
        file_path = params.get("file_path", "")
        old_text = params.get("old_text", "")
        new_text = params.get("new_text", "")

        if not all([file_path, old_text is not None, new_text is not None]):
            return {"success": False, "error": "Missing parameters"}

        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = self.working_directory / path

            content = path.read_text(encoding='utf-8')

            if old_text not in content:
                return {"success": False, "error": f"Text not found: {old_text[:50]}..."}

            new_content = content.replace(old_text, new_text)
            path.write_text(new_content, encoding='utf-8')

            return {
                "success": True,
                "path": str(path),
                "changes": 1
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _tool_glob(self, params: Dict) -> Dict:
        """Find files by pattern"""
        pattern = params.get("pattern", "*")
        search_path = params.get("path", str(self.working_directory))

        try:
            path = Path(search_path)
            files = [str(f) for f in path.rglob(pattern)][:50]  # Limit results

            return {
                "success": True,
                "files": files,
                "count": len(files)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _tool_grep(self, params: Dict) -> Dict:
        """Search file contents"""
        pattern = params.get("pattern", "")
        search_path = params.get("path", str(self.working_directory))

        if not pattern:
            return {"success": False, "error": "No search pattern provided"}

        try:
            matches = []
            path = Path(search_path)

            # Search in files
            for file_path in path.rglob("*"):
                if file_path.is_file() and file_path.suffix in ['.py', '.txt', '.md', '.json', '.js']:
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        if pattern.lower() in content.lower():
                            matches.append(str(file_path))
                    except:
                        continue

            return {
                "success": True,
                "matches": matches[:50],
                "count": len(matches)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _tool_web_search(self, params: Dict) -> Dict:
        """Search the web"""
        query = params.get("query", "")
        if not query:
            return {"success": False, "error": "No query provided"}

        try:
            from urllib.parse import quote_plus
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json"
            response = requests.get(url, timeout=10)
            data = response.json()

            results = []
            if data.get('Abstract'):
                results.append({
                    "title": data.get('Heading'),
                    "text": data.get('Abstract')
                })

            for topic in data.get('RelatedTopics', [])[:5]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({"text": topic.get('Text')})

            return {
                "success": True,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== UTILITIES ==========

    def _get_recent_context(self, n: int = 5) -> List[Dict]:
        """Get recent conversation for context"""
        return self.conversation_history[-(n*2):] if self.conversation_history else []

    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })


if __name__ == "__main__":
    nexus = NexusActionable()

    print(f"Chat with {nexus.name} - Actionable AI Assistant")
    print("I can actually DO things - create files, run commands, search, etc.")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == 'exit':
                print(f"\n{nexus.name}: Goodbye!")
                break

            if user_input:
                nexus.process(user_input)

        except KeyboardInterrupt:
            print(f"\n\n{nexus.name}: Goodbye!\n")
            break
