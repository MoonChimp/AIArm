#!/usr/bin/env python3
"""
Diagnostic Bridge for AlfaZer0 - Debug version

This script is specifically designed to diagnose why commands work in terminal 
but not through the web interface.
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

LOG_FILE = LOGS_DIR / "diagnostic_bridge.log"

# Log function
def log_message(message, level="INFO"):
    """Write a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    
    # Print to console
    print(f"DIAGNOSTIC: {log_line}", file=sys.stderr)
    
    # Write to log file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"ERROR WRITING TO LOG: {str(e)}", file=sys.stderr)

# Dump environment details
def dump_environment():
    """Dump all environment details to the log for diagnosis"""
    log_message("========== DIAGNOSTIC INFO ==========")
    
    # Current directory
    log_message(f"Current directory: {os.getcwd()}")
    
    # Script path
    log_message(f"Script path: {os.path.abspath(__file__)}")
    
    # User info
    try:
        log_message(f"Username: {os.getlogin()}")
    except:
        log_message("Could not get username", "WARNING")
    
    # Admin status
    try:
        is_admin = os.geteuid() == 0  # Unix
    except AttributeError:
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0  # Windows
        except:
            is_admin = "Unknown"
    log_message(f"Running as admin: {is_admin}")
    
    # Environment variables
    log_message("Environment variables:")
    for key, value in os.environ.items():
        log_message(f"  {key}={value}")
    
    # Python info
    log_message(f"Python version: {sys.version}")
    log_message(f"Python executable: {sys.executable}")
    
    # Test file access
    test_paths = ["D:/", "C:/", "D:/AIArm/Test"]
    log_message("Testing path access:")
    for p in test_paths:
        try:
            if os.path.exists(p):
                log_message(f"  Can access {p}: YES")
            else:
                log_message(f"  Can access {p}: NO (path doesn't exist)")
        except Exception as e:
            log_message(f"  Can access {p}: ERROR - {str(e)}")
    
    # Test file creation
    test_file = Path("D:/AIArm/Test/diagnostic_test.txt")
    try:
        with open(test_file, "w") as f:
            f.write(f"Diagnostic test at {datetime.now()}")
        log_message(f"Created test file: {test_file}")
    except Exception as e:
        log_message(f"Failed to create test file: {str(e)}", "ERROR")
    
    log_message("======================================")

# Execute a direct file write test
def direct_file_write_test():
    """Try to write a file using direct Python file operations"""
    try:
        test_file = Path("D:/AIArm/Test/direct_test.txt")
        with open(test_file, "w") as f:
            f.write(f"Direct file write test at {datetime.now()}")
        
        log_message(f"Direct file write successful: {test_file}")
        return {
            "success": True,
            "message": f"Successfully created file at {test_file}",
            "path": str(test_file)
        }
    except Exception as e:
        error_msg = f"Direct file write failed: {str(e)}"
        log_message(error_msg, "ERROR")
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": error_msg
        }

# Execute a subprocess file write test
def subprocess_file_write_test():
    """Try to write a file using subprocess"""
    try:
        # Use a simple command to write to a file
        if os.name == 'nt':  # Windows
            command = f'echo Subprocess test at {datetime.now()} > D:\\AIArm\\Test\\subprocess_test.txt'
            process = subprocess.run(command, shell=True, check=True, capture_output=True)
        else:  # Unix
            command = f'echo "Subprocess test at {datetime.now()}" > /tmp/subprocess_test.txt'
            process = subprocess.run(command, shell=True, check=True, capture_output=True)
        
        log_message(f"Subprocess command executed: {command}")
        log_message(f"Subprocess stdout: {process.stdout.decode('utf-8', errors='replace')}")
        log_message(f"Subprocess stderr: {process.stderr.decode('utf-8', errors='replace')}")
        
        # Verify the file was created
        test_file = "D:\\AIArm\\Test\\subprocess_test.txt" if os.name == 'nt' else "/tmp/subprocess_test.txt"
        if os.path.exists(test_file):
            log_message(f"Subprocess file write successful: {test_file}")
            return {
                "success": True,
                "message": f"Successfully created file at {test_file}",
                "path": test_file
            }
        else:
            raise Exception(f"File {test_file} was not created")
    except Exception as e:
        error_msg = f"Subprocess file write failed: {str(e)}"
        log_message(error_msg, "ERROR")
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": error_msg
        }

