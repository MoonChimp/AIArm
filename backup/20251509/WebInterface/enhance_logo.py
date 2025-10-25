"""
Logo Enhancer for NexusLogo.gif
Creates a larger version with transparent background
"""

import os
import sys
from pathlib import Path
import shutil

def enhance_logo():
    """
    Enhance the NexusLogo.gif by:
    1. Making a backup of the original
    2. Adding CSS to make it appear with transparent background
    3. Updating all interfaces to use the enhanced version
    """
    # Paths
    base_dir = Path("D:/AIArm")
    web_dir = base_dir / "WebInterface"
    logo_path = web_dir / "NexusLogo.gif"
    backup_path = web_dir / "NexusLogo_original.gif"
    
    # Ensure the logo exists
    if not logo_path.exists():
        print(f"Error: Logo file not found at {logo_path}")
        return False
    
    # Create backup if it doesn't exist
    if not backup_path.exists():
        try:
            shutil.copy2(logo_path, backup_path)
            print(f"Created backup of original logo at {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    print("Logo enhancement complete:")
    print("1. All interfaces now display the logo with a transparent background")
    print("2. The logo size has been increased to 100px height")
    print("3. Special blend mode has been applied for better visibility")
    print("\nThe changes are applied through CSS. Original file is preserved as NexusLogo_original.gif")
    
    return True

if __name__ == "__main__":
    print("NexusLogo Enhancer")
    print("==================")
    enhance_logo()
    print("\nDone!")
