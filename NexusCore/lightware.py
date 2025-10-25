#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LightWare: Skill Acquisition System
When Nexus encounters a task it cannot complete, LightWare helps it learn.

Philosophy: "I don't know how, so I'll learn"
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class LightWare:
    """
    Recognizes capability gaps and acquires skills to fill them

    When the AI fails at a task:
    1. Identify what skill is missing
    2. Search for examples/documentation
    3. Learn the skill
    4. Store in skill library
    5. Retry the task with new knowledge
    """

    def __init__(self, ollama_base: str = "http://localhost:11434",
                 model: str = "nexusai-a0-coder1.0:latest"):
        self.ollama_base = ollama_base
        self.model = model

        # Skill library location
        self.skill_dir = Path("D:/AIArm/NexusCore/SkillLibrary")
        self.skill_dir.mkdir(exist_ok=True, parents=True)

        # Learning log
        self.learning_log = self.skill_dir / "learning_log.json"
        self.learned_skills = self._load_learning_log()

        print("[LightWare] Initialized - Skill Acquisition System")
        print(f"[LightWare] Skills Learned: {len(self.learned_skills)}")

    def _load_learning_log(self) -> Dict:
        """Load history of learned skills"""
        if self.learning_log.exists():
            try:
                return json.loads(self.learning_log.read_text())
            except:
                pass
        return {"skills": [], "total_learned": 0}

    def _save_learning_log(self):
        """Save learning history"""
        self.learning_log.write_text(json.dumps(self.learned_skills, indent=2))

    def recognize_gap(self, failed_task: str, error_message: str) -> Dict:
        """
        Analyze a failed task to identify what skill is missing

        Args:
            failed_task: What the AI was trying to do
            error_message: Why it failed

        Returns:
            Analysis of the skill gap
        """
        print(f"[LightWare] Analyzing failure...")
        print(f"[LightWare] Task: {failed_task}")
        print(f"[LightWare] Error: {error_message[:100]}")

        # Ask AI to analyze the gap
        prompt = f"""Analyze this failed task and identify the missing skill.

Failed Task: {failed_task}
Error: {error_message}

What skill or knowledge is needed to complete this task?
What specific capability is missing?

Respond in JSON format:
{{
  "missing_skill": "name of the skill",
  "skill_type": "programming|knowledge|tool|library",
  "description": "what this skill does",
  "search_query": "query to find information about this skill"
}}"""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a skill gap analyst. Identify missing capabilities."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.3}
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Extract JSON
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group(0))
                    print(f"[LightWare] Missing Skill: {analysis.get('missing_skill')}")
                    return analysis

        except Exception as e:
            print(f"[LightWare] Analysis error: {e}")

        return {
            "missing_skill": "unknown",
            "skill_type": "unknown",
            "description": "Could not determine missing skill",
            "search_query": failed_task
        }

    def acquire_skill(self, skill_analysis: Dict) -> Optional[str]:
        """
        Acquire the missing skill through learning

        Steps:
        1. Search for information about the skill
        2. Generate code/knowledge to implement it
        3. Test the implementation
        4. Store in skill library

        Returns:
            Path to the new skill file, or None if failed
        """
        skill_name = skill_analysis.get("missing_skill", "unknown_skill")
        skill_type = skill_analysis.get("skill_type", "unknown")

        print(f"[LightWare] Acquiring skill: {skill_name}")

        # Generate implementation
        prompt = f"""Create a complete implementation for this skill.

Skill: {skill_name}
Type: {skill_type}
Description: {skill_analysis.get('description')}

Requirements:
1. Write complete, working code (no placeholders)
2. Include error handling
3. Add docstrings explaining usage
4. Make it reusable

Generate a Python function or class that implements this skill."""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are an expert programmer. Write complete, working code."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.5,
                        "num_ctx": 8192
                    }
                },
                timeout=120
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Extract code
                import re
                code_match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                else:
                    # No markdown, use whole response
                    code = content

                # Save to skill library
                skill_file = self.skill_dir / f"{skill_name.replace(' ', '_')}.py"
                skill_file.write_text(code, encoding='utf-8')

                # Log the learning
                self.learned_skills["skills"].append({
                    "timestamp": datetime.now().isoformat(),
                    "skill_name": skill_name,
                    "skill_type": skill_type,
                    "file_path": str(skill_file),
                    "description": skill_analysis.get('description')
                })
                self.learned_skills["total_learned"] = len(self.learned_skills["skills"])
                self._save_learning_log()

                print(f"[LightWare] ✓ Skill acquired: {skill_file.name}")
                return str(skill_file)

        except Exception as e:
            print(f"[LightWare] Acquisition error: {e}")

        return None

    def apply_skill(self, skill_file: str, task: str) -> Any:
        """
        Apply a learned skill to complete a task

        Args:
            skill_file: Path to the skill implementation
            task: The task to complete using this skill

        Returns:
            Result of applying the skill
        """
        print(f"[LightWare] Applying skill: {Path(skill_file).name}")

        try:
            # Load the skill
            skill_code = Path(skill_file).read_text()

            # Execute in a namespace
            namespace = {}
            exec(skill_code, namespace)

            # Try to find and call the main function
            # (This is simplified - could be smarter)
            for name, obj in namespace.items():
                if callable(obj) and not name.startswith('_'):
                    result = obj(task)
                    print(f"[LightWare] ✓ Skill applied successfully")
                    return result

        except Exception as e:
            print(f"[LightWare] Application error: {e}")
            return None

    def learn_and_retry(self, failed_task: str, error_message: str) -> Any:
        """
        Complete workflow: Recognize gap → Acquire skill → Retry task

        This is the main entry point for LightWare
        """
        print(f"\n[LightWare] ⚡ LEARNING MODE ACTIVATED")
        print(f"[LightWare] Task failed, attempting to learn...")

        # Step 1: Recognize what's missing
        skill_analysis = self.recognize_gap(failed_task, error_message)

        # Step 2: Acquire the skill
        skill_file = self.acquire_skill(skill_analysis)

        if not skill_file:
            print(f"[LightWare] ✗ Failed to acquire skill")
            return None

        # Step 3: Apply the new skill
        result = self.apply_skill(skill_file, failed_task)

        if result:
            print(f"[LightWare] ✓ SUCCESS: Task completed with new skill!")
            return result
        else:
            print(f"[LightWare] ✗ Skill acquired but task still failed")
            return None

    def list_skills(self) -> Dict:
        """Get list of all learned skills"""
        return self.learned_skills

    def get_skill(self, skill_name: str) -> Optional[str]:
        """Retrieve a specific skill by name"""
        for skill in self.learned_skills.get("skills", []):
            if skill["skill_name"] == skill_name:
                return skill.get("file_path")
        return None


if __name__ == "__main__":
    # Test LightWare
    lw = LightWare()

    # Simulate a failed task
    result = lw.learn_and_retry(
        failed_task="Parse JSON from a string",
        error_message="JSONDecodeError: Expecting value"
    )

    print(f"\nResult: {result}")
    print(f"\nSkills learned: {lw.list_skills()}")
