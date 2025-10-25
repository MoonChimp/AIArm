#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HRM System Test Script
Tests the concurrent operation of both bridges in the HRM architecture
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime

# Configuration
TEST_PORT = 45678
TEST_ENDPOINT = f"http://localhost:{TEST_PORT}/api/process"
TEST_STATUS_ENDPOINT = f"http://localhost:{TEST_PORT}/api/status"
LOGS_DIR = Path("D:/AIArm/Logs")
LOGS_DIR.mkdir(exist_ok=True, parents=True)

# Create a log file for this test
LOG_FILE = LOGS_DIR / f"hrm_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def check_server_status():
    """Check if the HRM server is running"""
    try:
        response = requests.get(TEST_STATUS_ENDPOINT, timeout=5)
        if response.status_code == 200:
            data = response.json()
            log_message("Server status check successful", "INFO")
            log_message(f"Status data: {json.dumps(data, indent=2)}", "DEBUG")
            return True, data
        else:
            log_message(f"Server returned status code {response.status_code}", "ERROR")
            return False, None
    except requests.exceptions.ConnectionError:
        log_message("Could not connect to server. Is the HRM system running?", "ERROR")
        return False, None
    except Exception as e:
        log_message(f"Error checking server status: {e}", "ERROR")
        return False, None

def test_request(prompt, agent="orchestrator", user_id="test_user"):
    """Send a test request to the HRM system"""
    log_message(f"Sending test request: '{prompt}' to agent: {agent}", "INFO")
    
    try:
        # Prepare the request
        data = {
            "input": prompt,
            "activeAgent": agent,
            "userId": user_id
        }
        
        # Send the request
        start_time = time.time()
        response = requests.post(TEST_ENDPOINT, json=data, timeout=30)
        processing_time = time.time() - start_time
        
        log_message(f"Request processed in {processing_time:.2f} seconds", "INFO")
        
        if response.status_code == 200:
            result = response.json()
            
            # Check for errors
            if not result.get("success", False):
                log_message(f"Request returned error: {result.get('error', 'Unknown error')}", "ERROR")
                return False, result
            
            # Check for non-empty response
            response_text = result.get("response", "")
            if not response_text:
                log_message("Request returned empty response", "ERROR")
                return False, result
            
            # Check if the response includes metadata for both bridges
            metadata = result.get("metadata", {})
            has_surface = "surface" in metadata
            has_deep = "deep" in metadata
            
            if has_surface and has_deep:
                log_message("✅ Response includes data from both bridges", "INFO")
            elif has_surface:
                log_message("⚠️ Response only includes data from surface bridge", "WARN")
            elif has_deep:
                log_message("⚠️ Response only includes data from deep bridge", "WARN")
            else:
                log_message("❌ Response doesn't include bridge metadata", "WARN")
            
            # Log response preview
            preview = response_text[:100] + "..." if len(response_text) > 100 else response_text
            log_message(f"Response preview: {preview}", "INFO")
            
            return True, result
        else:
            log_message(f"Request failed with status code {response.status_code}", "ERROR")
            return False, None
    except Exception as e:
        log_message(f"Error sending test request: {e}", "ERROR")
        return False, None

def run_test_battery():
    """Run a battery of tests on the HRM system"""
    log_message("Starting HRM system test battery", "INFO")
    
    # Check server status
    log_message("Checking server status...", "INFO")
    status_ok, status_data = check_server_status()
    
    if not status_ok:
        log_message("❌ Server status check failed. Aborting tests.", "ERROR")
        return False
    
    log_message("✅ Server is running", "INFO")
    
    # Test various agents and request types
    tests = [
        {
            "name": "Basic Greeting",
            "prompt": "Hello, how are you today?",
            "agent": "orchestrator"
        },
        {
            "name": "Reasoning Question",
            "prompt": "What are the ethical implications of artificial intelligence?",
            "agent": "reasoning"
        },
        {
            "name": "Code Request",
            "prompt": "Write a Python function to find the nth Fibonacci number.",
            "agent": "code"
        },
        {
            "name": "Design Question",
            "prompt": "What are good color combinations for a financial website?",
            "agent": "design"
        },
        {
            "name": "Planning Request",
            "prompt": "Help me create a roadmap for launching a mobile app.",
            "agent": "planning"
        }
    ]
    
    results = []
    
    for test in tests:
        log_message(f"Running test: {test['name']}", "INFO")
        success, result = test_request(test["prompt"], test["agent"])
        
        results.append({
            "test": test["name"],
            "success": success,
            "agent": test["agent"],
            "response_length": len(result.get("response", "")) if result else 0,
            "has_metadata": "metadata" in result if result else False,
            "has_both_bridges": ("metadata" in result and 
                               "surface" in result["metadata"] and 
                               "deep" in result["metadata"]) if result else False
        })
        
        # Wait between tests to avoid overwhelming the system
        time.sleep(2)
    
    # Summarize results
    log_message("\nTest Results Summary:", "INFO")
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    log_message(f"Passed: {passed}/{total} ({passed/total*100:.1f}%)", "INFO")
    
    for i, result in enumerate(results):
        status = "✅" if result["success"] else "❌"
        bridge_status = "✅ Both" if result["has_both_bridges"] else "⚠️ Single"
        log_message(f"{status} Test {i+1}: {result['test']} ({result['agent']}) - {bridge_status} bridge(s)", "INFO")
    
    # Check for overall success
    if passed == total:
        log_message("\n✅ All tests passed successfully! The HRM system is working correctly.", "INFO")
        return True
    else:
        log_message(f"\n⚠️ {total-passed} tests failed. The HRM system may need adjustment.", "WARN")
        return False

if __name__ == "__main__":
    log_message("=" * 80, "INFO")
    log_message("HRM System Test Script", "INFO")
    log_message("=" * 80, "INFO")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        try:
            TEST_PORT = int(sys.argv[2])
            TEST_ENDPOINT = f"http://localhost:{TEST_PORT}/api/process"
            TEST_STATUS_ENDPOINT = f"http://localhost:{TEST_PORT}/api/status"
            log_message(f"Using custom port: {TEST_PORT}", "INFO")
        except (IndexError, ValueError):
            log_message("Invalid port argument. Using default port.", "WARN")
    
    log_message(f"Testing server at: http://localhost:{TEST_PORT}", "INFO")
    success = run_test_battery()
    
    if success:
        log_message("\nHRM System Test completed successfully!", "INFO")
        sys.exit(0)
    else:
        log_message("\nHRM System Test completed with failures.", "WARN")
        sys.exit(1)
