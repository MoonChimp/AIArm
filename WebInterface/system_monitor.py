#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HRM System Monitor
Continuously monitors the HRM system and logs status information
"""

import os
import sys
import json
import time
import requests
import traceback
from pathlib import Path
from datetime import datetime

# Configuration
MONITOR_INTERVAL = 60  # Check system status every 60 seconds
STATUS_ENDPOINT = "http://localhost:45678/api/status"
LOG_DIR = Path("D:/AIArm/Logs/Monitor")
LOG_DIR.mkdir(exist_ok=True, parents=True)
MONITOR_LOG = LOG_DIR / f"hrm_monitor_{datetime.now().strftime('%Y%m%d')}.log"
ALERT_LOG = LOG_DIR / f"hrm_alerts_{datetime.now().strftime('%Y%m%d')}.log"
SERVICE_STATUS_FILE = Path("D:/AIArm/WebInterface/service_status.txt")

# Status thresholds
MAX_RESPONSE_TIME = 5.0  # Maximum acceptable response time in seconds
MAX_PENDING_REQUESTS = 3  # Maximum number of pending requests per bridge

def log_message(message, level="INFO", alert=False):
    """Log a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    # Print to console
    print(log_entry.strip())
    
    # Write to log file
    try:
        log_file = ALERT_LOG if alert else MONITOR_LOG
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

def check_system_status():
    """Check the status of the HRM system"""
    try:
        start_time = time.time()
        response = requests.get(STATUS_ENDPOINT, timeout=MAX_RESPONSE_TIME)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Update service status file
            update_service_status(True, response_time, data)
            
            # Log basic status
            log_message(f"System status: OK (Response time: {response_time:.2f}s)")
            
            # Check bridge status
            surface_status = data.get("status", {}).get("surface_bridge", "unknown")
            deep_status = data.get("status", {}).get("deep_bridge", "unknown")
            
            log_message(f"Surface bridge: {surface_status}, Deep bridge: {deep_status}")
            
            # Check for pending requests
            metrics = data.get("status", {}).get("metrics", {})
            pending_requests = metrics.get("pendingRequests", {})
            surface_pending = pending_requests.get("surface", 0)
            deep_pending = pending_requests.get("deep", 0)
            
            log_message(f"Pending requests - Surface: {surface_pending}, Deep: {deep_pending}")
            
            # Alert on issues
            if surface_status != "running" and surface_status != "responding with errors":
                log_message(f"ALERT: Surface bridge is not running: {surface_status}", "ERROR", alert=True)
            
            if deep_status != "running" and deep_status != "responding with errors":
                log_message(f"ALERT: Deep bridge is not running: {deep_status}", "ERROR", alert=True)
            
            if surface_pending > MAX_PENDING_REQUESTS:
                log_message(f"ALERT: Too many pending requests for Surface bridge: {surface_pending}", "WARNING", alert=True)
            
            if deep_pending > MAX_PENDING_REQUESTS:
                log_message(f"ALERT: Too many pending requests for Deep bridge: {deep_pending}", "WARNING", alert=True)
            
            if response_time > MAX_RESPONSE_TIME * 0.8:
                log_message(f"ALERT: System response time is slow: {response_time:.2f}s", "WARNING", alert=True)
            
            return True, data
        else:
            log_message(f"ALERT: System returned error status code: {response.status_code}", "ERROR", alert=True)
            update_service_status(False, response_time, {"error": f"Status code: {response.status_code}"})
            return False, None
    except requests.exceptions.Timeout:
        log_message("ALERT: System status check timed out", "ERROR", alert=True)
        update_service_status(False, MAX_RESPONSE_TIME, {"error": "Timeout"})
        return False, None
    except requests.exceptions.ConnectionError:
        log_message("ALERT: Could not connect to system", "ERROR", alert=True)
        update_service_status(False, 0, {"error": "Connection refused"})
        return False, None
    except Exception as e:
        log_message(f"ALERT: Error checking system status: {e}", "ERROR", alert=True)
        update_service_status(False, 0, {"error": str(e)})
        return False, None

def update_service_status(is_running, response_time, status_data):
    """Update the service status file with current system state"""
    try:
        status = {
            "timestamp": datetime.now().isoformat(),
            "is_running": is_running,
            "response_time": response_time,
            "status": status_data
        }
        
        with open(SERVICE_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)
    except Exception as e:
        log_message(f"Error updating service status file: {e}", "ERROR")

def monitor_loop():
    """Main monitoring loop"""
    log_message("Starting HRM System Monitor")
    log_message(f"Monitoring system at {STATUS_ENDPOINT}")
    log_message(f"Checking every {MONITOR_INTERVAL} seconds")
    log_message(f"Logs will be written to {LOG_DIR}")
    
    consecutive_failures = 0
    max_consecutive_failures = 5
    
    while True:
        try:
            success, _ = check_system_status()
            
            if success:
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                
                if consecutive_failures >= max_consecutive_failures:
                    log_message(f"ALERT: System has failed {consecutive_failures} consecutive checks", "CRITICAL", alert=True)
                    log_message("Recommend restarting the HRM system", "CRITICAL", alert=True)
            
            # Wait for next check
            time.sleep(MONITOR_INTERVAL)
        except KeyboardInterrupt:
            log_message("Monitor stopped by user", "INFO")
            break
        except Exception as e:
            log_message(f"Error in monitor loop: {e}", "ERROR")
            traceback.print_exc()
            time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    try:
        log_message("=" * 80)
        log_message("HRM System Monitor Starting")
        log_message("=" * 80)
        
        # Parse command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == "--interval":
            try:
                MONITOR_INTERVAL = int(sys.argv[2])
                log_message(f"Using custom interval: {MONITOR_INTERVAL} seconds")
            except (IndexError, ValueError):
                log_message("Invalid interval argument. Using default interval.")
        
        monitor_loop()
    except KeyboardInterrupt:
        log_message("Monitor stopped by user", "INFO")
    except Exception as e:
        log_message(f"Unhandled exception: {e}", "CRITICAL", alert=True)
        traceback.print_exc()
        sys.exit(1)
