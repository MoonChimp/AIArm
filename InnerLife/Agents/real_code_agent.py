#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REAL Code Execution Agent - Actually runs code
Executes Python and Node.js code safely with timeout protection
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import subprocess
import tempfile
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Agents.agent_base import Agent

class RealCodeAgent(Agent):
    """Agent that creates AND executes complete applications"""

    def __init__(self):
        super().__init__(
            name="CodeGeneration",
            description="Creates full websites, webapps, mobile apps, and executes code",
            capabilities=[
                "Generate complete websites (HTML/CSS/JS)",
                "Create React/Vue/Angular web applications",
                "Build React Native mobile apps",
                "Generate Python applications",
                "Create Node.js backends",
                "Execute and test code",
                "Install packages (pip, npm)"
            ]
        )
        self.execution_history = []
        self.code_dir = Path("D:/AIArm/Generated/Code")
        self.code_dir.mkdir(exist_ok=True, parents=True)
        self.max_execution_time = 30  # 30 second timeout
        self.ollama_base = "http://localhost:11434"
        self.code_model = "nexusai-a0-coder1.0:latest"  # Merged model: NexusAI + Qwen + CodeLlama

    def process(self, user_request, context=None, options=None):
        """Generate or execute code based on user request"""
        if not self.active:
            return {"status": "error", "message": "Agent is not active"}

        self.last_used = datetime.now().isoformat()
        options = options or {}

        # Detect if this is a creation request or execution request
        request_lower = user_request.lower()

        creation_keywords = ["create", "build", "make", "generate", "develop", "write"]
        app_keywords = ["website", "webapp", "app", "application", "mobile app", "react", "vue", "angular"]

        is_creation = any(kw in request_lower for kw in creation_keywords)
        is_app = any(kw in request_lower for kw in app_keywords)

        if is_creation and is_app:
            # Generate a complete application
            print(f"[CodeGeneration] Creating application: {user_request[:60]}...")
            return self._generate_application(user_request, options)
        elif "```" in user_request or options.get("execute", False):
            # Execute provided code
            code = self._extract_code(user_request)
            language = self._detect_language(code, user_request)
            print(f"[CodeExecution] Executing {language} code ({len(code)} chars)")
            return self._execute_code(code, language, options)
        else:
            # Generate code snippet
            print(f"[CodeGeneration] Generating code for: {user_request[:60]}...")
            return self._generate_code_snippet(user_request, options)

    def _generate_application(self, user_request, options):
        """Generate a complete application (website/webapp/mobile app)"""
        import requests

        # Detect app type
        app_type = self._detect_app_type(user_request)

        print(f"[CodeGeneration] App Type: {app_type}")

        # Generate complete application code
        prompt = self._build_app_generation_prompt(user_request, app_type)

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.code_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are an expert {app_type} developer. Generate complete, functional, production-ready code. Include ALL necessary files, dependencies, and setup instructions."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_ctx": 16384
                    }
                },
                timeout=180
            )

            if response.status_code == 200:
                data = response.json()
                generated_content = data.get("message", {}).get("content", "")

                # Save the application
                result = self._save_application(user_request, app_type, generated_content)
                return result
            else:
                return {
                    "status": "error",
                    "message": f"Code generation failed: {response.status_code}"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Application generation failed: {str(e)}"
            }

    def _detect_app_type(self, request):
        """Detect what type of app to generate"""
        request_lower = request.lower()

        # ML/AI specific detection (highest priority)
        ml_keywords = ["machine learning", "ml model", "neural network", "deep learning", "tensorflow", "pytorch", "scikit", "train", "dataset", "classifier", "regression", "lstm", "cnn", "transformer", "nlp", "computer vision"]
        if any(kw in request_lower for kw in ml_keywords):
            return "ml-python"

        # Other app types
        if any(kw in request_lower for kw in ["react native", "mobile app", "ios", "android"]):
            return "react-native"
        elif "react" in request_lower:
            return "react-web"
        elif "vue" in request_lower:
            return "vue"
        elif "angular" in request_lower:
            return "angular"
        elif any(kw in request_lower for kw in ["backend", "api", "server", "node"]):
            return "nodejs-backend"
        elif "python" in request_lower:
            return "python-app"
        else:
            return "html-website"

    def _build_app_generation_prompt(self, user_request, app_type):
        """Build prompt for application generation"""
        templates = {
            "html-website": """Create a complete, functional website for: {request}

Generate:
1. index.html - Complete HTML structure
2. styles.css - Full styling
3. app.js - All JavaScript functionality
4. README.md - Setup and usage instructions

Requirements:
- Modern, responsive design
- Clean, professional UI
- Fully functional features
- No placeholder code
- Production-ready

Provide the complete code for each file.""",

            "react-web": """Create a complete React web application for: {request}

Generate:
1. index.html - Entry point
2. App.jsx - Main component with ALL features
3. package.json - All dependencies
4. README.md - Setup instructions

Requirements:
- Functional components with hooks
- Complete implementation (no TODOs)
- Modern React patterns
- Responsive design
- All features working

Provide complete, working code.""",

            "react-native": """Create a complete React Native mobile app for: {request}

Generate:
1. App.js - Complete application with all screens
2. package.json - All dependencies
3. README.md - Setup and run instructions

Requirements:
- Functional components
- Complete navigation
- All features implemented
- Production-ready code
- iOS and Android compatible

Provide complete, working code.""",

            "nodejs-backend": """Create a complete Node.js backend API for: {request}

Generate:
1. server.js - Complete Express server
2. package.json - All dependencies
3. README.md - API documentation

Requirements:
- RESTful API endpoints
- Error handling
- Input validation
- Complete implementation
- Production-ready

Provide complete, working code.""",

            "python-app": """Create a complete Python application for: {request}

Generate:
1. main.py - Complete application code
2. requirements.txt - All dependencies
3. README.md - Usage instructions

Requirements:
- Clean, modular code
- Error handling
- Complete features
- Production-ready
- Well-documented

Provide complete, working code.""",

            "ml-python": """Create a complete Machine Learning application for: {request}

Generate:
1. model.py - ML model definition and architecture
2. train.py - Training script with data loading, training loop, and checkpointing
3. predict.py or inference.py - Inference/prediction script
4. data_loader.py - Data loading and preprocessing utilities
5. requirements.txt - All ML dependencies (torch/tensorflow/sklearn/etc)
6. README.md - Setup, training, and usage instructions
7. config.py or config.yaml - Hyperparameters and configuration

Requirements:
- Use appropriate ML framework (PyTorch, TensorFlow, or scikit-learn based on task)
- Include data preprocessing and augmentation if applicable
- Implement proper train/validation split
- Add model evaluation metrics
- Include model saving/loading functionality
- Add GPU support where applicable (CUDA checks)
- Use best practices: batch processing, learning rate scheduling, early stopping
- Provide example usage and expected input/output formats
- Include visualization code (training curves, confusion matrix, etc.)
- Production-ready, well-documented code

For neural networks:
- Define complete architecture (layers, activations, etc.)
- Include loss function and optimizer configuration
- Add tensorboard or wandb logging if beneficial

For classical ML:
- Include feature engineering steps
- Add cross-validation if applicable
- Provide feature importance analysis

Provide COMPLETE, FUNCTIONAL code that can actually train and make predictions."""
        }

        template = templates.get(app_type, templates["html-website"])
        return template.format(request=user_request)

    def _save_application(self, request, app_type, generated_content):
        """Save generated application to files"""
        import re

        app_id = str(uuid.uuid4())[:8]
        app_name = re.sub(r'[^a-zA-Z0-9_-]', '_', request[:30]).strip('_')
        app_dir = self.code_dir / f"{app_name}_{app_id}"
        app_dir.mkdir(exist_ok=True, parents=True)

        # Extract files from generated content
        files_saved = []

        # Pattern to match filename comments or markdown
        patterns = [
            r'(?:```|//|#|<!--|/\*)\s*(?:filename:|file:)?\s*([a-zA-Z0-9._/-]+)\s*(?:```|-->|\*/)?',
            r'(?:```|)([a-zA-Z0-9._/-]+)(?:```|)\s*:\s*```'
        ]

        # Try to extract multiple files
        parts = re.split(r'(?:```[\w]*\n)|(?:\n```)', generated_content)

        current_filename = None
        file_content = ""

        for part in parts:
            # Check if this part contains a filename
            for pattern in patterns:
                match = re.search(pattern, part)
                if match:
                    # Save previous file
                    if current_filename and file_content.strip():
                        filepath = app_dir / current_filename
                        filepath.parent.mkdir(exist_ok=True, parents=True)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(file_content.strip())
                        files_saved.append(current_filename)

                    current_filename = match.group(1)
                    file_content = part[match.end():]
                    break
            else:
                if current_filename:
                    file_content += part

        # Save last file
        if current_filename and file_content.strip():
            filepath = app_dir / current_filename
            filepath.parent.mkdir(exist_ok=True, parents=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file_content.strip())
            files_saved.append(current_filename)

        # If no files extracted, save as single file
        if not files_saved:
            ext = {
                "react-web": "jsx",
                "react-native": "js",
                "python-app": "py",
                "ml-python": "py",
                "nodejs-backend": "js"
            }.get(app_type, "html")

            filepath = app_dir / f"app.{ext}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(generated_content)
            files_saved.append(f"app.{ext}")

        # Save README if not already saved
        if not any("README" in f for f in files_saved):
            readme = app_dir / "README.md"
            with open(readme, 'w', encoding='utf-8') as f:
                f.write(f"# {app_name}\n\n")
                f.write(f"Generated application for: {request}\n\n")
                f.write(f"Type: {app_type}\n\n")
                f.write(f"Files:\n")
                for file in files_saved:
                    f.write(f"- {file}\n")
            files_saved.append("README.md")

        print(f"[CodeGeneration] Application saved to {app_dir}")
        print(f"[CodeGeneration] Files: {', '.join(files_saved)}")

        return {
            "status": "success",
            "app_type": app_type,
            "directory": str(app_dir),
            "files": files_saved,
            "message": f"Created {app_type} application in {app_dir.name}",
            "path": str(app_dir)
        }

    def _generate_code_snippet(self, user_request, options):
        """Generate a code snippet (not full app)"""
        import requests

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.code_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert programmer. Generate clean, functional code snippets."
                        },
                        {
                            "role": "user",
                            "content": f"Write code for: {user_request}"
                        }
                    ],
                    "stream": False,
                    "options": {"temperature": 0.3}
                },
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                code = data.get("message", {}).get("content", "")

                # Save snippet
                snippet_id = str(uuid.uuid4())[:8]
                filepath = self.code_dir / f"snippet_{snippet_id}.txt"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# Request: {user_request}\n\n")
                    f.write(code)

                return {
                    "status": "success",
                    "code": code,
                    "filepath": str(filepath),
                    "message": f"Code snippet generated and saved to snippet_{snippet_id}.txt"
                }
            else:
                return {
                    "status": "error",
                    "message": "Code generation failed"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _detect_language(self, code, context=""):
        """Detect programming language"""
        if "import " in code or "def " in code or "print(" in code:
            return "python"
        elif "const " in code or "function" in code or "=>" in code:
            return "javascript"
        else:
            return "python"  # default

    def _execute_code(self, code, language, options):
        """Execute code"""
        if language == "python":
            return self._execute_python(code, options)
        elif language in ["javascript", "js", "node"]:
            return self._execute_javascript(code, options)
        else:
            return {"status": "error", "message": f"Unsupported language: {language}"}

    def _extract_code(self, text):
        """Extract code from markdown code blocks"""
        import re

        # Try to extract from code blocks
        patterns = [
            r'```(?:python|py)\n(.*?)```',
            r'```(?:javascript|js|node)\n(.*?)```',
            r'```\n(.*?)```',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()

        # If no code block, return as-is
        return text.strip()

    def _execute_python(self, code, options):
        """Execute Python code"""
        # Create temporary file
        exec_id = str(uuid.uuid4())[:8]
        temp_file = self.code_dir / f"exec_{exec_id}.py"

        try:
            # Write code to file
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)

            # Execute with timeout
            result = subprocess.run(
                [sys.executable, str(temp_file)],
                capture_output=True,
                text=True,
                timeout=self.max_execution_time,
                cwd=str(self.code_dir)
            )

            output = {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "language": "python",
                "file": str(temp_file)
            }

            print(f"[CodeExecution] Python execution completed (return code: {result.returncode})")

            # Save successful code
            if result.returncode == 0 and options.get("save", False):
                saved_file = self.code_dir / f"success_{exec_id}.py"
                temp_file.rename(saved_file)
                output["saved_to"] = str(saved_file)
            elif not options.get("keep_temp", False):
                temp_file.unlink(missing_ok=True)

            return output

        except subprocess.TimeoutExpired:
            temp_file.unlink(missing_ok=True)
            return {
                "status": "error",
                "message": f"Execution timeout ({self.max_execution_time}s)",
                "language": "python"
            }
        except Exception as e:
            temp_file.unlink(missing_ok=True)
            return {
                "status": "error",
                "message": str(e),
                "language": "python"
            }

    def _execute_javascript(self, code, options):
        """Execute JavaScript/Node.js code"""
        exec_id = str(uuid.uuid4())[:8]
        temp_file = self.code_dir / f"exec_{exec_id}.js"

        try:
            # Write code to file
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)

            # Execute with Node.js
            result = subprocess.run(
                ["node", str(temp_file)],
                capture_output=True,
                text=True,
                timeout=self.max_execution_time,
                cwd=str(self.code_dir)
            )

            output = {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "language": "javascript",
                "file": str(temp_file)
            }

            print(f"[CodeExecution] JavaScript execution completed (return code: {result.returncode})")

            # Save successful code
            if result.returncode == 0 and options.get("save", False):
                saved_file = self.code_dir / f"success_{exec_id}.js"
                temp_file.rename(saved_file)
                output["saved_to"] = str(saved_file)
            elif not options.get("keep_temp", False):
                temp_file.unlink(missing_ok=True)

            return output

        except subprocess.TimeoutExpired:
            temp_file.unlink(missing_ok=True)
            return {
                "status": "error",
                "message": f"Execution timeout ({self.max_execution_time}s)",
                "language": "javascript"
            }
        except Exception as e:
            temp_file.unlink(missing_ok=True)
            return {
                "status": "error",
                "message": str(e),
                "language": "javascript"
            }

    def execute_shell_command(self, command, options=None):
        """Execute a shell command (use with caution)"""
        options = options or {}

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=options.get("timeout", self.max_execution_time),
                cwd=options.get("cwd", str(self.code_dir))
            )

            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "command": command
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": "Command timeout",
                "command": command
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "command": command
            }

    def install_package(self, package_name, package_manager="pip"):
        """Install a Python or Node package"""
        try:
            if package_manager == "pip":
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package_name],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
            elif package_manager == "npm":
                result = subprocess.run(
                    ["npm", "install", package_name],
                    capture_output=True,
                    text=True,
                    timeout=120,
                    cwd=str(self.code_dir)
                )
            else:
                return {
                    "status": "error",
                    "message": f"Unknown package manager: {package_manager}"
                }

            return {
                "status": "success" if result.returncode == 0 else "error",
                "package": package_name,
                "manager": package_manager,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "package": package_name
            }
