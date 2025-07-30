#!/usr/bin/env python3
"""
Test script for the new code generation node in GenX3D
This script tests the LLM-based CADQuery code generation functionality.
"""

import asyncio
import json
import sys
import os

# Add backend to path
sys.path.append('backend')

# Test queries for code generation
code_gen_queries = [
    "Write CADQuery code for a simple cylinder",
    "Generate code to create a cube with rounded corners",
    "Create CADQuery code for a gear with 20 teeth",
    "Write a script to make a spiral staircase",
    "Generate custom code for a bracket with holes",
    "Create CADQuery code for a parametric box"
]

async def test_code_generation():
    """Test the code generation node with various queries"""
    print("🧪 Testing GenX3D Code Generation Node")
    print("=" * 50)
    
    try:
        from langgraph_app import run_graph
    except ImportError as e:
        print(f"❌ Error importing langgraph_app: {e}")
        print("Make sure you're in the project root directory")
        return
    
    results = []
    
    for query in code_gen_queries:
        print(f"\n🔍 Testing code generation: '{query}'")
        
        try:
            # Run the graph
            result = await run_graph({"message": query})
            
            # Parse the result
            if isinstance(result, dict) and "result" in result:
                result_data = result["result"]
                
                # Try to parse JSON result
                try:
                    if isinstance(result_data, str):
                        parsed_result = json.loads(result_data)
                    else:
                        parsed_result = result_data
                    
                    # Check if it's a successful code generation
                    if "generated_code" in parsed_result:
                        print(f"✅ Code generation successful!")
                        print(f"   Model ID: {parsed_result.get('model_id', 'unknown')}")
                        print(f"   Method: {parsed_result.get('method', 'unknown')}")
                        print(f"   Code length: {len(parsed_result['generated_code'])} characters")
                        
                        # Show first few lines of generated code
                        code_lines = parsed_result['generated_code'].split('\n')[:5]
                        print(f"   Code preview:")
                        for line in code_lines:
                            print(f"     {line}")
                        if len(parsed_result['generated_code'].split('\n')) > 5:
                            print(f"     ... ({len(parsed_result['generated_code'].split('\n')) - 5} more lines)")
                        
                        results.append({
                            "query": query,
                            "status": "success",
                            "model_id": parsed_result.get('model_id'),
                            "code_length": len(parsed_result['generated_code'])
                        })
                    elif "error" in parsed_result:
                        print(f"❌ Error: {parsed_result['error']}")
                        results.append({
                            "query": query,
                            "status": "error",
                            "error": parsed_result['error']
                        })
                    else:
                        print(f"⚠️ Unexpected result format")
                        results.append({
                            "query": query,
                            "status": "unexpected",
                            "result": parsed_result
                        })
                        
                except json.JSONDecodeError:
                    print(f"⚠️ Result is not JSON: {result_data}")
                    results.append({
                        "query": query,
                        "status": "json_error",
                        "result": result_data
                    })
            else:
                print(f"❌ Unexpected result format: {result}")
                results.append({
                    "query": query,
                    "status": "format_error",
                    "result": result
                })
                
        except Exception as e:
            print(f"❌ Error testing query: {e}")
            results.append({
                "query": query,
                "status": "exception",
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CODE GENERATION TEST SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for r in results if r["status"] == "success")
    total = len(results)
    
    print(f"Total tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success rate: {(successful/total)*100:.1f}%")
    
    # Show successful generations
    successful_tests = [r for r in results if r["status"] == "success"]
    if successful_tests:
        print(f"\n✅ Successful code generations:")
        for test in successful_tests:
            print(f"  - '{test['query']}' → Model: {test['model_id']}, Code: {test['code_length']} chars")
    
    # Show failed tests
    failed_tests = [r for r in results if r["status"] != "success"]
    if failed_tests:
        print(f"\n❌ Failed tests:")
        for test in failed_tests:
            print(f"  - '{test['query']}' → {test['status']}: {test.get('error', 'Unknown error')}")

def test_specific_code_generation():
    """Test a specific code generation query interactively"""
    print("\n🎯 Interactive Code Generation Test")
    print("=" * 40)
    
    query = input("Enter a query for code generation: ").strip()
    
    if not query:
        print("❌ No query provided")
        return
    
    print(f"\nTesting code generation: '{query}'")
    
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
    print("🤖 GenX3D Code Generation Test")
    print("=" * 35)
    print("1. Run all code generation tests")
    print("2. Test specific code generation query")
    print("3. Exit")
    
    choice = input("\nChoose an option (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(test_code_generation())
    elif choice == "2":
        test_specific_code_generation()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 