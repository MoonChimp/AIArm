#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct File Operations for Nexus AI
Provides a simple interface for file operations
"""

import os
import sys
import json
import argparse
import traceback
from datetime import datetime
from pathlib import Path

# Configuration
LOGS_DIR = Path("D:/AIArm/Logs")
LOGS_DIR.mkdir(exist_ok=True, parents=True)

def log_message(message):
    """Log a message to the console and a file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    
    print(log_line)
    
    log_file = LOGS_DIR / "nexus_direct_fs.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

def write_file(path, content):
    """Write content to a file"""
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the content to the file
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return {
            "success": True,
            "message": f"Successfully wrote to file: {path}",
            "path": path
        }
    except Exception as e:
        log_message(f"Error writing file: {e}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "path": path
        }

def read_file(path):
    """Read content from a file"""
    try:
        # Check if file exists
        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"File does not exist: {path}",
                "path": path
            }
        
        # Read the content from the file
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return {
            "success": True,
            "content": content,
            "path": path
        }
    except Exception as e:
        log_message(f"Error reading file: {e}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "path": path
        }

def list_directory(path):
    """List contents of a directory"""
    try:
        # Check if directory exists
        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"Directory does not exist: {path}",
                "path": path
            }
        
        if not os.path.isdir(path):
            return {
                "success": False,
                "error": f"Path is not a directory: {path}",
                "path": path
            }
        
        # List directory contents
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            item_type = "directory" if os.path.isdir(item_path) else "file"
            items.append({
                "name": item,
                "type": item_type,
                "path": item_path
            })
        
        return {
            "success": True,
            "items": items,
            "path": path
        }
    except Exception as e:
        log_message(f"Error listing directory: {e}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "path": path
        }

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="Nexus Direct File Operations")
    parser.add_argument("--operation", type=str, required=True, 
                        choices=["write", "read", "list"],
                        help="Operation to perform")
    parser.add_argument("--path", type=str, required=True, 
                        help="Path to the file or directory")
    parser.add_argument("--content", type=str, 
                        help="Content to write to the file")
    
    args = parser.parse_args()
    
    try:
        if args.operation == "write":
            if not args.content:
                print(json.dumps({
                    "success": False,
                    "error": "Content is required for write operation"
                }))
                return
            
            result = write_file(args.path, args.content)
        elif args.operation == "read":
            result = read_file(args.path)
        elif args.operation == "list":
            result = list_directory(args.path)
        else:
            result = {
                "success": False,
                "error": f"Unknown operation: {args.operation}"
            }
        
        print(json.dumps(result, indent=2))
    except Exception as e:
        log_message(f"Error in main: {e}")
        traceback.print_exc()
        
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))

if __name__ == "__main__":
    main()