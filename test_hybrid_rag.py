#!/usr/bin/env python3
"""
Test script for the hybrid RAG system (Local FAISS + Pinecone)
"""

import sys
import os
sys.path.append('backend')

from langgraph_app import HybridRAGService

def test_hybrid_rag():
    """Test the hybrid RAG system"""
    print("🧪 Testing Hybrid RAG System...")
    
    # Initialize the hybrid RAG service
    rag_service = HybridRAGService()
    
    # Test queries
    test_queries = [
        "generate a sphere",
        "create a cylinder", 
        "make a cube",
        "design a gear",
        "build a bracket"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        print("-" * 50)
        
        # Test hybrid retrieval
        results = rag_service.retrieve_code(query, top_k=3, use_hybrid=True)
        
        print(f"📊 Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            source = result.get("source", "unknown")
            score = result.get("score", 0)
            prompt = result.get("metadata", {}).get("prompt", "No prompt")
            code = result.get("metadata", {}).get("code", "No code")
            
            print(f"\n{i}. Source: {source} (Score: {score:.3f})")
            print(f"   Prompt: {prompt}")
            print(f"   Code: {code[:100]}...")
    
    print("\n✅ Hybrid RAG test completed!")

if __name__ == "__main__":
    test_hybrid_rag() 