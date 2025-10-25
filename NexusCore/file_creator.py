#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File Creator - Generates code/content and saves to files
Used by Orchestrator for creating apps, scripts, etc.
"""

import requests
import re
from pathlib import Path
from typing import Dict

class FileCreator:
    """
    Creates files with AI-generated content
    """

    def __init__(self, ollama_base="http://localhost:11434"):
        self.ollama_base = ollama_base
        self.code_model = "qwen2.5-coder:latest"  # Best for code generation
        self.output_dir = Path("D:/AIArm/Generated/Code")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_file(self, user_request: str, file_path: str = None) -> Dict:
        """
        Generate content and create a file
        """
        # Determine file path if not provided
        if not file_path:
            file_path = self._determine_file_path(user_request)

        # Generate content
        content = self._generate_content(user_request, file_path)

        if not content:
            return {
                "status": "error",
                "message": "Failed to generate content"
            }

        # Write to file
        try:
            full_path = self.output_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')

            return {
                "status": "success",
                "file_path": str(full_path),
                "size": len(content),
                "message": f"Created {file_path}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to write file: {str(e)}"
            }

    def _determine_file_path(self, user_request: str) -> str:
        """
        Determine appropriate filename based on request
        """
        # Simple heuristics
        if "music" in user_request.lower() or "beat" in user_request.lower():
            return "music_generator.html"
        elif "game" in user_request.lower():
            return "game.html"
        elif "calculator" in user_request.lower():
            return "calculator.html"
        elif ".py" in user_request.lower() or "python" in user_request.lower():
            return "script.py"
        elif ".js" in user_request.lower() or "javascript" in user_request.lower():
            return "app.js"
        else:
            return "app.html"

    def _generate_content(self, user_request: str, file_path: str) -> str:
        """
        Generate actual code content using AI
        """
        extension = Path(file_path).suffix.lower()

        prompt = f"""Create a COMPLETE, WORKING, PRODUCTION-READY file for: {file_path}

User wants: {user_request}

Requirements:
1. Output ONLY the code - no explanations, no markdown
2. Make it FULLY FUNCTIONAL with ALL features
3. For HTML: include inline CSS and JavaScript in ONE file
4. For JS: include all necessary code
5. Make it interactive and feature-rich
6. Add comments explaining key parts

File type: {extension}

Generate the COMPLETE file content NOW (start coding immediately):"""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.code_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a code generator. Output ONLY code, no explanations. Make it complete and functional."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_ctx": 8192
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Clean up
                content = self._cleanup_code(content)

                return content

        except Exception as e:
            print(f"[FileCreator] Generation error: {e}")

        return None

    def _cleanup_code(self, content: str) -> str:
        """
        Remove markdown wrappers and explanatory text
        """
        # Remove markdown code blocks
        content = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n```$', '', content, flags=re.MULTILINE)
        content = re.sub(r'```', '', content)

        # Remove common prefixes
        content = re.sub(r'^Here is.*?:\s*\n+', '', content, flags=re.IGNORECASE | re.MULTILINE)
        content = re.sub(r'^Here\'s.*?:\s*\n+', '', content, flags=re.IGNORECASE | re.MULTILINE)

        return content.strip()
