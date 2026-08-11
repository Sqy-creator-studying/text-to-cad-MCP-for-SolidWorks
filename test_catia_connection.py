#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test CATIA MCP Connection - verify CATIA is running and accessible."""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")

def test_catia_connection():
    """Test connection to CATIA."""

    print("=" * 60)
    print("CATIA MCP Connection Test")
    print("=" * 60)

    # Step 1: Check if pywin32 is installed
    print("\n[1/4] Checking pywin32 installation...")
    try:
        import win32com.client
        print("  [OK] pywin32 is installed")
    except ImportError:
        print("  [FAIL] pywin32 is NOT installed")
        print("\n  Install it with: pip install pywin32")
        return False

    # Step 2: Try to connect to CATIA
    print("\n[2/4] Connecting to CATIA...")
    try:
        catia = win32com.client.Dispatch("CATIA.Application")
        print("  [OK] Connected to CATIA")
    except Exception as e:
        print(f"  [FAIL] Cannot connect to CATIA")
        print(f"\n  Error: {e}")
        print("\n  Make sure:")
        print("    - CATIA is RUNNING (open the application)")
        print("    - Try running this script as Administrator")
        print("    - Check if CATIA COM automation is enabled")
        return False

    # Step 3: Get CATIA version info
    print("\n[3/4] Getting CATIA information...")
    try:
        catia.Visible = True
        version = catia.SystemConfiguration.Version
        build = catia.SystemConfiguration.Build
        print(f"  [OK] CATIA Version: {version}")
        print(f"  [OK] Build: {build}")
    except Exception as e:
        print(f"  [WARN] Cannot get version info: {e}")

    # Step 4: Check active document
    print("\n[4/4] Checking active document...")
    try:
        doc = catia.ActiveDocument
        if doc:
            print(f"  [OK] Active document: {doc.Name}")
        else:
            print("  [WARN] No active document (will create one when needed)")
    except Exception:
        print("  [WARN] No active document (will create one when needed)")

    # Summary
    print("\n" + "=" * 60)
    print("[SUCCESS] CATIA MCP Connection Test PASSED")
    print("=" * 60)
    print("\nYour CATIA MCP server is ready to use!")
    print("\nNext steps:")
    print("  1. Make sure MCP server is configured in Claude")
    print("  2. Keep CATIA running")
    print("  3. Ask Claude to create CAD models")
    print("\nExample: 'Create a cylinder with 50mm diameter and 100mm height'")

    return True


if __name__ == "__main__":
    try:
        success = test_catia_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
