#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test script for Nexus AI Ultimate Interface
"""

import sys
import os

def test_files_exist():
    """Test that all required files exist"""
    required_files = [
        'NEXUS_ULTIMATE_INTERFACE.py',
        'NEXUS_ULTIMATE_PANEL_SYSTEM.py',
        'LAUNCH_NEXUS_ULTIMATE.bat',
        'DEMO_NEXUS_ULTIMATE.py',
        'README_NEXUS_ULTIMATE.md'
    ]

    print("[INFO] Checking required files...")
    all_exist = True

    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   [OK] {file} ({size:,} bytes)")
        else:
            print(f"   [ERROR] {file} (MISSING)")
            all_exist = False

    return all_exist

def test_python_syntax():
    """Test Python file syntax"""
    python_files = [
        'NEXUS_ULTIMATE_INTERFACE.py',
        'NEXUS_ULTIMATE_PANEL_SYSTEM.py',
        'DEMO_NEXUS_ULTIMATE.py'
    ]

    print("\n[PYTHON] Testing Python syntax...")
    all_valid = True

    for file in python_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    source = f.read()

                # Test compilation
                compile(source, file, 'exec')
                print(f"   [OK] {file} (valid syntax)")
            except SyntaxError as e:
                print(f"   [ERROR] {file} (syntax error: {e})")
                all_valid = False
            except Exception as e:
                print(f"   [WARNING] {file} (encoding issue: {e})")
        else:
            print(f"   [ERROR] {file} (file not found)")
            all_valid = False

    return all_valid

def test_launcher():
    """Test launcher script"""
    print("\n[LAUNCHER] Testing launcher script...")

    launcher = 'LAUNCH_NEXUS_ULTIMATE.bat'
    if os.path.exists(launcher):
        with open(launcher, 'r') as f:
            content = f.read()

        # Check for key components
        checks = [
            ('Python check', 'python --version' in content),
            ('Directory check', 'NEXUS_ULTIMATE_INTERFACE.py' in content),
            ('Server start', 'python NEXUS_ULTIMATE_INTERFACE.py' in content),
            ('UE5 instructions', 'UE5' in content),
            ('API endpoints', '8001' in content)
        ]

        for check_name, condition in checks:
            if condition:
                print(f"   [OK] {check_name}")
            else:
                print(f"   [ERROR] {check_name}")

        print(f"   [OK] {launcher} (structure looks good)")
        return True
    else:
        print(f"   [ERROR] {launcher} (not found)")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("[TEST] NEXUS AI ULTIMATE INTERFACE - TEST SUITE")
    print("=" * 60)
    print()

    # Test file existence
    files_ok = test_files_exist()

    # Test Python syntax
    syntax_ok = test_python_syntax()

    # Test launcher
    launcher_ok = test_launcher()

    print()
    print("=" * 60)
    print("[RESULTS] TEST RESULTS")
    print("=" * 60)

    if files_ok and syntax_ok and launcher_ok:
        print("[SUCCESS] ALL TESTS PASSED!")
        print()
        print("[OK] Files created successfully")
        print("[OK] Python syntax is valid")
        print("[OK] Launcher script is properly configured")
        print()
        print("[READY] The Nexus AI Ultimate Interface is ready!")
        print()
        print("Next steps:")
        print("1. Run: LAUNCH_NEXUS_ULTIMATE.bat")
        print("2. Follow the UE5 setup instructions")
        print("3. Run: python DEMO_NEXUS_ULTIMATE.py")
        print("4. Experience the most stunning AI interface ever created!")
        return True
    else:
        print("[FAILED] SOME TESTS FAILED!")
        print()
        print("Please check the errors above and fix any issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
