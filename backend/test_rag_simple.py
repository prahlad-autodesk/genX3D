#!/usr/bin/env python3
"""
Simple test script for RAG service and CAD model generator
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from langgraph_app import RAGService, CADModelGenerator

def test_rag_service():
    """Test the RAG service"""
    print("🧪 Testing RAG Service")
    print("=" * 30)
    
    rag_service = RAGService()
    
    test_queries = [
        "create a cuboid",
        "make a cylinder", 
        "generate a sphere"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        try:
            matches = rag_service.retrieve_code(query, top_k=2)
            print(f"Found {len(matches)} matches")
            
            for i, match in enumerate(matches):
                print(f"  Match {i+1}:")
                print(f"    Score: {match['score']:.3f}")
                print(f"    Prompt: {match['metadata'].get('prompt', 'N/A')[:100]}...")
                print(f"    Code length: {len(match['metadata'].get('code', ''))} chars")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def test_cad_generator():
    """Test the CAD model generator"""
    print("\n\n🔧 Testing CAD Model Generator")
    print("=" * 40)
    
    cad_generator = CADModelGenerator()
    
    test_queries = [
        "create a cuboid",
        "make a cylinder"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        try:
            result = cad_generator.generate_model(query)
            print(f"Result: {result}")
            
            if 'model_url' in result:
                print(f"✅ Model generated: {result['model_url']}")
            elif 'error' in result:
                print(f"❌ Error: {result['error']}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    # Test RAG service first
    test_rag_service()
    
    # Test CAD generator
    test_cad_generator() 