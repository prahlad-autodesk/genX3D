#!/usr/bin/env python3
"""
Test script for the RAG-assisted code generation in GenX3D
This script tests how the system uses RAG examples to improve code generation.
"""

import asyncio
import json
import sys
import os

# Add backend to path
sys.path.append('backend')

# Test queries that should benefit from RAG examples
rag_test_queries = [
    # Queries that should find good RAG examples
    "Write CADQuery code for a cylinder",
    "Generate code to create a cube",
    "Create CADQuery code for a sphere",
    "Write code to make a simple box",
    
    # Queries that might find partial matches
    "Write CADQuery code for a gear",
    "Generate code to create a bracket",
    "Create CADQuery code for a custom part",
    "Write code to make a complex shape",
    
    # Queries that might not find good examples
    "Write CADQuery code for a spiral staircase",
    "Generate code to create a parametric assembly",
    "Create CADQuery code for a custom mechanical part",
    "Write code to make a unique design"
]

async def test_rag_assisted_generation():
    """Test the RAG-assisted code generation with various queries"""
    print("🧪 Testing GenX3D RAG-Assisted Code Generation")
    print("=" * 60)
    
    try:
        from langgraph_app import run_graph
    except ImportError as e:
        print(f"❌ Error importing langgraph_app: {e}")
        print("Make sure you're in the project root directory")
        return
    
    results = []
    
    for query in rag_test_queries:
        print(f"\n🔍 Testing RAG-assisted generation: '{query}'")
        
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
                        attempts = parsed_result.get('attempts', 1)
                        method = parsed_result.get('method', 'unknown')
                        examples_count = parsed_result.get('examples_count', 0)
                        rag_examples = parsed_result.get('rag_examples_used', [])
                        
                        print(f"✅ Success after {attempts} attempt(s)!")
                        print(f"   Method: {method}")
                        print(f"   RAG examples used: {examples_count}")
                        print(f"   Model ID: {parsed_result.get('model_id', 'unknown')}")
                        print(f"   Code length: {len(parsed_result['generated_code'])} characters")
                        
                        # Show RAG examples info
                        if rag_examples:
                            print(f"   RAG examples:")
                            for i, example in enumerate(rag_examples, 1):
                                prompt = example.get('prompt', 'Unknown')
                                score = example.get('similarity_score', 0)
                                print(f"     {i}. '{prompt}' (similarity: {score:.3f})")
                        
                        results.append({
                            "query": query,
                            "status": "success",
                            "attempts": attempts,
                            "method": method,
                            "examples_count": examples_count,
                            "model_id": parsed_result.get('model_id'),
                            "code_length": len(parsed_result['generated_code']),
                            "rag_examples": rag_examples
                        })
                    elif "error" in parsed_result:
                        attempts = parsed_result.get('attempts', 0)
                        rag_examples = parsed_result.get('rag_examples_attempted', [])
                        print(f"❌ Failed after {attempts} attempt(s): {parsed_result['error']}")
                        
                        if rag_examples:
                            print(f"   RAG examples attempted:")
                            for i, example in enumerate(rag_examples, 1):
                                prompt = example.get('prompt', 'Unknown')
                                score = example.get('similarity_score', 0)
                                print(f"     {i}. '{prompt}' (similarity: {score:.3f})")
                        
                        results.append({
                            "query": query,
                            "status": "failed",
                            "attempts": attempts,
                            "error": parsed_result['error'],
                            "last_error": parsed_result.get('last_error', 'Unknown'),
                            "rag_examples": rag_examples
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
    print("\n" + "=" * 60)
    print("📊 RAG-ASSISTED GENERATION TEST SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    total = len(results)
    
    print(f"Total tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/total)*100:.1f}%")
    
    # Analyze RAG usage
    if successful > 0:
        successful_tests = [r for r in results if r["status"] == "success"]
        
        # RAG usage statistics
        total_examples_used = sum(r["examples_count"] for r in successful_tests)
        avg_examples_per_query = total_examples_used / len(successful_tests)
        queries_with_examples = sum(1 for r in successful_tests if r["examples_count"] > 0)
        
        print(f"\n📈 RAG Usage Analysis:")
        print(f"   Queries with RAG examples: {queries_with_examples}/{successful}")
        print(f"   Average examples per query: {avg_examples_per_query:.1f}")
        print(f"   Total examples used: {total_examples_used}")
        
        # Method distribution
        method_dist = {}
        for r in successful_tests:
            method = r["method"]
            method_dist[method] = method_dist.get(method, 0) + 1
        
        print(f"   Method distribution:")
        for method, count in method_dist.items():
            print(f"     {method}: {count} case(s)")
    
    # Show successful cases with RAG info
    if successful > 0:
        print(f"\n✅ Successful generations:")
        for test in [r for r in results if r["status"] == "success"]:
            examples_info = f"{test['examples_count']} RAG examples" if test['examples_count'] > 0 else "no RAG examples"
            print(f"  - '{test['query']}' → {test['attempts']} attempt(s), {examples_info}, Model: {test['model_id']}")
    
    # Show failed cases
    if failed > 0:
        print(f"\n❌ Failed cases:")
        for test in [r for r in results if r["status"] == "failed"]:
            examples_info = f"{len(test['rag_examples'])} RAG examples" if test.get('rag_examples') else "no RAG examples"
            print(f"  - '{test['query']}' → {test['attempts']} attempt(s), {examples_info}, Error: {test['last_error'][:50]}...")

def test_specific_rag_generation():
    """Test RAG-assisted generation with a specific query"""
    print("\n🎯 Interactive RAG-Assisted Generation Test")
    print("=" * 45)
    
    query = input("Enter a query for RAG-assisted code generation: ").strip()
    
    if not query:
        print("❌ No query provided")
        return
    
    print(f"\nTesting RAG-assisted generation: '{query}'")
    
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
    print("🤖 GenX3D RAG-Assisted Generation Test")
    print("=" * 40)
    print("1. Run all RAG-assisted generation tests")
    print("2. Test specific RAG-assisted query")
    print("3. Exit")
    
    choice = input("\nChoose an option (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(test_rag_assisted_generation())
    elif choice == "2":
        test_specific_rag_generation()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 