# Run a basic file command through bridge
def try_bridge_file_write():
    """Try to write a file using the alfazer0_bridge.py script"""
    bridge_path = Path(os.path.dirname(os.path.abspath(__file__))) / "alfazer0_bridge.py"
    if not bridge_path.exists():
        log_message(f"Bridge script not found at: {bridge_path}", "ERROR")
        return {
            "success": False,
            "error": f"Bridge script not found at: {bridge_path}"
        }
    
    try:
        request_data = json.dumps({
            "operation": "write_file",
            "path": "D:/AIArm/Test/bridge_test.txt",
            "content": f"Bridge test at {datetime.now()}"
        })
        
        log_message(f"Attempting to run bridge: {bridge_path}")
        log_message(f"Request data: {request_data}")
        
        process = subprocess.Popen(
            [sys.executable, str(bridge_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=request_data)
        
        log_message(f"Bridge process exit code: {process.returncode}")
        log_message(f"Bridge stdout: {stdout}")
        log_message(f"Bridge stderr: {stderr}")
        
        if process.returncode == 0:
            try:
                result = json.loads(stdout)
                log_message(f"Bridge result: {result}")
                return {
                    "success": True,
                    "message": f"Bridge test successful: {stdout}",
                    "bridge_result": result
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Failed to parse bridge output",
                    "output": stdout
                }
        else:
            return {
                "success": False,
                "error": f"Bridge process failed with code {process.returncode}",
                "stderr": stderr
            }
    except Exception as e:
        error_msg = f"Bridge execution failed: {str(e)}"
        log_message(error_msg, "ERROR")
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": error_msg
        }

# Main function
def main():
    try:
        # First, dump environment details for diagnostics
        dump_environment()
        
        # Try direct file creation
        direct_result = direct_file_write_test()
        
        # Try subprocess file creation
        subprocess_result = subprocess_file_write_test()
        
        # Try bridge file creation
        bridge_result = try_bridge_file_write()
        
        # Combine all results
        diagnostic_results = {
            "success": direct_result["success"] or subprocess_result["success"] or bridge_result["success"],
            "direct_test": direct_result,
            "subprocess_test": subprocess_result,
            "bridge_test": bridge_result,
            "environment": {
                "cwd": os.getcwd(),
                "script_path": os.path.abspath(__file__),
                "is_admin": "Unknown"  # We already logged this in dump_environment
            }
        }
        
        # Generate user-friendly response
        if diagnostic_results["success"]:
            response = "Diagnostic tests completed. At least one test was successful. Check the logs for details."
            if direct_result["success"]:
                response += " Direct file creation worked."
            if subprocess_result["success"]:
                response += " Subprocess file creation worked."
            if bridge_result["success"]:
                response += " Bridge file creation worked."
        else:
            response = "All diagnostic tests failed. This suggests permission issues or path problems. Check the logs for details."
        
        # Combine into final result
        result = {
            "success": True,
            "response": response,
            "diagnostic_results": diagnostic_results
        }
        
        # Write results to a special diagnostic file as well
        with open("D:/AIArm/Logs/interface_diagnostic_results.json", "w") as f:
            json.dump(diagnostic_results, f, indent=2)
        
        # Return results in the expected format
        print(json.dumps(result))
    except Exception as e:
        log_message(f"Fatal error in diagnostic_bridge.py: {str(e)}", "ERROR")
        traceback.print_exc(file=sys.stderr)
        error_result = {
            "success": False,
            "error": str(e),
            "response": "Diagnostics encountered a critical error. Check the logs."
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
