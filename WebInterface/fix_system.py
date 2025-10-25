#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus System Fix Script
Fixes the bridge parsing issues and response formatting
"""

import os
import sys
import re
import shutil
from pathlib import Path

def fix_concurrent_server():
    """Fix the concurrent_server.js file"""
    print("Fixing concurrent_server.js...")
    
    # Path to the file
    file_path = Path("D:/AIArm/WebInterface/concurrent_server.js")
    
    # Create a backup
    backup_path = file_path.with_suffix(".js.bak")
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")
    
    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix 1: The assignment to constant variable error
    content = content.replace("const BRIDGES", "let BRIDGES")
    
    # Fix 2: Update the spawn command to use the bridge wrapper
    content = content.replace(
        'const surfaceProcess = process.spawn("python", [surfaceBridgePath]',
        'const surfaceProcess = process.spawn("python", ["bridge_wrapper.py", surfaceBridgePath]'
    )
    content = content.replace(
        'const deepProcess = process.spawn("python", [deepBridgePath]',
        'const deepProcess = process.spawn("python", ["bridge_wrapper.py", deepBridgePath]'
    )
    
    # Fix 3: Make sure port is consistent
    port_pattern = r'const PORT = (\d+);'
    port_match = re.search(port_pattern, content)
    if port_match:
        content = content.replace(
            f'const PORT = {port_match.group(1)};',
            'const PORT = customPort || 45691;'
        )
    
    # Fix 4: Fix the JSON parsing
    content = content.replace(
        'try {\n          const surfaceResult = JSON.parse(surfaceOutput);',
        'try {\n          // Extract JSON from possibly mixed output\n          const jsonMatch = surfaceOutput.match(/\\{[\\s\\S]*\\}/); \n          const surfaceResult = jsonMatch ? JSON.parse(jsonMatch[0]) : null;'
    )
    
    content = content.replace(
        'try {\n          const deepResult = JSON.parse(deepOutput);',
        'try {\n          // Extract JSON from possibly mixed output\n          const jsonMatch = deepOutput.match(/\\{[\\s\\S]*\\}/); \n          const deepResult = jsonMatch ? JSON.parse(jsonMatch[0]) : null;'
    )
    
    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Fixed concurrent_server.js")
    return True

def fix_interface():
    """Fix the real_interface.html file"""
    print("Fixing real_interface.html...")
    
    # Path to the file
    file_path = Path("D:/AIArm/WebInterface/real_interface.html")
    
    # Create a backup
    backup_path = file_path.with_suffix(".html.bak")
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")
    
    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Add script to clean responses
    script = """
    <script>
    function cleanResponse(text) {
        // Remove repetitive prefix
        text = text.replace(/I've processed your request through the HRM architecture. The Surface layer provided structured understanding while the Deep reasoning layer added contextual depth. How else can I assist you\\?\\s*/g, "");
        
        // Remove orchestrator prefix
        text = text.replace(/Orchestrator \\(HRM\\)\\s*\\d{1,2}:\\d{1,2}:\\d{1,2} [AP]M\\s*/g, "");
        
        return text;
    }
    
    // Apply cleaning when a new message is added
    document.addEventListener("DOMNodeInserted", function(e) {
        if (e.target.classList && e.target.classList.contains("assistant-message")) {
            setTimeout(function() {
                e.target.innerHTML = cleanResponse(e.target.innerHTML);
            }, 100);
        }
    });
    </script>
    """
    
    # Add the script to the head section
    if "</head>" in content:
        content = content.replace("</head>", script + "</head>")
    else:
        content = content.replace("<body>", script + "<body>")
    
    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Fixed real_interface.html")
    return True

def create_startup_script():
    """Create a fixed startup script"""
    print("Creating fixed startup script...")
    
    script_path = Path("D:/AIArm/WebInterface/start_nexus_fixed_v2.bat")
    
    # Create the script
    with open(script_path, "w") as f:
        f.write("""@echo off
echo ===================================================================== 
echo NEXUS HRM ARCHITECTURE SYSTEM - FIXED VERSION
echo ===================================================================== 

REM Check if Ollama is running
echo Checking Ollama availability...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama is not running! Please start Ollama before running this script.
    echo Visit http://localhost:11434 to verify Ollama is running.
    pause
    exit /b 1
)
echo [SUCCESS] Ollama is running

REM Try to stop any running bridges
echo Cleaning up any running processes...
taskkill /f /im python.exe 2>nul

echo Starting Nexus HRM system on port 45691...
cd "D:\\AIArm\\WebInterface"
echo The system will be available at http://localhost:45691
node concurrent_server.js --port 45691

pause
""")
    
    print(f"Created startup script: {script_path}")
    return True

def main():
    """Main function"""
    print("===================================================================== ")
    print("NEXUS HRM ARCHITECTURE SYSTEM - FIX SCRIPT")
    print("===================================================================== ")
    
    # Fix the concurrent_server.js file
    fix_concurrent_server()
    
    # Fix the real_interface.html file
    fix_interface()
    
    # Create a fixed startup script
    create_startup_script()
    
    print("\n===================================================================== ")
    print("NEXUS HRM ARCHITECTURE SYSTEM FIX COMPLETE")
    print("===================================================================== ")
    print("The system has been fixed. Please:")
    print("1. Stop any running instances of Nexus")
    print("2. Start the fixed system using:")
    print("   D:\\AIArm\\WebInterface\\start_nexus_fixed_v2.bat")
    print("\nThe system will run on port 45691 to avoid any conflicts.")
    print("\nFixed issues:")
    print("1. Bridge output parsing errors")
    print("2. Port consistency")
    print("3. Repetitive prefix in responses")
    print("4. Assignment to constant variable error")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
