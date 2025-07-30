#!/usr/bin/env python3
"""
Test script for RAG functionality and CAD model generation
"""

import asyncio
import json
from langgraph_app import run_graph

async def test_rag_generation():
    """Test the RAG-based CAD model generation"""
    
    # Test queries
    test_queries = [
        "create a cuboid",
        "make a cylinder",
        "generate a sphere",
        "create a simple cube"
    ]
    
    print("🧪 Testing RAG-based CAD Model Generation")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: '{query}'")
        print("-" * 30)
        
        try:
            # Run the graph
            result = await run_graph({"message": query})
            
            # Parse the result
            if isinstance(result.get("result"), str):
                try:
                    result_data = json.loads(result.get("result"))
                except json.JSONDecodeError:
                    result_data = {"text": result.get("result")}
            else:
                result_data = result.get("result", {})
            
            # Display results
            print(f"Route: {result.get('route', 'N/A')}")
            print(f"Response: {result_data.get('text', 'N/A')}")
            
            if 'model_url' in result_data:
                print(f"Model URL: {result_data['model_url']}")
                print(f"Model Type: {result_data.get('model_type', 'N/A')}")
                print(f"Similarity Score: {result_data.get('similarity_score', 'N/A')}")
            
            if 'error' in result_data:
                print(f"❌ Error: {result_data['error']}")
            else:
                print("✅ Success!")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_rag_generation()) 