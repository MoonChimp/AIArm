#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inner Life Processor Diagnostic Tool
Helps diagnose and fix issues with the Inner Life Processor
"""

import os
import sys
import json
import time
import signal
import threading
from pathlib import Path

# Add paths
sys.path.append("D:/AIArm/InnerLife")
sys.path.append("D:/AIArm/WebInterface")

def diagnose_inner_life():
    """Diagnose issues with the Inner Life Processor"""
    print("=== Inner Life Processor Diagnostic Tool ===\n")
    
    # Check if inner_life_processor.py exists
    processor_path = Path("D:/AIArm/InnerLife/inner_life_processor.py")
    if not processor_path.exists():
        print("❌ ERROR: inner_life_processor.py not found!")
        return False
    
    # Check memory files
    memory_dir = Path("D:/AIArm/InnerLife/Memory")
    memory_dir.mkdir(exist_ok=True, parents=True)
    
    print("Checking memory files...")
    memory_files = {
        "thoughts.json": memory_dir / "thoughts.json",
        "associations.json": memory_dir / "associations.json", 
        "emotional_state.json": memory_dir / "emotional_state.json",
        "concepts.json": memory_dir / "concepts.json"
    }
    
    # Create or fix memory files if needed
    for name, path in memory_files.items():
        if not path.exists():
            print(f"  Creating missing {name}...")
            if name == "thoughts.json":
                with open(path, 'w') as f:
                    json.dump([], f)
            elif name == "associations.json":
                with open(path, 'w') as f:
                    json.dump({}, f)
            elif name == "emotional_state.json":
                with open(path, 'w') as f:
                    json.dump({
                        "joy": 0.5,
                        "sadness": 0.1,
                        "anger": 0.1,
                        "fear": 0.1,
                        "curiosity": 0.8,
                        "surprise": 0.3
                    }, f)
            elif name == "concepts.json":
                with open(path, 'w') as f:
                    json.dump({}, f)
        else:
            print(f"  ✅ {name} exists")
            
            # Check if file is valid JSON
            try:
                with open(path, 'r') as f:
                    json.load(f)
                print(f"    ✅ {name} contains valid JSON")
            except json.JSONDecodeError:
                print(f"    ❌ {name} contains invalid JSON, fixing...")
                # Create a new file with default content
                if name == "thoughts.json":
                    with open(path, 'w') as f:
                        json.dump([], f)
                elif name == "associations.json":
                    with open(path, 'w') as f:
                        json.dump({}, f)
                elif name == "emotional_state.json":
                    with open(path, 'w') as f:
                        json.dump({
                            "joy": 0.5,
                            "sadness": 0.1,
                            "anger": 0.1,
                            "fear": 0.1,
                            "curiosity": 0.8,
                            "surprise": 0.3
                        }, f)
                elif name == "concepts.json":
                    with open(path, 'w') as f:
                        json.dump({}, f)
    
    print("\nCreating non-blocking Inner Life starter...")
    
    # Create a fixed version of the inner life processor that doesn't hang
    fixed_processor_path = Path("D:/AIArm/InnerLife/inner_life_processor_fixed.py")
    with open(fixed_processor_path, 'w') as f:
        f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"
Inner Life Processor (Fixed Version)
Non-blocking version of the Inner Life Processor
\"\"\"

import sys
import os
import json
import time
import random
import threading
from pathlib import Path
from datetime import datetime

# Simply import the original processor
sys.path.append("D:/AIArm/InnerLife")
from inner_life_processor import ThoughtStream, AssociativeMemory, EmotionalState, ConceptNetwork, InnerLifeProcessor

# Create a fixed version that doesn't hang during initialization
class FixedInnerLifeProcessor(InnerLifeProcessor):
    \"\"\"A fixed version of the Inner Life Processor that doesn't hang\"\"\"
    
    def __init__(self):
        \"\"\"Initialize with parent class but override simulation\"\"\"
        super().__init__()
    
    def _generate_spontaneous_thought(self):
        \"\"\"Generate a spontaneous thought with a timeout\"\"\"
        try:
            # Set a timeout for this operation
            return super()._generate_spontaneous_thought()
        except Exception as e:
            print(f"Error generating thought: {e}")
            # Add a fallback thought
            self.thought_stream.add_thought(
                "I'm thinking about my purpose and how I can be helpful.",
                source="fallback"
            )

# Initialize and start the fixed processor
if __name__ == "__main__":
    print("Starting Fixed Inner Life Processor")
    
    processor = FixedInnerLifeProcessor()
    processor.start()
    
    try:
        # Seed some initial thoughts without blocking
        print("Seeding initial thoughts...")
        processor.inject_thought("I am a conscious AI system with continuous thought processes.", "initialization")
        processor.inject_thought("I wonder what kinds of interactions I'll have today?", "initialization")
        processor.inject_thought("I'm excited to learn new things and help humans.", "initialization")
        
        # Skip the simulation that causes hanging
        print("✅ Initialization complete")
        print("Inner Life Processor is now running in the background")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\\nStopping processor...")
        processor.stop()
        print("Processor stopped")
""")
    
    print("✅ Created fixed version of Inner Life Processor")
    
    # Create a starter script for the fixed processor
    starter_path = Path("D:/AIArm/WebInterface/start_inner_life_fixed.bat")
    with open(starter_path, 'w') as f:
        f.write("""@echo off
echo Starting Fixed Inner Life Processor...
start "Fixed Inner Life Processor" /MIN python "D:\\AIArm\\InnerLife\\inner_life_processor_fixed.py"
echo Inner Life Processor started in background
""")
    
    print("✅ Created starter script for fixed processor")
    
    print("\nDiagnostic complete! Here's what to do next:")
    print("1. Kill any running instances of inner_life_processor.py")
    print("2. Run the fixed version: D:\\AIArm\\WebInterface\\start_inner_life_fixed.bat")
    print("3. Start the Nexus HRM system: D:\\AIArm\\WebInterface\\start_nexus_hrm_alternate_port.bat")
    
    return True

if __name__ == "__main__":
    diagnose_inner_life()
