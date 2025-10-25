#!/usr/bin/env python
"""
Port Checker - This script will check if the ports used by AIArm services are available
and suggest actions if they are in use by other processes.
"""

import os
import sys
import socket
import subprocess
import re
import platform

# Ports used by AIArm services
PORTS_TO_CHECK = [3000, 3100, 3200, 8000, 8080, 45678, 45679, 45680]

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_process_using_port(port):
    """Get the process ID using a port"""
    system = platform.system()
    
    if system == "Windows":
        try:
            # Windows command to get process using port
            netstat_output = subprocess.check_output(f'netstat -ano | findstr ":{port}"', shell=True).decode()
            if netstat_output:
                # Extract PID from the last column
                lines = netstat_output.strip().split('\n')
                for line in lines:
                    if f":{port}" in line and ("LISTENING" in line or "ESTABLISHED" in line):
                        pid = line.strip().split()[-1]
                        return pid
        except subprocess.CalledProcessError:
            pass
    elif system == "Linux" or system == "Darwin":  # Linux or macOS
        try:
            # Linux/macOS command to get process using port
            if system == "Linux":
                lsof_output = subprocess.check_output(f'lsof -i :{port} -t', shell=True).decode()
            else:  # macOS
                lsof_output = subprocess.check_output(f'lsof -i tcp:{port} -t', shell=True).decode()
            
            if lsof_output:
                pid = lsof_output.strip().split('\n')[0]
                return pid
        except subprocess.CalledProcessError:
            pass
    
    return None

def get_process_name(pid):
    """Get the name of a process by its PID"""
    system = platform.system()
    
    if system == "Windows":
        try:
            tasklist_output = subprocess.check_output(f'tasklist /FI "PID eq {pid}" /NH', shell=True).decode()
            if tasklist_output and not "No tasks" in tasklist_output:
                # Extract process name from the first column
                process_name = tasklist_output.strip().split()[0]
                return process_name
        except subprocess.CalledProcessError:
            pass
    elif system == "Linux":
        try:
            ps_output = subprocess.check_output(f'ps -p {pid} -o comm=', shell=True).decode()
            if ps_output:
                return ps_output.strip()
        except subprocess.CalledProcessError:
            pass
    elif system == "Darwin":  # macOS
        try:
            ps_output = subprocess.check_output(f'ps -p {pid} -o comm=', shell=True).decode()
            if ps_output:
                return ps_output.strip()
        except subprocess.CalledProcessError:
            pass
    
    return "Unknown Process"

def format_output(message, color=None):
    """Format console output with colors if supported"""
    if platform.system() == "Windows":
        os.system("")  # Enable VT100 escape sequences on Windows
    
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    
    if color and color in colors:
        return f"{colors[color]}{message}{colors['reset']}"
    else:
        return message

def main():
    """Main function to check port availability"""
    print(format_output("AIArm Port Checker", "blue"))
    print(format_output("====================", "blue"))
    print()
    
    all_ports_available = True
    
    for port in PORTS_TO_CHECK:
        if is_port_in_use(port):
            all_ports_available = False
            pid = get_process_using_port(port)
            process_name = get_process_name(pid) if pid else "Unknown Process"
            
            print(format_output(f"Port {port} is in use by {process_name} (PID: {pid})", "red"))
            
            # Suggest actions
            if pid:
                print(format_output(f"  To free this port, you can:", "yellow"))
                if platform.system() == "Windows":
                    print(format_output(f"  - Run: taskkill /F /PID {pid}", "yellow"))
                else:
                    print(format_output(f"  - Run: kill {pid}", "yellow"))
                
                if process_name in ["node.exe", "node", "python.exe", "python", "pythonw.exe"]:
                    print(format_output(f"  This appears to be another AIArm service. You may want to stop it first.", "yellow"))
        else:
            print(format_output(f"Port {port} is available", "green"))
    
    print()
    if all_ports_available:
        print(format_output("All required ports are available. AIArm services can start normally.", "green"))
    else:
        print(format_output("Some ports are in use. Consider freeing them before starting AIArm services.", "yellow"))
        print(format_output("You can also modify the port numbers in the configuration files.", "yellow"))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
