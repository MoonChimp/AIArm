#!/usr/bin/env python3
"""
Standalone Bridge for AlfaZer0 - works without Ollama

This script provides AI-like responses with administrative filesystem capabilities
without requiring Ollama to be installed or running.
"""

import sys
import json
import subprocess
import os
import traceback
from pathlib import Path
from datetime import datetime

# Constants
LOGS_DIR = Path("D:/AIArm/Logs")
LOGS_DIR.mkdir(exist_ok=True, parents=True)

LOG_FILE = LOGS_DIR / "standalone_bridge.log"

# Log function
def log_message(message):
    """Write a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    
    # Print to console
    print(log_line, file=sys.stderr)
    
    # Write to log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

# Ensure alfazer0_bridge.py exists
def ensure_bridge():
    bridge_path = Path(os.path.dirname(os.path.abspath(__file__))) / "alfazer0_bridge.py"
    
    if not bridge_path.exists():
        log_message(f"Error: {bridge_path} not found!")
        return False
    
    return str(bridge_path)

# Execute a filesystem operation using the bridge
def execute_operation(operation, params=None):
    """Execute an operation using the alfazer0_bridge.py script"""
    bridge_path = ensure_bridge()
    if not bridge_path:
        return {"success": False, "error": "Bridge script not found"}
    
    if params is None:
        params = {}
    
    request_data = json.dumps({
        "operation": operation,
        **params
    })
    
    try:
        # Run the bridge
        process = subprocess.Popen(
            [sys.executable, bridge_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=request_data)
        
        if process.returncode == 0:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                return {"success": False, "error": "Failed to parse bridge output", "output": stdout}
        else:
            return {"success": False, "error": f"Bridge process failed with code {process.returncode}", "stderr": stderr}
    except Exception as e:
        log_message(f"Error executing operation: {str(e)}\n{traceback.format_exc()}")
        return {"success": False, "error": str(e)}

# Create a test file
def create_test_file():
    """Create a test file to demonstrate filesystem capabilities"""
    return execute_operation(
        "write_file",
        {
            "path": f"D:/AIArm/Test/standalone_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "content": f"This is a test file created by NexusAI:AlfaZer0 on {datetime.now()}.\n\nThis file demonstrates that I have full administrative filesystem capabilities.\n\nIf you can read this file, the test was successful!"
        }
    )

# Generate a response based on user input
def generate_response(user_input):
    """Generate a response based on user input"""
    input_lower = user_input.lower()
    
    # Special case for test file creation
    if "test file" in input_lower or ("create" in input_lower and "file" in input_lower):
        result = create_test_file()
        if result.get("success"):
            return f"I've successfully created a test file at {result['path']}. This confirms that I have full administrative filesystem capabilities. You can open and read this file to verify."
        else:
            return f"I tried to create a test file, but encountered an error: {result.get('error', 'Unknown error')}."
    
    # Handle different types of requests
    if "hello" in input_lower or "hi" in input_lower or len(user_input) < 20:
        return "Hello! I am NexusAI:AlfaZer0, an advanced AI assistant with administrative filesystem capabilities. I can help you with various tasks, including file operations with full system access. How can I assist you today?"
    
    # Check if this looks like a filesystem operation
    filesystem_terms = [
        'file', 'directory', 'folder', 'create', 'write', 'read', 'list',
        'show me', 'display', 'delete', 'remove', 'copy', 'move', 'rename',
        'command', 'execute', 'run', 'script', 'system', 'admin', 'task'
    ]
    
    is_filesystem_request = any(term in input_lower for term in filesystem_terms)
    
    if is_filesystem_request:
        # Try to determine what operation is being requested
        if "list" in input_lower or "show" in input_lower or "what's in" in input_lower:
            # This is a directory listing request
            dir_path = "D:/"
            # Try to extract a path
            if ":" in user_input:
                for word in user_input.split():
                    if ":" in word:
                        possible_path = word.strip(",.?!")
                        if os.path.exists(possible_path):
                            dir_path = possible_path
                            break
            
            result = execute_operation("list_directory", {"path": dir_path})
            if result.get("success") and "items" in result:
                response = f"Here's what I found in {dir_path}:\n\n"
                for item in result["items"]:
                    if isinstance(item, dict) and "name" in item and "type" in item:
                        response += f"[{item['type'].upper()}] {item['name']}\n"
                return response
        
        # Handle write requests
        if "write" in input_lower or "create file" in input_lower:
            return "I can create or write to files with my administrative privileges. Please provide the path and content you'd like to write."
        
        # Handle read requests
        if "read" in input_lower:
            return "I can read files with my administrative privileges. Please specify which file you'd like me to read."
        
        # Generic filesystem response
        return "I have administrative filesystem capabilities that allow me to perform this operation. I can read, write, list, and execute files across your system. Would you like me to proceed?"
    
    # Default response for other types of queries
    return "I'm NexusAI:AlfaZer0, an advanced AI assistant with administrative capabilities. I can help you with file operations, run commands with administrative privileges, and adapt to your needs. What would you like me to do for you today?"

# Main function
def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        
        log_message(f"Received input: {input_data[:100]}...")
        
        # Generate a response
        response = generate_response(input_data)
        
        # Return the response in the expected JSON format
        result = {
            "success": True,
            "response": response
        }
        
        print(json.dumps(result))
    except Exception as e:
        log_message(f"Error in standalone_bridge.py: {str(e)}\n{traceback.format_exc()}")
        error_result = {
            "success": False,
            "error": str(e),
            "response": "I encountered an error in my processing. Please check the logs for details."
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
