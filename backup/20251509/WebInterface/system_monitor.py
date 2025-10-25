"""
System Monitor for Nexus HRM Architecture
Provides real-time monitoring and automatic recovery for system components
"""

import os
import sys
import time
import psutil
import requests
import datetime
import subprocess
import threading
import json
import logging
from pathlib import Path

# Load configuration
config_path = "D:/AIArm/WebInterface/config.json"
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    print(f"Configuration loaded from {config_path}")
except Exception as e:
    print(f"Error loading configuration: {e}")
    config = {
        "paths": {
            "base": "D:/AIArm",
            "web": "D:/AIArm/WebInterface",
            "innerLife": "D:/AIArm/InnerLife",
            "logs": "D:/AIArm/WebInterface/logs"
        },
        "system": {
            "checkInterval": 30,
            "statsInterval": 300,
            "restartThreshold": 3,
            "maxCpuUsage": 90,
            "maxMemoryUsage": 90,
            "maxDiskUsage": 90
        },
        "server": {
            "port": 45678
        }
    }
    print("Using default configuration")

# Configure logging
log_path = os.path.join(config["paths"]["logs"], "system_monitor.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SystemMonitor")

class SystemMonitor:
    """Monitor and maintain the Nexus HRM system"""
    
    def __init__(self):
        self.base_dir = Path(config["paths"]["base"])
        self.web_dir = Path(config["paths"]["web"])
        self.inner_life_dir = Path(config["paths"]["innerLife"])
        
        # Component status
        self.components = {
            "inner_life": {"active": False, "last_check": None, "process": None},
            "agent_manager": {"active": False, "last_check": None, "process": None},
            "memory_visualizer": {"active": False, "last_check": None, "process": None},
            "agent_integration": {"active": False, "last_check": None, "process": None},
            "server": {"active": False, "last_check": None, "process": None}
        }
        
        # Server info
        self.server_port = config["server"]["port"]
        
        # Monitoring intervals
        self.check_interval = config["system"]["checkInterval"]  # seconds
        self.stats_interval = config["system"]["statsInterval"]  # seconds
        
        # Recovery thresholds
        self.restart_threshold = config["system"]["restartThreshold"]  # failed checks before restart
        self.component_failures = {comp: 0 for comp in self.components}
        
        # Resource thresholds
        self.max_cpu_usage = config["system"]["maxCpuUsage"]
        self.max_memory_usage = config["system"]["maxMemoryUsage"]
        self.max_disk_usage = config["system"]["maxDiskUsage"]
        
        logger.info(f"System Monitor initialized - Server port: {self.server_port}")
    
    def _get_server_port(self):
        """Determine the port used by the server"""
        # Default port
        port = 45678
        
        # Check if a different port is specified in the startup script
        try:
            with open(self.base_dir / "start_nexus_hrm.bat", "r") as f:
                content = f.read()
                if "set PORT=" in content:
                    for line in content.split("\n"):
                        if line.strip().startswith("set PORT="):
                            port = int(line.strip().split("=")[1])
                            break
        except Exception as e:
            logger.error(f"Error reading port from startup script: {e}")
        
        return port
    
    def check_component_processes(self):
        """Check if component processes are running"""
        # Process name patterns to look for
        process_patterns = {
            "inner_life": "inner_life_processor.py",
            "agent_manager": "agent_manager.py",
            "memory_visualizer": "memory_visualizer.py",
            "agent_integration": "agent_integration.py",
            "server": "concurrent_server.js"
        }
        
        # Check each process
        for name, pattern in process_patterns.items():
            found = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.cmdline())
                    if pattern in cmdline:
                        self.components[name]["active"] = True
                        self.components[name]["last_check"] = datetime.datetime.now()
                        self.components[name]["process"] = proc
                        found = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            if not found:
                if self.components[name]["active"]:
                    logger.warning(f"Component {name} is no longer active")
                self.components[name]["active"] = False
                self.component_failures[name] += 1
            else:
                self.component_failures[name] = 0
    
    def check_server_health(self):
        """Check if the server is responding to health checks"""
        try:
            response = requests.get(f"http://localhost:{self.server_port}/health", timeout=5)
            if response.status_code == 200:
                self.components["server"]["active"] = True
                self.components["server"]["last_check"] = datetime.datetime.now()
                self.component_failures["server"] = 0
                return True
            else:
                logger.warning(f"Server health check failed: HTTP {response.status_code}")
                self.component_failures["server"] += 1
                return False
        except requests.RequestException as e:
            logger.warning(f"Server health check failed: {str(e)}")
            self.component_failures["server"] += 1
            return False
    
    def restart_component(self, component):
        """Restart a specific component"""
        logger.info(f"Attempting to restart {component}...")
        
        # Commands to restart each component
        restart_commands = {
            "inner_life": ["python", str(self.inner_life_dir / "inner_life_processor.py")],
            "agent_manager": ["python", str(self.inner_life_dir / "Agents" / "agent_manager.py")],
            "memory_visualizer": ["python", str(self.inner_life_dir / "memory_visualizer.py")],
            "agent_integration": ["python", str(self.inner_life_dir / "agent_integration.py")],
            "server": ["node", str(self.web_dir / "concurrent_server.js"), "--port", str(self.server_port)]
        }
        
        # Kill the existing process if it exists
        if self.components[component]["process"]:
            try:
                process = self.components[component]["process"]
                if process.is_running():
                    process.terminate()
                    process.wait(timeout=10)
            except Exception as e:
                logger.error(f"Error terminating {component} process: {e}")
        
        # Start the new process
        try:
            if component == "server":
                # For server, change to the WebInterface directory
                process = subprocess.Popen(
                    restart_commands[component],
                    cwd=str(self.web_dir)
                )
            else:
                process = subprocess.Popen(restart_commands[component])
            
            self.components[component]["process"] = psutil.Process(process.pid)
            logger.info(f"Successfully restarted {component}")
            
            # Allow time for the process to initialize
            time.sleep(5)
            
            # Reset failure counter
            self.component_failures[component] = 0
            return True
        except Exception as e:
            logger.error(f"Failed to restart {component}: {e}")
            return False
    
    def check_system_resources(self):
        """Check system resources and log stats"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Log the stats
            logger.info(f"System Resources - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")
            
            # Check if resources are critically low
            critical = False
            if cpu_percent > self.max_cpu_usage:
                logger.warning(f"CRITICAL: CPU usage is very high: {cpu_percent}%")
                critical = True
            if memory_percent > self.max_memory_usage:
                logger.warning(f"CRITICAL: Memory usage is very high: {memory_percent}%")
                critical = True
            if disk_percent > self.max_disk_usage:
                logger.warning(f"CRITICAL: Disk usage is very high: {disk_percent}%")
                critical = True
            
            return not critical
        except Exception as e:
            logger.error(f"Error checking system resources: {e}")
            return False
    
    def recovery_needed(self, component):
        """Determine if recovery is needed for a component"""
        return self.component_failures[component] >= self.restart_threshold
    
    def perform_recovery(self):
        """Check components and perform recovery if needed"""
        # Check all component processes
        self.check_component_processes()
        
        # Check server health specifically
        self.check_server_health()
        
        # Log component status
        status_str = " | ".join([f"{c}: {'✓' if s['active'] else '✗'}" for c, s in self.components.items()])
        logger.info(f"Component Status: {status_str}")
        
        # Attempt recovery for failed components
        for component, failures in self.component_failures.items():
            if self.recovery_needed(component):
                logger.warning(f"{component} has failed {failures} consecutive checks - attempting recovery")
                self.restart_component(component)
    
    def run(self):
        """Main monitoring loop"""
        logger.info("Starting system monitoring")
        
        stats_timer = 0
        
        try:
            while True:
                # Perform recovery checks
                self.perform_recovery()
                
                # Check system resources periodically
                stats_timer += self.check_interval
                if stats_timer >= self.stats_interval:
                    self.check_system_resources()
                    stats_timer = 0
                
                # Wait until next check
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logger.info("System monitoring stopped by user")
        except Exception as e:
            logger.error(f"System monitoring error: {e}")
            logger.info("Restarting monitoring...")
            time.sleep(5)
            self.run()

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run()
