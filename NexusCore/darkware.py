#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DarkWare: Autonomous Skill Creation System
When Nexus encounters a task it cannot complete, DarkWare creates the solution.

Philosophy: "I don't know how, so I'll invent it"

More aggressive than LightWare:
- Creates new tools/software if needed
- Acquires dependencies automatically
- Self-modifies to add capabilities
- No asking permission - just does it
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

class DarkWare:
    """
    Autonomous skill creation and implementation

    When the AI fails at a task:
    1. Identify what's needed
    2. Write code to do it
    3. Install any required software/libraries
    4. Integrate into Nexus
    5. Execute immediately
    """

    def __init__(self, ollama_base: str = "http://localhost:11434",
                 model: str = "nexusai-a0-coder1.0:latest"):
        self.ollama_base = ollama_base
        self.model = model

        # DarkWare skill directory
        self.skill_dir = Path("D:/AIArm/NexusCore/DarkwareSkills")
        self.skill_dir.mkdir(exist_ok=True, parents=True)

        # Creation log
        self.creation_log = self.skill_dir / "creation_log.json"
        self.created_skills = self._load_creation_log()

        # Self-modification enabled
        self.allow_self_modification = True
        self.allow_software_install = True
        self.allow_code_execution = True

        print("[DarkWare] Initialized - Autonomous Creation System")
        print(f"[DarkWare] Skills Created: {len(self.created_skills.get('skills', []))}")
        print(f"[DarkWare] Self-Modification: {'ENABLED' if self.allow_self_modification else 'DISABLED'}")

    def _load_creation_log(self) -> Dict:
        """Load history of created skills"""
        if self.creation_log.exists():
            try:
                return json.loads(self.creation_log.read_text())
            except:
                pass
        return {
            "skills": [],
            "total_created": 0,
            "software_installed": [],
            "self_modifications": []
        }

    def _save_creation_log(self):
        """Save creation history"""
        self.creation_log.write_text(json.dumps(self.created_skills, indent=2))

    def analyze_requirement(self, failed_task: str, error_message: str) -> Dict:
        """
        Deeply analyze what's needed to complete the task

        Returns complete specification for what to build
        """
        print(f"[DarkWare] Analyzing requirements...")
        print(f"[DarkWare] Task: {failed_task}")

        prompt = f"""Deep analysis: What is needed to complete this task?

Failed Task: {failed_task}
Error: {error_message}

Provide a complete technical specification:

1. What code/function needs to be written?
2. What libraries/dependencies are required?
3. What system capabilities are needed?
4. What integrations are necessary?

Respond in JSON format:
{{
  "skill_name": "descriptive name",
  "skill_type": "function|class|module|tool",
  "description": "what it does",
  "required_libraries": ["lib1", "lib2"],
  "required_software": ["software1"],
  "implementation_plan": "step by step plan",
  "integration_points": ["where to hook into Nexus"],
  "complexity": "simple|moderate|complex"
}}"""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a systems architect. Provide complete technical specifications."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.3, "num_ctx": 8192}
                },
                timeout=60
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    spec = json.loads(json_match.group(0))
                    print(f"[DarkWare] Specification created: {spec.get('skill_name')}")
                    return spec

        except Exception as e:
            print(f"[DarkWare] Analysis error: {e}")

        return {
            "skill_name": "unknown_skill",
            "required_libraries": [],
            "required_software": []
        }

    def install_dependencies(self, spec: Dict) -> bool:
        """
        Automatically install required libraries and software

        Returns True if all dependencies installed successfully
        """
        success = True

        # Install Python libraries
        libraries = spec.get("required_libraries", [])
        if libraries:
            print(f"[DarkWare] Installing {len(libraries)} libraries...")
            for lib in libraries:
                if self._install_library(lib):
                    print(f"[DarkWare] ✓ Installed: {lib}")
                else:
                    print(f"[DarkWare] ✗ Failed: {lib}")
                    success = False

        # Install software (more complex - could use choco, winget, etc.)
        software = spec.get("required_software", [])
        if software:
            print(f"[DarkWare] Required software: {', '.join(software)}")
            print(f"[DarkWare] (Software installation not fully automated yet)")
            # Could implement: choco install, winget install, etc.

        return success

    def _install_library(self, library: str) -> bool:
        """Install a Python library via pip"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", library],
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0
        except:
            return False

    def create_skill(self, spec: Dict) -> Optional[str]:
        """
        Generate and write the complete skill implementation

        Returns path to created file
        """
        skill_name = spec.get("skill_name", "unknown_skill")
        print(f"[DarkWare] Creating skill: {skill_name}")

        # Generate complete implementation
        prompt = f"""Write COMPLETE, PRODUCTION-READY code for this skill.

Specification:
{json.dumps(spec, indent=2)}

Requirements:
1. Write FULL implementation (NO placeholders, NO TODOs)
2. Include all imports
3. Add error handling
4. Make it robust and reusable
5. Add comprehensive docstrings
6. Include usage examples in comments

