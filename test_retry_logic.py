#!/usr/bin/env python3
"""
Test script for the retry logic in GenX3D code generation
This script tests how the system handles code generation failures and retries.
"""

import asyncio
import json
import sys
import os

# Add backend to path
sys.path.append('backend')

# Test queries that might cause issues (to test retry logic)
retry_test_queries = [
    # Simple queries that should work
    "Write CADQuery code for a simple cube",
    "Generate code to create a basic cylinder",
    
    # Complex queries that might need retries
    "Write CADQuery code for a complex gear with 20 teeth and helical pattern",
    "Generate code to create a spiral staircase with 10 steps",
    "Create CADQuery code for a parametric bracket with multiple holes and fillets",
    "Write code to make a custom part with complex geometry",
    
    # Edge cases that might fail
    "Write CADQuery code for an impossible shape",
    "Generate code to create a part with invalid parameters"
]

async def test_retry_logic():
    """Test the retry logic with various queries"""
    print("🧪 Testing GenX3D Retry Logic")
    print("=" * 50)
    
    try:
        from langgraph_app import run_graph
    except ImportError as e:
        print(f"❌ Error importing langgraph_app: {e}")
        print("Make sure you're in the project root directory")
        return
    
    results = []
    
    for query in retry_test_queries:
        print(f"\n🔍 Testing retry logic: '{query}'")
        
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
                        print(f"✅ Success after {attempts} attempt(s)!")
                        print(f"   Model ID: {parsed_result.get('model_id', 'unknown')}")
                        print(f"   Code length: {len(parsed_result['generated_code'])} characters")
                        
                        results.append({
                            "query": query,
                            "status": "success",
                            "attempts": attempts,
                            "model_id": parsed_result.get('model_id'),
                            "code_length": len(parsed_result['generated_code'])
                        })
                    elif "error" in parsed_result:
                        attempts = parsed_result.get('attempts', 0)
                        print(f"❌ Failed after {attempts} attempt(s): {parsed_result['error']}")
                        
                        if "last_generated_code" in parsed_result:
                            code = parsed_result['last_generated_code']
                            if code and code != "No code generated":
                                print(f"   Last generated code preview: {code[:100]}...")
                        
                        results.append({
                            "query": query,
                            "status": "failed",
                            "attempts": attempts,
                            "error": parsed_result['error'],
                            "last_error": parsed_result.get('last_error', 'Unknown')
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
    print("📊 RETRY LOGIC TEST SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    total = len(results)
    
    print(f"Total tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/total)*100:.1f}%")
    
    # Analyze retry patterns
    if successful > 0:
        successful_tests = [r for r in results if r["status"] == "success"]
        avg_attempts = sum(r["attempts"] for r in successful_tests) / len(successful_tests)
        max_attempts = max(r["attempts"] for r in successful_tests)
        
        print(f"\n📈 Retry Analysis (Successful cases):")
        print(f"   Average attempts: {avg_attempts:.1f}")
        print(f"   Maximum attempts: {max_attempts}")
        
        # Show attempts distribution
        attempts_dist = {}
        for r in successful_tests:
            attempts = r["attempts"]
            attempts_dist[attempts] = attempts_dist.get(attempts, 0) + 1
        
        print(f"   Attempts distribution:")
        for attempts, count in sorted(attempts_dist.items()):
            print(f"     {attempts} attempt(s): {count} case(s)")
    
    # Show successful cases
    if successful > 0:
        print(f"\n✅ Successful generations:")
        for test in [r for r in results if r["status"] == "success"]:
            print(f"  - '{test['query']}' → {test['attempts']} attempt(s), Model: {test['model_id']}")
    
    # Show failed cases
    if failed > 0:
        print(f"\n❌ Failed cases:")
        for test in [r for r in results if r["status"] == "failed"]:
            print(f"  - '{test['query']}' → {test['attempts']} attempt(s), Error: {test['last_error'][:50]}...")

def test_specific_retry():
    """Test retry logic with a specific problematic query"""
    print("\n🎯 Interactive Retry Test")
    print("=" * 30)
    
    query = input("Enter a query that might need retries: ").strip()
    
    if not query:
        print("❌ No query provided")
        return
    
    print(f"\nTesting retry logic: '{query}'")
    
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
    print("🤖 GenX3D Retry Logic Test")
    print("=" * 30)
    print("1. Run all retry logic tests")
    print("2. Test specific retry query")
    print("3. Exit")
    
    choice = input("\nChoose an option (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(test_retry_logic())
    elif choice == "2":
        test_specific_retry()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 