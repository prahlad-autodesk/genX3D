#!/usr/bin/env python3
"""
Debug script to test CadQuery code execution step by step
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app import RAGService, CADModelGenerator
import cadquery as cq
from cadquery import Workplane

def test_simple_cadquery():
    """Test simple CadQuery code execution"""
    print("🧪 Testing simple CadQuery code...")
    
    try:
        # Test 1: Simple box creation
        print("Test 1: Creating a simple box...")
        result = cq.Workplane('XY').box(10, 5, 3)
        print(f"✅ Box created: {type(result)}")
        
        # Test 2: Export to STEP
        print("Test 2: Exporting to STEP...")
        step_file_path = "test_box.step"
        cq.exporters.export(result, step_file_path, exportType='STEP')
        
        if Path(step_file_path).exists():
            file_size = Path(step_file_path).stat().st_size
            print(f"✅ STEP file created: {step_file_path} (size: {file_size} bytes)")
            return True
        else:
            print(f"❌ STEP file not created: {step_file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error in simple CadQuery test: {e}")
        return False

def test_rag_code_execution():
    """Test RAG code execution"""
    print("\n🧪 Testing RAG code execution...")
    
    try:
        # Get RAG service
        rag_service = RAGService()
        
        # Test query
        query = "create a cuboid"
        matches = rag_service.retrieve_code(query, top_k=1)
        
        if matches:
            match = matches[0]
            code = match["metadata"].get("code", "")
            print(f"Retrieved code:\n{code}")
            
            # Test code execution
            print("\nExecuting retrieved code...")
            step_file_path = "test_rag.step"
            
            # Create execution environment
            local_vars = {
                'cq': cq,
                'Workplane': Workplane,
                'step_file_path': step_file_path
            }
            
            # Execute the code
            exec(code, {}, local_vars)
            
            # Add export statement if not present
            if 'solid' in local_vars:
                print("Adding export statement...")
                solid = local_vars['solid']
                cq.exporters.export(solid, step_file_path, exportType='STEP')
            
            if Path(step_file_path).exists():
                file_size = Path(step_file_path).stat().st_size
                print(f"✅ RAG STEP file created: {step_file_path} (size: {file_size} bytes)")
                return True
            else:
                print(f"❌ RAG STEP file not created: {step_file_path}")
                return False
        else:
            print("❌ No matches found in RAG")
            return False
            
    except Exception as e:
        print(f"❌ Error in RAG code execution: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Debugging CadQuery execution...")
    
    # Test 1: Simple CadQuery
    success1 = test_simple_cadquery()
    
    # Test 2: RAG code execution
    success2 = test_rag_code_execution()
    
    if success1 and success2:
        print("\n🎉 All debug tests passed!")
    else:
        print("\n❌ Some debug tests failed.")
        sys.exit(1) 