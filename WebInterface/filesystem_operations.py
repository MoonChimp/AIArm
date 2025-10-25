#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIArm FileSystem Operations Module
Provides file system capabilities to NexusAI
"""

import os
import sys
import json
import shutil
import traceback
import argparse
import io
import time
import random
import uuid
import base64
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
LOGS_DIR = Path("D:/AIArm/Logs")
LOGS_DIR.mkdir(exist_ok=True, parents=True)

# Create a log file for this session
LOG_FILE = LOGS_DIR / f"filesystem_operations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log_message(message, level="INFO"):
    """Log a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    # Print to console
    print(log_entry.strip())
    
    # Write to log file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

class FileSystemOperations:
    """Provides file system operations for NexusAI"""
    
    @staticmethod
    def read_file(path):
        """Read the contents of a file"""
        try:
            log_message(f"Reading file: {path}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return {
                "success": True,
                "content": content,
                "path": path
            }
        except UnicodeDecodeError:
            # Try reading as binary
            try:
                with open(path, "rb") as f:
                    content = base64.b64encode(f.read()).decode("utf-8")
                return {
                    "success": True,
                    "content": content,
                    "path": path,
                    "encoding": "base64"
                }
            except Exception as e:
                log_message(f"Error reading file as binary: {e}", "ERROR")
                return {
                    "success": False,
                    "error": str(e),
                    "path": path
                }
        except Exception as e:
            log_message(f"Error reading file: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def write_file(path, content, encoding="utf-8"):
        """Write content to a file"""
        try:
            log_message(f"Writing file: {path}")
            
            # Create directory if it doesn't exist
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Write the content
            if encoding == "base64":
                with open(path, "wb") as f:
                    f.write(base64.b64decode(content))
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
            
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            log_message(f"Error writing file: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def append_file(path, content):
        """Append content to a file"""
        try:
            log_message(f"Appending to file: {path}")
            
            # Create directory if it doesn't exist
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Append the content
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
            
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            log_message(f"Error appending to file: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def list_directory(path):
        """List the contents of a directory"""
        try:
            log_message(f"Listing directory: {path}")
            
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
            
            # Get the directory contents
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
            log_message(f"Error listing directory: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def create_directory(path):
        """Create a directory"""
        try:
            log_message(f"Creating directory: {path}")
            
            if os.path.exists(path):
                if os.path.isdir(path):
                    return {
                        "success": True,
                        "path": path,
                        "message": "Directory already exists"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Path exists but is not a directory: {path}",
                        "path": path
                    }
            
            # Create the directory
            os.makedirs(path)
            
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            log_message(f"Error creating directory: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def delete_file(path):
        """Delete a file"""
        try:
            log_message(f"Deleting file: {path}")
            
            if not os.path.exists(path):
                return {
                    "success": False,
                    "error": f"File does not exist: {path}",
                    "path": path
                }
            
            if os.path.isdir(path):
                return {
                    "success": False,
                    "error": f"Path is a directory, not a file: {path}",
                    "path": path
                }
            
            # Delete the file
            os.remove(path)
            
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            log_message(f"Error deleting file: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def delete_directory(path, recursive=False):
        """Delete a directory"""
        try:
            log_message(f"Deleting directory: {path} (recursive={recursive})")
            
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
            
            # Delete the directory
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
            
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            log_message(f"Error deleting directory: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def move_file(source, destination):
        """Move a file from source to destination"""
        try:
            log_message(f"Moving file: {source} to {destination}")
            
            if not os.path.exists(source):
                return {
                    "success": False,
                    "error": f"Source file does not exist: {source}",
                    "source": source,
                    "destination": destination
                }
            
            # Create destination directory if it doesn't exist
            dest_dir = os.path.dirname(destination)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            # Move the file
            shutil.move(source, destination)
            
            return {
                "success": True,
                "source": source,
                "destination": destination
            }
        except Exception as e:
            log_message(f"Error moving file: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "source": source,
                "destination": destination
            }
    
    @staticmethod
    def copy_file(source, destination):
        """Copy a file from source to destination"""
        try:
            log_message(f"Copying file: {source} to {destination}")
            
            if not os.path.exists(source):
                return {
                    "success": False,
                    "error": f"Source file does not exist: {source}",
                    "source": source,
                    "destination": destination
                }
            
            # Create destination directory if it doesn't exist
            dest_dir = os.path.dirname(destination)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            # Copy the file
            shutil.copy2(source, destination)
            
            return {
                "success": True,
                "source": source,
                "destination": destination
            }
        except Exception as e:
            log_message(f"Error copying file: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "source": source,
                "destination": destination
            }
    
    @staticmethod
    def get_file_info(path):
        """Get information about a file"""
        try:
            log_message(f"Getting file info: {path}")
            
            if not os.path.exists(path):
                return {
                    "success": False,
                    "error": f"File does not exist: {path}",
                    "path": path
                }
            
            # Get file information
            stat_info = os.stat(path)
            info = {
                "size": stat_info.st_size,
                "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                "is_directory": os.path.isdir(path),
                "is_file": os.path.isfile(path),
                "path": path,
                "name": os.path.basename(path),
                "directory": os.path.dirname(path),
                "extension": os.path.splitext(path)[1] if os.path.isfile(path) else ""
            }
            
            return {
                "success": True,
                "info": info,
                "path": path
            }
        except Exception as e:
            log_message(f"Error getting file info: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    @staticmethod
    def search_files(directory, pattern, recursive=True):
        """Search for files matching a pattern"""
        try:
            log_message(f"Searching for files: {pattern} in {directory} (recursive={recursive})")
            
            if not os.path.exists(directory):
                return {
                    "success": False,
                    "error": f"Directory does not exist: {directory}",
                    "directory": directory,
                    "pattern": pattern
                }
            
            if not os.path.isdir(directory):
                return {
                    "success": False,
                    "error": f"Path is not a directory: {directory}",
                    "directory": directory,
                    "pattern": pattern
                }
            
            # Search for files
            matches = []
            
            if recursive:
                for root, dirs, files in os.walk(directory):
                    for item in files + dirs:
                        if pattern.lower() in item.lower():
                            item_path = os.path.join(root, item)
                            item_type = "directory" if os.path.isdir(item_path) else "file"
                            matches.append({
                                "name": item,
                                "type": item_type,
                                "path": item_path
                            })
            else:
                for item in os.listdir(directory):
                    if pattern.lower() in item.lower():
                        item_path = os.path.join(directory, item)
                        item_type = "directory" if os.path.isdir(item_path) else "file"
                        matches.append({
                            "name": item,
                            "type": item_type,
                            "path": item_path
                        })
            
            return {
                "success": True,
                "matches": matches,
                "directory": directory,
                "pattern": pattern
            }
        except Exception as e:
            log_message(f"Error searching files: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e),
                "directory": directory,
                "pattern": pattern
            }

def process_filesystem_request(request_data):
    """Process a file system operation request"""
    try:
        # Extract request data
        if isinstance(request_data, str):
            try:
                # Try to parse as JSON
                data = json.loads(request_data)
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Invalid JSON request",
                    "request": request_data
                }
        else:
            data = request_data
        
        # Extract operation and parameters
        operation = data.get("operation")
        if not operation:
            return {
                "success": False,
                "error": "No operation specified",
                "request": data
            }
        
        # Process the operation
        fs = FileSystemOperations()
        
        if operation == "read_file":
            return fs.read_file(data.get("path", ""))
        
        elif operation == "write_file":
            return fs.write_file(
                data.get("path", ""),
                data.get("content", ""),
                data.get("encoding", "utf-8")
            )
        
        elif operation == "append_file":
            return fs.append_file(
                data.get("path", ""),
                data.get("content", "")
            )
        
        elif operation == "list_directory":
            return fs.list_directory(data.get("path", ""))
        
        elif operation == "create_directory":
            return fs.create_directory(data.get("path", ""))
        
        elif operation == "delete_file":
            return fs.delete_file(data.get("path", ""))
        
        elif operation == "delete_directory":
            return fs.delete_directory(
                data.get("path", ""),
                data.get("recursive", False)
            )
        
        elif operation == "move_file":
            return fs.move_file(
                data.get("source", ""),
                data.get("destination", "")
            )
        
        elif operation == "copy_file":
            return fs.copy_file(
                data.get("source", ""),
                data.get("destination", "")
            )
        
        elif operation == "get_file_info":
            return fs.get_file_info(data.get("path", ""))
        
        elif operation == "search_files":
            return fs.search_files(
                data.get("directory", ""),
                data.get("pattern", ""),
                data.get("recursive", True)
            )
        
        else:
            return {
                "success": False,
                "error": f"Unsupported operation: {operation}",
                "request": data
            }
    
    except Exception as e:
        log_message(f"Error processing filesystem request: {e}", "ERROR")
        return {
            "success": False,
            "error": str(e),
            "request": request_data
        }

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="AIArm FileSystem Operations")
    parser.add_argument("--input", type=str, help="Input JSON request")
    parser.add_argument("--json", action="store_true", help="Indicate that input is provided as JSON")
    args = parser.parse_args()
    
    try:
        log_message("FileSystem Operations starting")
        
        # Get the input
        if args.input:
            input_text = args.input
            log_message(f"Input provided via command line: {input_text[:100]}")
        else:
            # Read from stdin
            input_text = sys.stdin.read()
            log_message(f"Input provided via stdin: {input_text[:100]}")
        
        # Process the request
        result = process_filesystem_request(input_text)
        
        # Output the result
        output = json.dumps(result, indent=2, ensure_ascii=False)
        log_message(f"Returning result: {output[:200]}")
        print(output)
        
    except Exception as e:
        log_message(f"Error in main: {e}", "ERROR")
        traceback.print_exc()
        
        error_result = {
            "success": False,
            "error": str(e),
            "request": args.input
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
    
    log_message("FileSystem Operations execution completed")

if __name__ == "__main__":
    main()