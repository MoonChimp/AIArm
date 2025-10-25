#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copy Nexus Logo to WebInterface directory
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    """Main function"""
    source_path = Path("D:/AIArm/NexusLogo.gif")
    target_path = Path("D:/AIArm/WebInterface/NexusLogo.gif")
    
    # Check if source file exists
    if not source_path.exists():
        print(f"Error: Source file {source_path} does not exist!")
        return 1
    
    # Copy the file
    try:
        shutil.copy2(source_path, target_path)
        print(f"Successfully copied {source_path} to {target_path}")
        return 0
    except Exception as e:
        print(f"Error copying file: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
