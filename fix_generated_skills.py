#!/usr/bin/env python
"""
Quick fix: Clean markdown from generated skill files
"""
import re
from pathlib import Path

def clean_skill_file(filepath):
    """Remove markdown blocks and explanatory text from skill files"""
    content = filepath.read_text(encoding='utf-8')

    # Extract code from markdown
    code_match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
    if code_match:
        clean_code = code_match.group(1)
        filepath.write_text(clean_code, encoding='utf-8')
        print(f"✓ Fixed: {filepath.name}")
        return True
    else:
        print(f"⚠ No markdown found in: {filepath.name}")
        return False

# Fix LightWare skills
lightware_dir = Path("D:/AIArm/NexusCore/SkillLibrary")
if lightware_dir.exists():
    print("[LightWare Skills]")
    for skill_file in lightware_dir.glob("*.py"):
        clean_skill_file(skill_file)

# Fix DarkWare skills
darkware_dir = Path("D:/AIArm/NexusCore/DarkwareSkills")
if darkware_dir.exists():
    print("\n[DarkWare Skills]")
    for skill_file in darkware_dir.glob("*.py"):
        clean_skill_file(skill_file)

print("\n✓ Skill files cleaned!")
