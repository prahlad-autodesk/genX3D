#!/usr/bin/env python3
"""
Test script for core imports - focuses on the essential functionality
that needs to work for the langgraph_app import to succeed
"""

import sys
import os

print("=== Core Imports Test ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

try:
    print("\n=== Testing core imports ===")
    
    # Test basic imports
    from typing import TypedDict, Literal, Union
    print("✅ typing imports successful")
    
    # Test LangChain imports
    from langchain_openai import ChatOpenAI
    print("✅ langchain_openai import successful")
    
    from langchain_core.messages import HumanMessage
    print("✅ langchain_core.messages import successful")
    
    # Test LangGraph imports
    from langgraph.graph import StateGraph, END
    print("✅ langgraph.graph import successful")
    
    # Test RAG imports
    from sentence_transformers import SentenceTransformer
    print("✅ sentence_transformers import successful")
    
    import pinecone
    print("✅ pinecone import successful")
    
    import faiss
    print("✅ faiss import successful")
    
    # Test the critical import that was failing
    print("\n=== Testing graph module import ===")
    from graph.langgraph_app import run_graph, cad_generator
    print("✅ graph.langgraph_app import successful")
    
    # Test FastAPI
    from fastapi import FastAPI
    print("✅ FastAPI import successful")
    
    print("\n=== Core functionality test successful! ===")
    print("✅ Docker container should work with these core imports")
    
    # Test CadQuery if available (but don't fail if it's not)
    try:
        import cadquery as cq
        from cadquery import Workplane
        print("✅ cadquery import successful")
        
        # Test basic CadQuery functionality
        wp = cq.Workplane("XY")
        print("✅ CadQuery Workplane creation successful")
        
    except ImportError as e:
        print(f"⚠️ CadQuery not available: {e}")
        print("💡 This is acceptable for core functionality")
    except Exception as e:
        print(f"⚠️ CadQuery error (non-critical): {e}")
        print("💡 Core functionality should still work")
    
    print("\n=== All core tests passed! ===")
    print("✅ The langgraph_app import issue should be resolved")
    
except ImportError as e:
    print(f"❌ Core import error: {e}")
    print(f"💡 This indicates a missing dependency in the Docker container")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
