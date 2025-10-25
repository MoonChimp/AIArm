#!/usr/bin/env python3
"""
Web Interface Bridge for AlfaZer0
Extremely simplified version for direct web interface integration
"""

import sys
import json
import os
import traceback
from pathlib import Path
from datetime import datetime

# Make sure we can write logs
LOG_FILE = "D:/AIArm/Logs/web_bridge.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Log function
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# Just write a test file directly - simplest possible operation
def create_test_file():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"D:/AIArm/Test/web_test_{timestamp}.txt"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"This is a test file created through the web interface at {datetime.now()}.\n")
            f.write("If you can read this, the integration is working correctly.\n")
        
        log(f"Successfully created test file: {file_path}")
        return {
            "success": True,
            "message": f"Test file created at {file_path}",
            "path": file_path
        }
    except Exception as e:
        error_msg = f"Error creating test file: {str(e)}"
        log(f"ERROR: {error_msg}\n{traceback.format_exc()}")
        return {
            "success": False,
            "error": error_msg
        }

# Main function - extremely simplified
def main():
    try:
        # Read any input but ignore it
        input_data = sys.stdin.read()
        log(f"Received input: {input_data[:100]}...")
        
        # Always just create a test file
        result = create_test_file()
        
        # Format response for the web interface
        response = {
            "success": True,
            "response": f"I created a test file for you at {result['path']}. This demonstrates my filesystem capabilities working through the web interface."
        }
        
        # Return the result
        print(json.dumps(response))
    except Exception as e:
        error_msg = f"Error in web_bridge.py: {str(e)}"
        log(f"ERROR: {error_msg}\n{traceback.format_exc()}")
        print(json.dumps({
            "success": False,
            "response": f"I encountered an error: {str(e)}. Please check the logs."
        }))

if __name__ == "__main__":
    main()
