#!/usr/bin/env python3
"""
Test script to verify CadQuery is working with real STEP file generation
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app import RAGService, CADModelGenerator

def test_cadquery_generation():
    """Test real CadQuery code generation"""
    print("🧪 Testing real CadQuery generation...")
    
    # Test the RAG service
    rag_service = RAGService()
    print("✅ RAG service initialized")
    
    # Test the CAD model generator
    cad_generator = CADModelGenerator()
    print("✅ CAD model generator initialized")
    
    # Test with a simple query
    test_query = "create a cuboid"
    print(f"🔍 Testing query: '{test_query}'")
    
    try:
        result = cad_generator.generate_model(test_query)
        print("✅ Model generation successful!")
        print(f"Result: {result}")
        
        # Check if the STEP file was actually created
        if 'model_url' in result:
            model_path = result['model_url'].replace('/temp_models/', 'temp_models/')
            if Path(model_path).exists():
                file_size = Path(model_path).stat().st_size
                print(f"✅ STEP file created: {model_path} (size: {file_size} bytes)")
                return True
            else:
                print(f"❌ STEP file not found: {model_path}")
                return False
        else:
            print("❌ No model_url in result")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_cadquery_generation()
    if success:
        print("\n🎉 All tests passed! CadQuery is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the setup.")
        sys.exit(1) 