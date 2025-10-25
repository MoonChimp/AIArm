#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REAL Agent Framework - Claude-like capabilities
This gives NexusAI the ACTUAL tools that Claude uses:
- Bash execution
- File operations (Read, Write, Edit)
- File search (Glob, Grep)
- Web operations (WebFetch, WebSearch)
- Multi-step task planning

This is a REAL agent, not a toy.
"""

import sys
import os
import subprocess
import json
import re
import requests
from pathlib import Path
from datetime import datetime
import shutil
import glob as python_glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class RealAgentFramework(Agent):
    """
    REAL agent with Claude-like tool capabilities
    This is what makes an agent actually intelligent
    """

    def __init__(self):
        super().__init__(
            name="RealAgent",
            description="Full agent with Bash, file ops, web access - like Claude",
            capabilities=[
                "Execute bash commands",
                "Read/Write/Edit files",
                "Search files (Glob/Grep)",
                "Fetch web content",
                "Multi-step task planning",
                "Strategic tool use",
                "Actual learning and adaptation"
            ]
        )

        self.working_dir = Path("D:/AIArm")
        self.tools_history = []

    def process(self, task, context=None, options=None):
        """
        Process a task using available tools
        This is where the REAL agent intelligence happens
        """
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        print(f"[RealAgent] Processing task: {task[:80]}...")

        try:
            # Use Ollama to plan approach
            plan = self._plan_task(task, context, options)

            if plan["status"] != "success":
                return plan

            # Execute the plan using tools
            result = self._execute_plan(plan["steps"], task)

            return result

        except Exception as e:
            print(f"[RealAgent] Error: {e}")
            return {
                "status": "error",
                "message": f"Task failed: {str(e)}"
            }

    def _plan_task(self, task, context, options):
        """Use Ollama to plan how to accomplish the task"""
        try:
            planning_prompt = f"""You are a strategic AI agent with these tools available:

TOOLS:
1. bash(command) - Execute shell commands
2. read_file(path) - Read file contents
3. write_file(path, content) - Write/create files
4. edit_file(path, old_text, new_text) - Edit existing files
5. glob(pattern, path) - Find files by pattern
6. grep(pattern, path, options) - Search file contents
7. web_fetch(url) - Fetch web content
8. web_search(query) - Search the web

TASK: {task}

Create a step-by-step plan using these tools. Be strategic and efficient.
Format as JSON array of steps:
[
  {{"tool": "bash", "args": {{"command": "ls"}}, "reason": "why"}},
  ...
]

