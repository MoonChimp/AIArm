#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bridge Test Script
Tests both Surface and Deep bridges to ensure they're working properly
"""

import sys
import os
import json
import subprocess
import re
from pathlib import Path

def test_surface_bridge():
    """Test the Surface Bridge (improved_bridge.py)"""
    print("\n=== Testing Surface Bridge ===")
    
    bridge_path = Path("D:/AIArm/WebInterface/improved_bridge.py")
    
    if not bridge_path.exists():
        print(f"ERROR: Surface Bridge file not found at {bridge_path}")
        return False
    
    test_input = json.dumps({
        "input": "This is a test message for the Surface Bridge",
        "agent": "orchestrator",
        "user_id": "test_user"
    })
    
    try:
        # Run the bridge process
        process = subprocess.Popen(
            [sys.executable, str(bridge_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send input and get output
        stdout, stderr = process.communicate(input=test_input, timeout=10)
        
        # Check for errors
        if stderr:
            print(f"Surface Bridge stderr output: {stderr}")
        
        # Print raw output for debugging
        print(f"Surface Bridge raw output (first 500 chars):\n{stdout[:500]}...")
        
        # Try to extract JSON from the output
        json_match = re.search(r'\{[\s\S]*\}', stdout)
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)
                print(f"Surface Bridge JSON output: {json.dumps(result, indent=2)}")
                
                # Check for success
                if result.get("success") is True:
                    print("✅ Surface Bridge is working correctly")
                    return True
                else:
                    print("❌ Surface Bridge returned an error")
                    return False
            except json.JSONDecodeError as e:
                print(f"❌ Extracted JSON is invalid: {e}")
                return False
        else:
            print("❌ Could not find JSON object in Surface Bridge output")
            return False
    
    except Exception as e:
        print(f"❌ Error testing Surface Bridge: {e}")
        return False

def test_deep_bridge():
    """Test the Deep Bridge (ollama_bridge.py)"""
    print("\n=== Testing Deep Bridge ===")
    
    bridge_path = Path("D:/AIArm/WebInterface/ollama_bridge.py")
    
    if not bridge_path.exists():
        print(f"ERROR: Deep Bridge file not found at {bridge_path}")
        return False
    
    try:
        # Run the bridge process
        process = subprocess.Popen(
            [sys.executable, str(bridge_path), "--input", "This is a test message for the Deep Bridge"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Get output
        stdout, stderr = process.communicate(timeout=15)
        
        # Check for errors
        if stderr:
            print(f"Deep Bridge stderr output: {stderr}")
        
        # Print raw output for debugging
        print(f"Deep Bridge raw output (first 500 chars):\n{stdout[:500]}...")
        
        # Try to extract JSON from the output
        json_match = re.search(r'\{[\s\S]*\}', stdout)
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)
                print(f"Deep Bridge JSON output: {json.dumps(result, indent=2)}")
                
                # Check for success
                if result.get("success") is True:
                    print("✅ Deep Bridge is working correctly")
                    return True
                else:
                    print("❌ Deep Bridge returned an error")
                    return False
            except json.JSONDecodeError as e:
                print(f"❌ Extracted JSON is invalid: {e}")
                return False
        else:
            print("❌ Could not find JSON object in Deep Bridge output")
            return False
    
    except Exception as e:
        print(f"❌ Error testing Deep Bridge: {e}")
        return False

def main():
    """Main function"""
    print("=== Bridge Test Script ===")
    
    # Test Surface Bridge
    surface_bridge_ok = test_surface_bridge()
    
    # Test Deep Bridge
    deep_bridge_ok = test_deep_bridge()
    
    # Report overall status
    print("\n=== Test Results ===")
    print(f"Surface Bridge: {'✅ OK' if surface_bridge_ok else '❌ Failed'}")
    print(f"Deep Bridge: {'✅ OK' if deep_bridge_ok else '❌ Failed'}")
    
    if surface_bridge_ok and deep_bridge_ok:
        print("\n✅ All bridges are working correctly")
        return 0
    else:
        print("\n❌ One or more bridges are not working correctly")
        return 1

if __name__ == "__main__":
    sys.exit(main())
