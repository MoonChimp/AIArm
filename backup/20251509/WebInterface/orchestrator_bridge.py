import os
import sys
import json
import argparse

# Add the MultiAgent directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
multiagent_dir = os.path.join(parent_dir, 'MultiAgent')
sys.path.append(multiagent_dir)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='AIArm Interface Bridge')
parser.add_argument('--input', type=str, help='User input to process')
parser.add_argument('--agent', type=str, default='orchestrator', help='Agent to use')
parser.add_argument('--list-methods', action='store_true', help='List available methods')
args = parser.parse_args()

# Import the orchestrator
try:
    import enhanced_orchestrator
    
    # Create an instance of the orchestrator
    orchestrator = enhanced_orchestrator.EnhancedAIArmOrchestrator()
    
    # List all methods if requested
    if args.list_methods:
        methods = [method for method in dir(orchestrator) if not method.startswith('_')]
        print(json.dumps({
            "success": True, 
            "methods": methods
        }))
        sys.exit(0)
    
    # Check for input
    if args.input:
        # Use the process_request method we discovered
        try:
            result = orchestrator.process_request(args.input, args.agent)
            print(json.dumps({"success": True, "response": result}))
        except Exception as e:
            print(json.dumps({
                "success": False,
                "error": f"Error calling process_request: {str(e)}"
            }))
    else:
        # Just return status if no input
        agents = []
        if hasattr(orchestrator, 'agent_manager') and hasattr(orchestrator.agent_manager, 'list_agents'):
            agents = orchestrator.agent_manager.list_agents()
        
        print(json.dumps({
            "success": True, 
            "status": "Orchestrator loaded successfully",
            "agents": agents
        }))
        
except Exception as e:
    print(json.dumps({
        "success": False,
        "error": str(e)
    }))
