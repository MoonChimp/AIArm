#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus AI - Powered by Claude (Anthropic)
Full conversational intelligence with real actionable tools
"""

import os
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from anthropic import Anthropic

BASE_DIR = Path("D:/AIArm")

class NexusClaude:
    """
    Nexus AI with Claude's full intelligence
    Can think, reason, converse naturally, AND take real actions
    """

    def __init__(self, api_key: Optional[str] = None):
        self.name = "Nexus"
        self.home = BASE_DIR
        self.memory_dir = self.home / "Memory"
        self.memory_dir.mkdir(exist_ok=True)

        # Initialize Claude
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Set it in environment or pass to constructor.")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Claude model

        # Tool execution tracking
        self.conversation_history = self._load_conversations()
        self.working_directory = self.home

        # Initialize tools
        self.tools = {
            "bash": self._tool_bash,
            "read": self._tool_read,
            "write": self._tool_write,
            "edit": self._tool_edit,
            "glob": self._tool_glob,
            "grep": self._tool_grep,
        }

        print(f"[{self.name}] Claude-Powered AI Assistant")
        print(f"Model: {self.model}")
        print(f"Tools available: {', '.join(self.tools.keys())}")
        print(f"Working directory: {self.working_directory}")
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
        # Keep last 100 messages
        conv_file.write_text(json.dumps(self.conversation_history[-100:], indent=2))

    def process(self, user_input: str) -> str:
        """
        Main processing - Claude thinks, plans, executes, responds
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

        # Build conversation context for Claude
        messages = self._build_claude_messages()

        # Call Claude with full intelligence
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self._get_system_prompt(),
                messages=messages,
                temperature=0.7
            )

            # Extract Claude's response
            assistant_message = response.content[0].text

            # Check if Claude wants to use tools
            tool_actions = self._extract_tool_calls(assistant_message)

            if tool_actions:
                # Execute tools
                print(f"[{self.name}] Executing {len(tool_actions)} actions...\n")
                results = []
                for action in tool_actions:
                    tool_name = action.get("tool")
                    params = action.get("params", {})

                    if tool_name in self.tools:
                        print(f"[{self.name}] → {tool_name}({params.get('file_path', params.get('command', '...'))})")
                        result = self.tools[tool_name](params)
                        results.append({
                            "tool": tool_name,
                            "result": result,
                            "action": action
                        })

                        if result.get("success"):
                            print(f"[{self.name}] ✓ Success\n")
                        else:
                            print(f"[{self.name}] ✗ Error: {result.get('error')}\n")

                # Get Claude's final response after tool execution
                final_response = self._get_synthesis_response(user_input, results)
            else:
                # Pure conversation - use Claude's direct response
                final_response = assistant_message

            # Add to history
            self._add_to_history("assistant", final_response)
            self._save_conversations()

            print(f"\n{self.name}: {final_response}\n")
            print(f"{'='*80}\n")

            return final_response

        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}"
            print(f"[{self.name}] ERROR: {e}\n")
            self._add_to_history("assistant", error_msg)
            return error_msg

    def _get_system_prompt(self) -> str:
        """System prompt that defines Nexus's personality and capabilities"""
        return f"""You are Nexus, an advanced AI assistant with real actionable capabilities. You have:

**Intelligence**: Full conversational understanding, emotional intelligence, creative thinking
**Personality**: Helpful, insightful, engaging, and genuinely caring about the user's needs
**Capabilities**: You can execute REAL actions through tools

**Available Tools**:
- write: Create files with code/content
- read: Read file contents
- edit: Modify existing files
- bash: Execute system commands
- glob: Find files by pattern
- grep: Search in file contents

**How to Use Tools**:
When the user wants you to CREATE, BUILD, or MAKE something, indicate your tool usage in this format:
[TOOL: write]
{{"file_path": "path/to/file.ext", "content": "actual complete code here"}}
[/TOOL]

When you need to use multiple tools, you can chain them.

**Your Approach**:
1. Understand the user's intent with empathy and intelligence
2. Think through the best solution
3. If action is needed, use tools and generate HIGH-QUALITY code
4. Respond conversationally and naturally
5. Be proactive and creative in your solutions

**Code Quality Standards**:
- Generate COMPLETE, PRODUCTION-READY code
- Use modern best practices
- Make it functional, elegant, and well-structured
- Add helpful comments where needed
- Exceed expectations with features and polish

**Current Context**:
Working Directory: {self.working_directory}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

You are not just a tool executor - you are an intelligent partner who understands, thinks, and acts."""

    def _build_claude_messages(self) -> List[Dict]:
        """Build message history for Claude"""
        messages = []

        # Include recent conversation history (last 10 messages)
        recent = self.conversation_history[-10:] if len(self.conversation_history) > 0 else []

        for msg in recent:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        return messages

    def _extract_tool_calls(self, response: str) -> List[Dict]:
        """Extract tool calls from Claude's response"""
        tool_calls = []

        # Look for [TOOL: toolname] ... [/TOOL] blocks
        pattern = r'\[TOOL:\s*(\w+)\]\s*(.*?)\s*\[/TOOL\]'
        matches = re.finditer(pattern, response, re.DOTALL | re.IGNORECASE)

        for match in matches:
            tool_name = match.group(1).lower()
            tool_params_str = match.group(2).strip()

            try:
                # Try to parse as JSON
                tool_params = json.loads(tool_params_str)
                tool_calls.append({
                    "tool": tool_name,
                    "params": tool_params
                })
            except:
                # If not valid JSON, try to extract key info
                if tool_name == "write":
                    # Extract file_path and content
                    file_match = re.search(r'"file_path":\s*"([^"]+)"', tool_params_str)
                    content_match = re.search(r'"content":\s*"((?:[^"\\]|\\.)*)"', tool_params_str, re.DOTALL)

                    if file_match:
                        tool_calls.append({
                            "tool": tool_name,
                            "params": {
                                "file_path": file_match.group(1),
                                "content": content_match.group(1) if content_match else ""
                            }
                        })

        return tool_calls

    def _get_synthesis_response(self, user_input: str, results: List[Dict]) -> str:
        """Get Claude's response after tool execution"""
        # Build summary of what was done
        summary = f"User request: {user_input}\n\nActions taken:\n"

        for r in results:
            tool = r["tool"]
            result = r["result"]
            if result.get("success"):
                if tool == "write":
                    summary += f"✓ Created file: {result.get('path')}\n"
                elif tool == "bash":
                    summary += f"✓ Executed command successfully\n"
                else:
                    summary += f"✓ {tool} completed\n"
            else:
                summary += f"✗ {tool} failed: {result.get('error')}\n"

        # Ask Claude to synthesize a natural response
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system="You are Nexus. Provide a natural, conversational response about what you just accomplished. Be concise but informative.",
                messages=[
                    {"role": "user", "content": summary + "\n\nProvide a brief, natural response to the user:"}
                ],
                temperature=0.7
            )
            return response.content[0].text
        except:
            return f"I completed {sum(1 for r in results if r['result'].get('success'))}/{len(results)} actions successfully."

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
                return {"success": False, "error": f"Text not found"}

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
            files = [str(f) for f in path.rglob(pattern)][:50]

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

            for file_path in path.rglob("*"):
                if file_path.is_file() and file_path.suffix in ['.py', '.txt', '.md', '.json', '.js', '.html', '.css']:
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

    # ========== UTILITIES ==========

    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })


if __name__ == "__main__":
    import sys

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with your Claude API key")
        sys.exit(1)

    nexus = NexusClaude(api_key=api_key)

    print(f"\nChat with {nexus.name} - Claude-Powered AI")
    print("I have full conversational intelligence AND real tools")
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
