#!/usr/bin/env python3
"""
Test script for the improved routing logic in GenX3D
This script tests different types of user queries to see how the router responds.
"""

import asyncio
import json
import sys
import os

# Add backend to path
sys.path.append('backend')

# Test queries with expected routing
test_queries = [
    # Generation queries (RAG-based)
    ("Create a cylinder", "generate"),
    ("Make me a cube", "generate"),
    ("Design a gear with 20 teeth", "generate"),
    ("Build a bracket for mounting", "generate"),
    ("Generate a sphere", "generate"),
    ("Model a simple box", "generate"),
    
    # Code generation queries
    ("Write CADQuery code for a spiral staircase", "code_gen"),
    ("Generate code to create a custom part", "code_gen"),
    ("Create CADQuery code for a complex assembly", "code_gen"),
    ("Write a script to make a parametric gear", "code_gen"),
    ("Generate custom code for a bracket", "code_gen"),
    ("Create a program for a 3D model", "code_gen"),
    
    # Help queries
    ("What is parametric modeling?", "help"),
    ("How do I create a cylinder?", "help"),
    ("Explain the difference between STL and STEP files", "help"),
    ("Help me understand CAD concepts", "help"),
    ("What are the best practices for 3D modeling?", "help"),
    ("How to export models?", "help"),
    
    # Edge cases
    ("Hello", "help"),  # Default to help for greetings
    ("Thanks", "help"),  # Default to help for acknowledgments
    ("", "help"),  # Empty message
]

async def test_routing():
    """Test the routing logic with various queries"""
    print("🧪 Testing GenX3D Routing Logic")
    print("=" * 50)
    
    try:
        from langgraph_app import run_graph
    except ImportError as e:
        print(f"❌ Error importing langgraph_app: {e}")
        print("Make sure you're in the project root directory")
        return
    
    results = []
    
    for query, expected_route in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print(f"Expected route: {expected_route}")
        
        try:
            # Run the graph
            result = await run_graph({"message": query})
            
            # Parse the result
            if isinstance(result, dict) and "route" in result:
                actual_route = result["route"]
                success = actual_route == expected_route
                
                print(f"Actual route: {actual_route}")
                print(f"Status: {'✅ PASS' if success else '❌ FAIL'}")
                
                results.append({
                    "query": query,
                    "expected": expected_route,
                    "actual": actual_route,
                    "success": success
                })
            else:
                print(f"❌ Unexpected result format: {result}")
                results.append({
                    "query": query,
                    "expected": expected_route,
                    "actual": "error",
                    "success": False
                })
                
        except Exception as e:
            print(f"❌ Error testing query: {e}")
            results.append({
                "query": query,
                "expected": expected_route,
                "actual": "error",
                "success": False
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ROUTING TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    # Show failed tests
    failed_tests = [r for r in results if not r["success"]]
    if failed_tests:
        print(f"\n❌ Failed tests:")
        for test in failed_tests:
            print(f"  - '{test['query']}' → Expected: {test['expected']}, Got: {test['actual']}")
    
    # Show passed tests
    passed_tests = [r for r in results if r["success"]]
    if passed_tests:
        print(f"\n✅ Passed tests:")
        for test in passed_tests:
            print(f"  - '{test['query']}' → {test['actual']}")

def test_specific_query():
    """Test a specific query interactively"""
    print("\n🎯 Interactive Query Test")
    print("=" * 30)
    
    query = input("Enter a query to test routing: ").strip()
    
    if not query:
        print("❌ No query provided")
        return
    
    print(f"\nTesting: '{query}'")
    
    try:
        from langgraph_app import run_graph
        
        async def run_test():
            result = await run_graph({"message": query})
            print(f"Result: {json.dumps(result, indent=2)}")
        
        asyncio.run(run_test())
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🤖 GenX3D Routing Test")
    print("=" * 30)
    print("1. Run all routing tests")
    print("2. Test specific query")
    print("3. Exit")
    
    choice = input("\nChoose an option (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(test_routing())
    elif choice == "2":
        test_specific_query()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 