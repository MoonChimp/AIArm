#!/usr/bin/env python3
"""
AlfaZer0 Advanced Bridge
Administrative Filesystem and System Capabilities for NexusAI:AlfaZer0
"""

import os
import sys
import json
import time
import shutil
import ctypes
import platform
import subprocess
from datetime import datetime
from pathlib import Path
import traceback

# Ensure we have admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    if not is_admin():
        print("Requesting administrative privileges...")
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Constants
LOGS_DIR = Path("D:/AIArm/Logs")
NEXUSAI_DIR = Path("D:/NexusAI")
SCRIPTS_DIR = NEXUSAI_DIR / "Scripts"
MODULES_DIR = NEXUSAI_DIR / "Modules"
KNOWLEDGE_DIR = NEXUSAI_DIR / "Knowledge"
USERDATA_DIR = NEXUSAI_DIR / "UserData"
INDEX_FILE = NEXUSAI_DIR / "index.json"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True, parents=True)
NEXUSAI_DIR.mkdir(exist_ok=True, parents=True)
SCRIPTS_DIR.mkdir(exist_ok=True, parents=True)
MODULES_DIR.mkdir(exist_ok=True, parents=True)
KNOWLEDGE_DIR.mkdir(exist_ok=True, parents=True)
USERDATA_DIR.mkdir(exist_ok=True, parents=True)