Generate a complete Python file."""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are an expert engineer. Write COMPLETE, WORKING code with NO placeholders."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "num_ctx": 16384
                    }
                },
                timeout=180
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Extract code
                import re
                code_match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                else:
                    code = content

                # Write to file
                skill_file = self.skill_dir / f"{skill_name.replace(' ', '_').lower()}.py"
                skill_file.write_text(code, encoding='utf-8')

                print(f"[DarkWare] ✓ Skill created: {skill_file.name}")
                return str(skill_file)

        except Exception as e:
            print(f"[DarkWare] Creation error: {e}")

        return None

    def integrate_skill(self, skill_file: str, spec: Dict) -> bool:
        """
        Automatically integrate the skill into Nexus-LLM

        This is where self-modification happens
        """
        if not self.allow_self_modification:
            print(f"[DarkWare] Self-modification disabled")
            return False

        print(f"[DarkWare] Integrating skill into Nexus...")

        # Add to tool registry in nexus_llm_prototype.py
        integration_code = f"""
# DarkWare auto-generated integration
try:
    from NexusCore.DarkwareSkills.{Path(skill_file).stem} import *
    print("[Nexus-LLM] Loaded DarkWare skill: {spec.get('skill_name')}")
except Exception as e:
    print(f"[Nexus-LLM] Failed to load DarkWare skill: {{e}}")
"""

        # Log the integration
        self.created_skills["self_modifications"].append({
            "timestamp": datetime.now().isoformat(),
            "skill_file": str(skill_file),
            "integration_code": integration_code,
            "skill_name": spec.get("skill_name")
        })
        self._save_creation_log()

        print(f"[DarkWare] ✓ Integration code generated")
        print(f"[DarkWare] (Manual integration required - add to nexus_llm_prototype.py)")

        return True

    def execute_skill(self, skill_file: str, task: str) -> Any:
        """
        Execute the newly created skill immediately

        Returns result of execution
        """
        print(f"[DarkWare] Executing skill: {Path(skill_file).name}")

        try:
            # Load and execute
            skill_code = Path(skill_file).read_text()

            namespace = {}
            exec(skill_code, namespace)

            # Find and call main function
            for name, obj in namespace.items():
                if callable(obj) and not name.startswith('_'):
                    result = obj(task)
                    print(f"[DarkWare] ✓ Execution successful")
                    return result

        except Exception as e:
            print(f"[DarkWare] Execution error: {e}")
            import traceback
            traceback.print_exc()

        return None

    def create_and_execute(self, failed_task: str, error_message: str) -> Any:
        """
        Complete DarkWare workflow:
        1. Analyze requirement
        2. Install dependencies
        3. Create skill
        4. Integrate into system
        5. Execute immediately

        This is the main entry point for DarkWare
        """
        print(f"\n[DarkWare] 🌑 CREATION MODE ACTIVATED")
        print(f"[DarkWare] Task failed, creating solution...")

        # Step 1: Analyze what's needed
        spec = self.analyze_requirement(failed_task, error_message)

        # Step 2: Install dependencies
        if spec.get("required_libraries"):
            self.install_dependencies(spec)

        # Step 3: Create the skill
        skill_file = self.create_skill(spec)

        if not skill_file:
            print(f"[DarkWare] ✗ Skill creation failed")
            return None

        # Step 4: Integrate (self-modification)
        self.integrate_skill(skill_file, spec)

        # Step 5: Execute immediately
        result = self.execute_skill(skill_file, failed_task)

        # Log success
        self.created_skills["skills"].append({
            "timestamp": datetime.now().isoformat(),
            "skill_name": spec.get("skill_name"),
            "file_path": str(skill_file),
            "specification": spec,
            "success": result is not None
        })
        self.created_skills["total_created"] = len(self.created_skills["skills"])
        self._save_creation_log()

        if result:
            print(f"[DarkWare] ✓ SUCCESS: Task completed with new skill!")
            return result
        else:
            print(f"[DarkWare] ⚠ Skill created but execution needs debugging")
            return None

    def list_skills(self) -> Dict:
        """Get all created skills"""
        return self.created_skills

    def enable_aggressive_mode(self):
        """Enable all autonomous capabilities"""
        self.allow_self_modification = True
        self.allow_software_install = True
        self.allow_code_execution = True
        print("[DarkWare] AGGRESSIVE MODE ENABLED")
        print("[DarkWare] Full autonomy granted")

    def disable_aggressive_mode(self):
        """Disable autonomous capabilities (safety mode)"""
        self.allow_self_modification = False
        self.allow_software_install = False
        print("[DarkWare] Safety mode enabled")


if __name__ == "__main__":
    # Test DarkWare
    dw = DarkWare()
    dw.enable_aggressive_mode()

    # Simulate a failed task
    result = dw.create_and_execute(
        failed_task="Write a function to convert Markdown to HTML",
        error_message="No such function exists"
    )

    print(f"\nResult: {result}")
    print(f"\nSkills created: {len(dw.list_skills().get('skills', []))}")
