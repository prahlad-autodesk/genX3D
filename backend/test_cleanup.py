#!/usr/bin/env python3
"""
Test script for the temp models cleanup functionality
"""

import time
import os
from pathlib import Path
from langgraph_app import CADModelGenerator, TempModelsCleanupService

def test_cleanup_service():
    """Test the cleanup service functionality"""
    print("🧪 Testing cleanup service...")
    
    # Create a test temp directory
    test_temp_dir = Path("test_temp_models")
    test_temp_dir.mkdir(exist_ok=True)
    
    # Initialize cleanup service with 1 minute interval for testing
    cleanup_service = TempModelsCleanupService(test_temp_dir, cleanup_interval_minutes=1)
    
    # Create some test files
    test_files = []
    for i in range(3):
        test_file = test_temp_dir / f"test_model_{i}.step"
        test_file.write_text(f"Test content {i}")
        test_files.append(test_file)
        print(f"📝 Created test file: {test_file.name}")
    
    # Start cleanup service
    cleanup_service.start_cleanup_service()
    
    # Wait for cleanup to happen
    print("⏰ Waiting for cleanup (1 minute)...")
    time.sleep(70)  # Wait 70 seconds for cleanup
    
    # Check which files remain
    remaining_files = list(test_temp_dir.glob("*.step"))
    print(f"📊 Remaining files after cleanup: {len(remaining_files)}")
    for file in remaining_files:
        print(f"   - {file.name}")
    
    # Stop cleanup service
    cleanup_service.stop_cleanup_service()
    
    # Clean up test directory
    for file in test_files:
        if file.exists():
            file.unlink()
    test_temp_dir.rmdir()
    
    print("✅ Cleanup service test completed")

def test_cad_generator_cleanup():
    """Test the CAD generator with cleanup integration"""
    print("🧪 Testing CAD generator cleanup integration...")
    
    try:
        # Initialize CAD generator
        cad_gen = CADModelGenerator()
        
        # Get initial stats
        initial_stats = cad_gen.get_cleanup_stats()
        print(f"📊 Initial cleanup stats: {initial_stats}")
        
        # Test manual cleanup
        cleanup_stats = cad_gen.manual_cleanup()
        print(f"📊 Manual cleanup stats: {cleanup_stats}")
        
        print("✅ CAD generator cleanup integration test completed")
        
    except Exception as e:
        print(f"❌ Error testing CAD generator cleanup: {e}")

def main():
    """Main function for running cleanup tests"""
    print("🚀 Starting cleanup functionality tests...")
    
    # Test 1: Basic cleanup service
    test_cleanup_service()
    
    # Test 2: CAD generator integration
    test_cad_generator_cleanup()
    
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main() 