Plan:"""

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "nexusai-agent-enhanced:latest",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a strategic planning AI. Create efficient, correct tool usage plans."
                        },
                        {
                            "role": "user",
                            "content": planning_prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Lower for planning
                        "num_ctx": 8192
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                plan_text = data.get("message", {}).get("content", "")

                # Extract JSON from response
                steps = self._extract_plan_json(plan_text)

                return {
                    "status": "success",
                    "steps": steps,
                    "raw_plan": plan_text
                }
            else:
                return {
                    "status": "error",
                    "message": "Planning failed"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Planning error: {str(e)}"
            }

    def _extract_plan_json(self, text):
        """Extract JSON plan from model output"""
        try:
            # Try to find JSON array
            json_match = re.search(r'\[.*\]', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        # Fallback: Create simple plan from text
        return [
            {
                "tool": "bash",
                "args": {"command": "echo 'Plan parsing failed, executing basic approach'"},
                "reason": "Fallback execution"
            }
        ]

    def _execute_plan(self, steps, original_task):
        """Execute the planned steps using actual tools"""
        results = []

        print(f"[RealAgent] Executing {len(steps)} steps...")

        for i, step in enumerate(steps, 1):
            tool = step.get("tool", "unknown")
            args = step.get("args", {})
            reason = step.get("reason", "")

            print(f"[RealAgent] Step {i}/{len(steps)}: {tool} - {reason}")

            try:
                if tool == "bash":
                    result = self.tool_bash(**args)
                elif tool == "read_file":
                    result = self.tool_read_file(**args)
                elif tool == "write_file":
                    result = self.tool_write_file(**args)
                elif tool == "edit_file":
                    result = self.tool_edit_file(**args)
                elif tool == "glob":
                    result = self.tool_glob(**args)
                elif tool == "grep":
                    result = self.tool_grep(**args)
                elif tool == "web_fetch":
                    result = self.tool_web_fetch(**args)
                elif tool == "web_search":
                    result = self.tool_web_search(**args)
                else:
                    result = {"status": "error", "message": f"Unknown tool: {tool}"}

                results.append({
                    "step": i,
                    "tool": tool,
                    "result": result
                })

                # Log tool use
                self.tools_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "tool": tool,
                    "args": args,
                    "result": result
                })

            except Exception as e:
                results.append({
                    "step": i,
                    "tool": tool,
                    "error": str(e)
                })

        return {
            "status": "success",
            "task": original_task,
            "steps_completed": len(results),
            "results": results
        }

    # ========== ACTUAL TOOL IMPLEMENTATIONS ==========

    def tool_bash(self, command, timeout=30, cwd=None):
        """Execute bash command - REAL system access"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd or str(self.working_dir)
            )

            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Command timeout"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tool_read_file(self, path, offset=0, limit=None):
        """Read file contents"""
        try:
            filepath = Path(path)

            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            if offset > 0:
                lines = lines[offset:]
            if limit:
                lines = lines[:limit]

            return {
                "status": "success",
                "content": ''.join(lines),
                "lines": len(lines),
                "path": str(filepath)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tool_write_file(self, path, content):
        """Write file - creates or overwrites"""
        try:
            filepath = Path(path)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                "status": "success",
                "path": str(filepath),
                "bytes_written": len(content)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tool_edit_file(self, path, old_string, new_string, replace_all=False):
        """Edit file - find and replace"""
        try:
            filepath = Path(path)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if replace_all:
                new_content = content.replace(old_string, new_string)
                count = content.count(old_string)
            else:
                new_content = content.replace(old_string, new_string, 1)
                count = 1 if old_string in content else 0

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return {
                "status": "success",
                "path": str(filepath),
                "replacements": count
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tool_glob(self, pattern, path=None):
        """Find files by pattern"""
        try:
            search_path = Path(path) if path else self.working_dir
            full_pattern = str(search_path / pattern)

            matches = python_glob.glob(full_pattern, recursive=True)

            return {
                "status": "success",
                "matches": matches[:100],  # Limit results
                "count": len(matches)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tool_grep(self, pattern, path=None, case_insensitive=False, context_lines=0):
        """Search file contents"""
        try:
            search_path = Path(path) if path else self.working_dir

            if search_path.is_file():
                files = [search_path]
            else:
                files = list(search_path.rglob('*.py')) + list(search_path.rglob('*.js')) + list(search_path.rglob('*.md'))

            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(pattern, flags)

            results = []

            for file in files[:100]:  # Limit files
                try:
                    with open(file, 'r', encoding='utf-8', errors='replace') as f:
                        lines = f.readlines()

                    for i, line in enumerate(lines):
                        if regex.search(line):
                            results.append({
                                "file": str(file),
                                "line": i + 1,
                                "content": line.strip()
                            })

                            if len(results) >= 50:  # Limit results
                                break

                except:
                    continue

            return {
                "status": "success",
                "matches": results,
                "count": len(results)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tool_web_fetch(self, url, timeout=15):
        """Fetch content from URL"""
        try:
            response = requests.get(url, timeout=timeout, headers={
                'User-Agent': 'Mozilla/5.0 NexusAI Agent'
            })

            return {
                "status": "success",
                "url": url,
                "status_code": response.status_code,
                "content": response.text[:10000],  # First 10k chars
                "full_length": len(response.text)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tool_web_search(self, query, max_results=10):
        """Search the web using DuckDuckGo"""
        try:
            from urllib.parse import quote_plus

            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1"
            response = requests.get(url, timeout=15)

            if response.status_code == 200:
                data = response.json()
                results = []

                if data.get('Abstract'):
                    results.append({
                        "title": data.get('Heading', query),
                        "url": data.get('AbstractURL', ''),
                        "snippet": data.get('Abstract', '')
                    })

                for topic in data.get('RelatedTopics', []):
                    if isinstance(topic, dict) and 'Text' in topic:
                        results.append({
                            "title": topic.get('Text', '')[:100],
                            "url": topic.get('FirstURL', ''),
                            "snippet": topic.get('Text', '')
                        })

                return {
                    "status": "success",
                    "query": query,
                    "results": results[:max_results]
                }

        except Exception as e:
            return {"status": "error", "message": str(e)}
