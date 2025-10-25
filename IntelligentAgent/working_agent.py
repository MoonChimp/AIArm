#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WORKING Intelligent Agent
This ACTUALLY works because it uses deterministic intelligence, not hoping Ollama figures it out
"""

import sys
import os
import json
import requests
import subprocess
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus

class WorkingAgent:
    """An agent that ACTUALLY works"""

    def __init__(self):
        self.name = "NexusAI"
        self.conversation = []
        self.working_dir = Path("D:/AIArm")

        print(f"[{self.name}] Intelligent Assistant Ready")

    def process(self, user_input):
        """Process user input - ACTUALLY intelligently"""
        print(f"\n{'='*80}")
        print(f"You: {user_input}")
        print(f"{'='*80}\n")

        # INTELLIGENT INTENT DETECTION (deterministic, reliable)
        intent = self._detect_intent(user_input)

        print(f"[{self.name}] Intent detected: {intent['action']}")

        # Execute based on intent
        if intent['action'] == 'web_search':
            result = self._do_web_search(intent['query'])
        elif intent['action'] == 'bash':
            result = self._do_bash(intent['command'])
        elif intent['action'] == 'read_file':
            result = self._do_read_file(intent['path'])
        elif intent['action'] == 'write_file':
            result = self._do_write_file(intent['path'], intent['content'])
        elif intent['action'] == 'list_directory':
            result = self._do_list_directory(intent['path'])
        elif intent['action'] == 'execute_code':
            result = self._do_execute_code(intent['code'], intent['language'])
        elif intent['action'] == 'conversation':
            result = self._do_conversation(user_input)
        else:
            result = "I'm not sure how to help with that."

        # Add to conversation history
        self.conversation.append({"user": user_input, "assistant": result})

        print(f"\n[{self.name}]: {result}\n")
        print(f"{'='*80}\n")

        return result

    def _detect_intent(self, text):
        """Detect what the user wants - RELIABLY"""
        text_lower = text.lower()

        # Web search patterns
        if any(word in text_lower for word in ['search', 'google', 'find', 'look up', 'search for']):
            # Extract query
            for pattern in ['search for ', 'google ', 'find ', 'look up ']:
                if pattern in text_lower:
                    query = text[text_lower.find(pattern) + len(pattern):].strip()
                    return {'action': 'web_search', 'query': query}
            return {'action': 'web_search', 'query': text}

        # Directory listing
        if any(phrase in text_lower for phrase in ['what\'s in', 'whats in', 'list', 'show me', 'contents of']):
            # Extract path
            path_match = re.search(r'[A-Z]:\\[\w\\]*', text) or re.search(r'/[\w/]*', text)
            path = path_match.group() if path_match else '.'
            return {'action': 'list_directory', 'path': path}

        # File operations
        if 'read' in text_lower and 'file' in text_lower:
            path_match = re.search(r'[\'"]([^\'"]+)[\'"]', text) or re.search(r'(\S+\.\w+)', text)
            path = path_match.group(1) if path_match else ''
            return {'action': 'read_file', 'path': path}

        if any(word in text_lower for word in ['create file', 'write file', 'save to']):
            # Extract path and content
            path = ''
            content = ''
            # Simple extraction - can be improved
            return {'action': 'write_file', 'path': path, 'content': content}

        # Code execution
        if '```' in text or any(word in text_lower for word in ['run code', 'execute', 'run this']):
            code = self._extract_code(text)
            lang = 'python' if 'python' in text_lower else 'javascript' if 'javascript' in text_lower else 'python'
            return {'action': 'execute_code', 'code': code, 'language': lang}

        # Bash command
        if any(word in text_lower for word in ['run command', 'execute command', 'bash', 'cmd']):
            command = text  # Extract command
            return {'action': 'bash', 'command': command}

        # Default: conversation
        return {'action': 'conversation', 'text': text}

    def _do_web_search(self, query):
        """Actually search the web"""
        try:
            print(f"[{self.name}] Searching for: {query}")

            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=10)
            data = response.json()

            results = []

            # Get abstract
            if data.get('Abstract'):
                results.append(f"**{data.get('Heading', 'Result')}**\n{data.get('Abstract')}\nSource: {data.get('AbstractURL', 'N/A')}")

            # Get topics
            for topic in data.get('RelatedTopics', [])[:5]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append(f"• {topic.get('Text')}\nLink: {topic.get('FirstURL', 'N/A')}")

            if results:
                return f"Search results for '{query}':\n\n" + "\n\n".join(results)
            else:
                return f"No results found for '{query}'. DuckDuckGo might not have indexed this topic well."

        except Exception as e:
            return f"Search failed: {str(e)}"

    def _do_bash(self, command):
        """Execute bash command"""
        try:
            print(f"[{self.name}] Running: {command}")

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.working_dir)
            )

            if result.stdout:
                return f"Command output:\n{result.stdout}"
            elif result.stderr:
                return f"Command error:\n{result.stderr}"
            else:
                return "Command executed successfully (no output)"

        except Exception as e:
            return f"Command failed: {str(e)}"

    def _do_list_directory(self, path):
        """List directory contents"""
        try:
            print(f"[{self.name}] Listing: {path}")

            result = subprocess.run(
                f'dir "{path}"' if os.name == 'nt' else f'ls -la "{path}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.stdout:
                return f"Contents of {path}:\n\n{result.stdout}"
            else:
                return f"Could not list {path}"

        except Exception as e:
            return f"Failed to list directory: {str(e)}"

    def _do_read_file(self, path):
        """Read file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File contents of {path}:\n\n{content[:2000]}"  # Limit size
        except Exception as e:
            return f"Could not read file: {str(e)}"

    def _do_write_file(self, path, content):
        """Write file"""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Could not write file: {str(e)}"

    def _do_execute_code(self, code, language):
        """Execute code"""
        try:
            if language == 'python':
                temp_file = self.working_dir / f"temp_{datetime.now().timestamp()}.py"
                temp_file.write_text(code)
                result = subprocess.run([sys.executable, str(temp_file)], capture_output=True, text=True, timeout=30)
                temp_file.unlink()
            else:
                temp_file = self.working_dir / f"temp_{datetime.now().timestamp()}.js"
                temp_file.write_text(code)
                result = subprocess.run(['node', str(temp_file)], capture_output=True, text=True, timeout=30)
                temp_file.unlink()

            output = result.stdout if result.stdout else result.stderr
            return f"Code execution result:\n{output}"

        except Exception as e:
            return f"Code execution failed: {str(e)}"

    def _do_conversation(self, text):
        """Have a conversation using Ollama"""
        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "nexusai-agent-enhanced:latest",
                    "messages": [
                        {"role": "system", "content": "You are NexusAI, a helpful and intelligent AI assistant."},
                        *[{"role": m.get("user") and "user" or "assistant", "content": m.get("user") or m.get("assistant")}
                          for m in self.conversation[-5:]],
                        {"role": "user", "content": text}
                    ],
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "I'm not sure how to respond.")
            else:
                return "I'm having trouble thinking right now."

        except Exception as e:
            return f"Conversation error: {str(e)}"

    def _extract_code(self, text):
        """Extract code from text"""
        code_match = re.search(r'```(?:\w+)?\n(.*?)```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        return text


if __name__ == "__main__":
    agent = WorkingAgent()

    print(f"{agent.name} - Working Intelligent Assistant")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() == 'exit':
                break
            if user_input:
                agent.process(user_input)
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
