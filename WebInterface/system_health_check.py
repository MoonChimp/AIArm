#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus HRM System Health Check
Diagnoses and reports system status and issues
"""

import os
import sys
import json
import socket
import subprocess
import time
from pathlib import Path

def check_port(port):
    """Check if a port is in use"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        s.bind(("localhost", port))
        result = True
    except socket.error:
        result = False
    finally:
        s.close()
    return result

def find_free_port(start_port, end_port=None):
    """Find a free port in a range"""
    if end_port is None:
        end_port = start_port + 100
    
    for port in range(start_port, end_port):
        if check_port(port):
            return port
    
    return None

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return True, {"status": "running", "models": [m.get("name") for m in models]}
        else:
            return False, {"status": "error", "message": f"API returned status code {response.status_code}"}
    except Exception as e:
        return False, {"status": "error", "message": str(e)}

def check_config(config_path):
    """Check if config.json is valid"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return True, {"status": "valid", "config": config}
    except json.JSONDecodeError as e:
        return False, {"status": "invalid", "message": str(e)}
    except FileNotFoundError:
        return False, {"status": "missing", "message": "Config file not found"}
    except Exception as e:
        return False, {"status": "error", "message": str(e)}

def check_bridge(bridge_path):
    """Check if a bridge file exists and is valid"""
    try:
        path = Path(bridge_path)
        if not path.exists():
            return False, {"status": "missing", "message": "Bridge file not found"}
        
        # Try to run the bridge with a test input
        try:
            proc = subprocess.Popen(
                [sys.executable, str(path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(input=json.dumps({"input": "test", "agent": "test", "user_id": "test"}), timeout=5)
            
            if proc.returncode != 0:
                return False, {"status": "error", "message": f"Bridge returned error code {proc.returncode}", "stderr": stderr}
            
            try:
                json.loads(stdout)
                return True, {"status": "valid", "message": "Bridge returns valid JSON"}
            except json.JSONDecodeError:
                return False, {"status": "invalid", "message": "Bridge does not return valid JSON", "stdout": stdout}
                
        except subprocess.TimeoutExpired:
            return False, {"status": "timeout", "message": "Bridge execution timed out"}
        except Exception as e:
            return False, {"status": "error", "message": f"Error executing bridge: {str(e)}"}
        
    except Exception as e:
        return False, {"status": "error", "message": str(e)}

def check_directory(directory_path):
    """Check if a directory exists and is writable"""
    try:
        path = Path(directory_path)
        if not path.exists():
            return False, {"status": "missing", "message": "Directory not found"}
        
        if not path.is_dir():
            return False, {"status": "not_directory", "message": "Path exists but is not a directory"}
        
        # Check if directory is writable
        test_file = path / f"test_{int(time.time())}.txt"
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            test_file.unlink()
            return True, {"status": "writable", "message": "Directory exists and is writable"}
        except Exception as e:
            return False, {"status": "not_writable", "message": f"Directory is not writable: {str(e)}"}
        
    except Exception as e:
        return False, {"status": "error", "message": str(e)}

def main():
    """Run system health check"""
    base_dir = Path("D:/AIArm")
    web_interface_dir = base_dir / "WebInterface"
    inner_life_dir = base_dir / "InnerLife"
    logs_dir = base_dir / "Logs"
    
    print("Nexus HRM System Health Check")
    print("============================\n")
    
    # Check directories
    print("Checking directories...")
    dirs_to_check = {
        "Base Directory": base_dir,
        "Web Interface Directory": web_interface_dir,
        "Inner Life Directory": inner_life_dir,
        "Logs Directory": logs_dir,
        "Generated Directory": inner_life_dir / "Generated",
        "Images Directory": inner_life_dir / "Generated" / "Images",
        "Videos Directory": inner_life_dir / "Generated" / "Videos",
        "Websites Directory": inner_life_dir / "Generated" / "Websites",
        "Agents Directory": inner_life_dir / "Agents",
        "Agent Config Directory": inner_life_dir / "Agents" / "config"
    }
    
    for name, path in dirs_to_check.items():
        status, info = check_directory(path)
        print(f"  {name}: {'✓' if status else '✗'} - {info['status']}")
        if not status:
            print(f"    Error: {info['message']}")
            # Try to create the directory if it doesn't exist
            if info['status'] == 'missing':
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"    Created directory: {path}")
                except Exception as e:
                    print(f"    Failed to create directory: {e}")
    
    print("\nChecking configuration...")
    config_path = web_interface_dir / "config.json"
    config_status, config_info = check_config(config_path)
    print(f"  Config file: {'✓' if config_status else '✗'} - {config_info['status']}")
    if not config_status:
        print(f"    Error: {config_info['message']}")
        
        # Try to repair config.json if needed
        if config_info['status'] == 'invalid' or config_info['status'] == 'missing':
            try:
                with open(config_path, 'w') as f:
                    json.dump({
                        "port": 45678,
                        "surfaceBridge": "improved_bridge.py",
                        "deepBridge": "ollama_bridge.py",
                        "timeoutMs": 120000,
                        "logLevel": "info",
                        "environment": "production",
                        "memoryEnabled": True,
                        "innerLifeEnabled": True,
                        "innerLifeDirectory": "D:/AIArm/InnerLife",
                        "memoryDirectory": "D:/AIArm/Memory",
                        "logDirectory": "D:/AIArm/Logs",
                        "responseConfiguration": {
                            "combinationMethod": "augment-surface",
                            "similarityThreshold": 0.5,
                            "preferDeepForDomains": ["reasoning", "philosophy", "creativity"]
                        },
                        "monitoring": {
                            "enableMetrics": True,
                            "enableHealthCheck": True,
                            "statusCheckIntervalMs": 300000
                        },
                        "caching": {
                            "enabled": True,
                            "ttl": 3600
                        },
                        "fallbackStrategy": "prefer-surface"
                    }, f, indent=2)
                print("    Repaired config.json with default values")
            except Exception as e:
                print(f"    Failed to repair config.json: {e}")
    
    print("\nChecking bridges...")
    surface_bridge_path = web_interface_dir / "improved_bridge.py"
    deep_bridge_path = web_interface_dir / "ollama_bridge.py"
    
    surface_status, surface_info = check_bridge(surface_bridge_path)
    print(f"  Surface Bridge: {'✓' if surface_status else '✗'} - {surface_info['status']}")
    if not surface_status:
        print(f"    Error: {surface_info['message']}")
    
    deep_status, deep_info = check_bridge(deep_bridge_path)
    print(f"  Deep Bridge: {'✓' if deep_status else '✗'} - {deep_info['status']}")
    if not deep_status:
        print(f"    Error: {deep_info['message']}")
    
    print("\nChecking Ollama...")
    ollama_status, ollama_info = check_ollama()
    print(f"  Ollama: {'✓' if ollama_status else '✗'} - {ollama_info['status']}")
    if not ollama_status:
        print(f"    Error: {ollama_info['message']}")
    else:
        print(f"    Available models: {', '.join(ollama_info['models'])}")
    
    print("\nChecking ports...")
    server_port = 45678
    port_status = check_port(server_port)
    print(f"  Port {server_port}: {'✓' if port_status else '✗'} - {'available' if port_status else 'in use'}")
    
    if not port_status:
        # Find an available port
        free_port = find_free_port(server_port + 1, server_port + 100)
        if free_port:
            print(f"    Suggested alternative port: {free_port}")
    
    print("\nSystem health check complete")
    
    # Summarize issues and suggest fixes
    issues = []
    if not config_status:
        issues.append(f"Config file issue: {config_info['status']} - {config_info['message']}")
    if not surface_status:
        issues.append(f"Surface Bridge issue: {surface_info['status']} - {surface_info['message']}")
    if not deep_status:
        issues.append(f"Deep Bridge issue: {deep_info['status']} - {deep_info['message']}")
    if not ollama_status:
        issues.append(f"Ollama issue: {ollama_info['status']} - {ollama_info['message']}")
    if not port_status:
        issues.append(f"Port {server_port} is already in use")
    
    if issues:
        print("\nIssues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\nRecommended actions:")
        if not config_status:
            print("  - Fix the config.json file with a valid JSON configuration")
        if not port_status:
            free_port = find_free_port(server_port + 1, server_port + 100)
            if free_port:
                print(f"  - Use an alternative port: {free_port}")
        if not ollama_status:
            print("  - Ensure Ollama is installed and running on port 11434")
        if not surface_status or not deep_status:
            print("  - Check the Python bridge files for errors")
    else:
        print("\nNo issues found! The system is healthy.")

if __name__ == "__main__":
    main()