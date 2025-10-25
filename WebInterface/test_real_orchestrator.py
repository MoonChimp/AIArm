import sys
import os
import json
import importlib.util

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
multiagent_dir = os.path.join(parent_dir, 'MultiAgent')

# Add the MultiAgent directory to the path
sys.path.append(multiagent_dir)

# Try to import the enhanced_orchestrator module
try:
    import enhanced_orchestrator
    print("Successfully imported enhanced_orchestrator")
    print("Available attributes:", dir(enhanced_orchestrator))
    
    # Check for the orchestrator class
    if hasattr(enhanced_orchestrator, 'EnhancedAIArmOrchestrator'):
        print("Found class: EnhancedAIArmOrchestrator")
        
        # Try to create an instance
        try:
            orchestrator = enhanced_orchestrator.EnhancedAIArmOrchestrator()
            print("Successfully created orchestrator instance")
            
            # Try a simple request
            result = orchestrator.process_input("test message", "orchestrator")
            print("Test result:", result)
            
        except Exception as e:
            print(f"Error creating orchestrator instance: {str(e)}")
    else:
        print("Class EnhancedAIArmOrchestrator not found")
        print("Available classes:", [attr for attr in dir(enhanced_orchestrator) if not attr.startswith('_')])
except Exception as e:
    print(f"Error importing enhanced_orchestrator: {str(e)}")

# If the module couldn't be imported, try to load it directly
if 'enhanced_orchestrator' not in sys.modules:
    print("Trying to load module directly...")
    orchestrator_path = os.path.join(multiagent_dir, 'enhanced_orchestrator.py')
    
    if os.path.exists(orchestrator_path):
        print(f"Found orchestrator at: {orchestrator_path}")
        
        # Load the module from file
        spec = importlib.util.spec_from_file_location("enhanced_orchestrator", orchestrator_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print("Successfully loaded module directly")
        print("Available attributes:", dir(module))
        
        # Look for the orchestrator class
        potential_classes = [attr for attr in dir(module) if 'orchestrator' in attr.lower() or 'agent' in attr.lower()]
        print("Potential orchestrator classes:", potential_classes)
    else:
        print(f"Orchestrator file not found at: {orchestrator_path}")
