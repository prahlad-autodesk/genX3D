#!/usr/bin/env python3
"""
Test script to verify mamba-based CadQuery installation
"""

import sys
import os

print("=== Mamba CadQuery Test ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

try:
    print("\n=== Testing CadQuery imports ===")
    
    # Test CadQuery import
    import cadquery as cq
    from cadquery import Workplane
    print("✅ cadquery import successful")
    
    # Test OCP import (should be included with CadQuery)
    import OCP
    print("✅ OCP import successful")
    
    # Test basic CadQuery functionality
    wp = cq.Workplane("XY")
    print("✅ CadQuery Workplane creation successful")
    
    # Test creating a simple shape
    cube = wp.box(10, 10, 10)
    print("✅ CadQuery shape creation successful")
    
    print("\n=== CadQuery installation successful! ===")
    print("✅ Mamba-based CadQuery installation is working correctly")
    
except ImportError as e:
    print(f"❌ CadQuery import error: {e}")
    print(f"💡 This indicates CadQuery/OCP needs to be installed")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected CadQuery error: {e}")
    sys.exit(1)