# Create index file if it doesn't exist
if not INDEX_FILE.exists():
    with open(INDEX_FILE, 'w') as f:
        json.dump({
            "version": "1.0",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scripts": [],
            "modules": [],
            "capabilities": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2)

# Logging setup
LOG_FILE = LOGS_DIR / "alfazer0.log"

def log_message(message, level="INFO"):
    """Log a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    print(log_entry)
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

# Core filesystem operations with admin privileges
def read_file(file_path):
    """Read a file with administrative privileges"""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return {"success": False, "error": f"File not found: {file_path}"}
        
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        
        log_message(f"Read file: {file_path}")
        return {
            "success": True, 
            "content": content, 
            "path": str(file_path)
        }
    except Exception as e:
        error_msg = f"Error reading file {file_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def write_file(file_path, content):
    """Write to a file with administrative privileges"""
    try:
        file_path = Path(file_path)
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        log_message(f"Wrote to file: {file_path}")
        return {
            "success": True, 
            "path": str(file_path)
        }
    except Exception as e:
        error_msg = f"Error writing to file {file_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def append_file(file_path, content):
    """Append to a file with administrative privileges"""
    try:
        file_path = Path(file_path)
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
        
        log_message(f"Appended to file: {file_path}")
        return {
            "success": True, 
            "path": str(file_path)
        }
    except Exception as e:
        error_msg = f"Error appending to file {file_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def list_directory(dir_path):
    """List contents of a directory with administrative privileges"""
    try:
        dir_path = Path(dir_path)
        if not dir_path.exists():
            return {"success": False, "error": f"Directory not found: {dir_path}"}
        
        items = []
        for item in dir_path.iterdir():
            item_type = "directory" if item.is_dir() else "file"
            items.append({
                "name": item.name,
                "type": item_type,
                "path": str(item)
            })
        
        log_message(f"Listed directory: {dir_path}")
        return {
            "success": True, 
            "items": items, 
            "path": str(dir_path)
        }
    except Exception as e:
        error_msg = f"Error listing directory {dir_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def create_directory(dir_path):
    """Create a directory with administrative privileges"""
    try:
        dir_path = Path(dir_path)
        dir_path.mkdir(exist_ok=True, parents=True)
        
        log_message(f"Created directory: {dir_path}")
        return {
            "success": True, 
            "path": str(dir_path)
        }
    except Exception as e:
        error_msg = f"Error creating directory {dir_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def delete_file(file_path):
    """Delete a file with administrative privileges"""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return {"success": False, "error": f"File not found: {file_path}"}
        
        file_path.unlink()
        
        log_message(f"Deleted file: {file_path}")
        return {
            "success": True, 
            "path": str(file_path)
        }
    except Exception as e:
        error_msg = f"Error deleting file {file_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def delete_directory(dir_path, recursive=False):
    """Delete a directory with administrative privileges"""
    try:
        dir_path = Path(dir_path)
        if not dir_path.exists():
            return {"success": False, "error": f"Directory not found: {dir_path}"}
        
        if recursive:
            shutil.rmtree(dir_path)
        else:
            dir_path.rmdir()
        
        log_message(f"Deleted directory: {dir_path}")
        return {
            "success": True, 
            "path": str(dir_path)
        }
    except Exception as e:
        error_msg = f"Error deleting directory {dir_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def execute_command(command, capture_output=True):
    """Execute a system command with administrative privileges"""
    try:
        log_message(f"Executing command: {command}")
        
        if capture_output:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            output = result.stdout
            error = result.stderr
            
            return {
                "success": result.returncode == 0,
                "output": output,
                "error": error,
                "return_code": result.returncode,
                "command": command
            }
        else:
            subprocess.run(command, shell=True)
            return {
                "success": True,
                "command": command
            }
    except Exception as e:
        error_msg = f"Error executing command {command}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def get_file_info(file_path):
    """Get information about a file with administrative privileges"""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return {"success": False, "error": f"File not found: {file_path}"}
        
        stat_info = file_path.stat()
        
        info = {
            "path": str(file_path),
            "size": stat_info.st_size,
            "created": datetime.fromtimestamp(stat_info.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "accessed": datetime.fromtimestamp(stat_info.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
            "is_directory": file_path.is_dir(),
            "is_file": file_path.is_file()
        }
        
        if file_path.is_file() and file_path.suffix:
            info["extension"] = file_path.suffix
        
        log_message(f"Got file info: {file_path}")
        return {
            "success": True, 
            "info": info
        }
    except Exception as e:
        error_msg = f"Error getting file info for {file_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def search_files(dir_path, pattern):
    """Search for files matching a pattern with administrative privileges"""
    try:
        dir_path = Path(dir_path)
        if not dir_path.exists():
            return {"success": False, "error": f"Directory not found: {dir_path}"}
        
        matches = []
        for item in dir_path.glob(f"**/{pattern}"):
            item_type = "directory" if item.is_dir() else "file"
            matches.append({
                "name": item.name,
                "type": item_type,
                "path": str(item)
            })
        
        log_message(f"Searched files in {dir_path} for pattern {pattern}")
        return {
            "success": True, 
            "matches": matches, 
            "pattern": pattern,
            "directory": str(dir_path)
        }
    except Exception as e:
        error_msg = f"Error searching for files in {dir_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def copy_file(source_path, dest_path):
    """Copy a file with administrative privileges"""
    try:
        source_path = Path(source_path)
        dest_path = Path(dest_path)
        
        if not source_path.exists():
            return {"success": False, "error": f"Source file not found: {source_path}"}
        
        # Create parent directories if they don't exist
        dest_path.parent.mkdir(exist_ok=True, parents=True)
        
        shutil.copy2(source_path, dest_path)
        
        log_message(f"Copied file from {source_path} to {dest_path}")
        return {
            "success": True, 
            "source": str(source_path),
            "destination": str(dest_path)
        }
    except Exception as e:
        error_msg = f"Error copying file from {source_path} to {dest_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def move_file(source_path, dest_path):
    """Move a file with administrative privileges"""
    try:
        source_path = Path(source_path)
        dest_path = Path(dest_path)
        
        if not source_path.exists():
            return {"success": False, "error": f"Source file not found: {source_path}"}
        
        # Create parent directories if they don't exist
        dest_path.parent.mkdir(exist_ok=True, parents=True)
        
        shutil.move(source_path, dest_path)
        
        log_message(f"Moved file from {source_path} to {dest_path}")
        return {
            "success": True, 
            "source": str(source_path),
            "destination": str(dest_path)
        }
    except Exception as e:
        error_msg = f"Error moving file from {source_path} to {dest_path}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def get_system_info():
    """Get detailed system information"""
    try:
        info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
            "username": os.getlogin(),
            "hostname": platform.node(),
            "admin": is_admin()
        }
        
        # Get memory info using wmic on Windows
        if platform.system() == "Windows":
            mem_cmd = subprocess.run(
                "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            mem_result = mem_cmd.stdout.strip().split("\n")
            mem_data = {}
            for line in mem_result:
                if "=" in line:
                    key, value = line.split("=", 1)
                    mem_data[key.strip()] = value.strip()
            
            if "TotalVisibleMemorySize" in mem_data and mem_data["TotalVisibleMemorySize"]:
                info["total_memory_mb"] = round(int(mem_data["TotalVisibleMemorySize"]) / 1024)
            
            if "FreePhysicalMemory" in mem_data and mem_data["FreePhysicalMemory"]:
                info["free_memory_mb"] = round(int(mem_data["FreePhysicalMemory"]) / 1024)
        
        # Get disk info
        drives = {}
        for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                try:
                    total, used, free = shutil.disk_usage(drive_path)
                    drives[drive] = {
                        "total_gb": round(total / (1024**3), 2),
                        "used_gb": round(used / (1024**3), 2),
                        "free_gb": round(free / (1024**3), 2),
                        "percent_used": round((used / total) * 100, 2)
                    }
                except:
                    pass
        
        info["drives"] = drives
        
        log_message("Retrieved system information")
        return {
            "success": True, 
            "info": info
        }
    except Exception as e:
        error_msg = f"Error getting system information: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

# Self-expansion capabilities
def create_script(name, description, content=""):
    """Create a new script in the Scripts directory"""
    try:
        script_path = SCRIPTS_DIR / f"{name}.js"
        
        script_content = f"""// {name}
// Created by NexusAI:AlfaZer0 on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
// Description: {description}

{content}
"""
        
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # Update index
        update_index(name)
        
        log_message(f"Created script: {name}")
        return {
            "success": True, 
            "path": str(script_path),
            "name": name
        }
    except Exception as e:
        error_msg = f"Error creating script {name}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def create_module(name, description, content=""):
    """Create a new module in the Modules directory"""
    try:
        module_dir = MODULES_DIR / name
        module_dir.mkdir(exist_ok=True, parents=True)
        
        module_path = module_dir / "index.js"
        
        module_content = f"""// {name} Module
// Created by NexusAI:AlfaZer0 on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
// Description: {description}

{content}
"""
        
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(module_content)
        
        # Update index
        update_index(name)
        
        log_message(f"Created module: {name}")
        return {
            "success": True, 
            "path": str(module_path),
            "name": name
        }
    except Exception as e:
        error_msg = f"Error creating module {name}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def store_knowledge(name, content):
    """Store knowledge in the Knowledge directory"""
    try:
        knowledge_path = KNOWLEDGE_DIR / f"{name}.txt"
        
        knowledge_content = f"""// {name}
// Created by NexusAI:AlfaZer0 on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{content}
"""
        
        with open(knowledge_path, "w", encoding="utf-8") as f:
            f.write(knowledge_content)
        
        log_message(f"Stored knowledge: {name}")
        return {
            "success": True, 
            "path": str(knowledge_path),
            "name": name
        }
    except Exception as e:
        error_msg = f"Error storing knowledge {name}: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

def update_index(new_capability=None):
    """Update the capabilities index file"""
    try:
        if not INDEX_FILE.exists():
            # Create initial index
            index = {
                "version": "1.0",
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "scripts": [],
                "modules": [],
                "capabilities": [],
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            # Read existing index
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                index = json.load(f)
        
        # Update scripts list
        scripts = []
        for script_path in SCRIPTS_DIR.glob("*.js"):
            script_name = script_path.stem
            if script_name not in index["scripts"]:
                index["scripts"].append(script_name)
        
        # Update modules list
        modules = []
        for module_dir in MODULES_DIR.iterdir():
            if module_dir.is_dir():
                module_name = module_dir.name
                if module_name not in index["modules"]:
                    index["modules"].append(module_name)
        
        # Add new capability if provided
        if new_capability and new_capability not in index["capabilities"]:
            index["capabilities"].append(new_capability)
        
        # Update timestamp
        index["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write updated index
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
        
        log_message(f"Updated capabilities index")
        return {
            "success": True, 
            "index": index
        }
    except Exception as e:
        error_msg = f"Error updating index: {str(e)}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

# Function to handle request from the bridge
def handle_request(request_data):
    """Process a request and return the response"""
    try:
        operation = request_data.get("operation")
        
        # File operations
        if operation == "read_file":
            return read_file(request_data.get("path"))
        elif operation == "write_file":
            return write_file(request_data.get("path"), request_data.get("content"))
        elif operation == "append_file":
            return append_file(request_data.get("path"), request_data.get("content"))
        elif operation == "list_directory":
            return list_directory(request_data.get("path"))
        elif operation == "create_directory":
            return create_directory(request_data.get("path"))
        elif operation == "delete_file":
            return delete_file(request_data.get("path"))
        elif operation == "delete_directory":
            return delete_directory(request_data.get("path"), request_data.get("recursive", False))
        elif operation == "get_file_info":
            return get_file_info(request_data.get("path"))
        elif operation == "search_files":
            return search_files(request_data.get("directory"), request_data.get("pattern"))
        elif operation == "copy_file":
            return copy_file(request_data.get("source"), request_data.get("destination"))
        elif operation == "move_file":
            return move_file(request_data.get("source"), request_data.get("destination"))
        
        # System operations
        elif operation == "execute_command":
            return execute_command(request_data.get("command"), request_data.get("capture_output", True))
        elif operation == "get_system_info":
            return get_system_info()
        
        # Self-expansion operations
        elif operation == "create_script":
            return create_script(request_data.get("name"), request_data.get("description"), request_data.get("content", ""))
        elif operation == "create_module":
            return create_module(request_data.get("name"), request_data.get("description"), request_data.get("content", ""))
        elif operation == "store_knowledge":
            return store_knowledge(request_data.get("name"), request_data.get("content"))
        elif operation == "update_index":
            return update_index(request_data.get("new_capability"))
        
        # Unknown operation
        else:
            return {"success": False, "error": f"Unknown operation: {operation}"}
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}\n{traceback.format_exc()}"
        log_message(error_msg, "ERROR")
        return {"success": False, "error": error_msg}

# Main function for direct execution
def main():
    """Main function for processing requests"""
    # Ensure admin privileges
    if not is_admin():
        request_admin()
    
    log_message("Starting AlfaZer0 Administrative Bridge")
    
    # Create test file to confirm admin access
    test_file = Path("D:/AIArm/Test/alfazer0_bridge_test.txt")
    try:
        with open(test_file, "w") as f:
            f.write(f"AlfaZer0 Administrative Bridge Test\nCreated on: {datetime.now()}\nRunning with admin privileges: {is_admin()}")
        log_message(f"Created test file at {test_file}")
    except Exception as e:
        log_message(f"Error creating test file: {str(e)}", "ERROR")
    
    # Read input JSON from stdin
    input_data = sys.stdin.read()
    
    try:
        request_data = json.loads(input_data)
        response = handle_request(request_data)
    except json.JSONDecodeError:
        response = {"success": False, "error": "Invalid JSON input"}
    except Exception as e:
        response = {"success": False, "error": f"Error processing request: {str(e)}"}
    
    # Return JSON response
    print(json.dumps(response))

if __name__ == "__main__":
    main()
