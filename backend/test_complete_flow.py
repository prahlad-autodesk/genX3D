#!/usr/bin/env python3
"""
Test script for the complete flow: user query -> RAG -> model generation -> response
"""

import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))

from langgraph_app import run_graph

async def test_complete_flow():
    """Test the complete flow from user query to model generation"""
    
    print("🚀 Testing Complete Flow: User Query -> RAG -> Model Generation")
    print("=" * 60)
    
    # Test queries that should route to "generate"
    test_queries = [
        "create a cuboid",
        "make a cylinder",
        "generate a sphere",
        "I want a cube",
        "build a simple box"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: '{query}'")
        print("-" * 40)
        
        try:
            # Simulate the /graph_chat endpoint call
            print("1. Sending query to graph...")
            result = await run_graph({"message": query})
            
            print(f"2. Graph result: {result}")
            
            # Parse the result like the main.py endpoint does
            route = result.get("route")
            response = result.get("result")
            
            print(f"3. Route: {route}")
            print(f"4. Response: {response}")
            
            # If routed to generate, parse the JSON response
            if route == "generate":
                try:
                    response_data = json.loads(response)
                    print(f"5. Parsed response:")
                    print(f"   - Text: {response_data.get('text', 'N/A')}")
                    print(f"   - Model URL: {response_data.get('model_url', 'N/A')}")
                    print(f"   - Model Type: {response_data.get('model_type', 'N/A')}")
                    print(f"   - Similarity Score: {response_data.get('similarity_score', 'N/A')}")
                    
                    if 'model_url' in response_data:
                        print(f"✅ SUCCESS: Model generated at {response_data['model_url']}")
                    elif 'error' in response_data:
                        print(f"❌ ERROR: {response_data['error']}")
                    else:
                        print("⚠️  WARNING: No model URL or error in response")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ ERROR: Could not parse response as JSON: {e}")
                    print(f"   Raw response: {response}")
            else:
                print(f"ℹ️  Query routed to '{route}' (not generate)")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
        
        print()

def simulate_frontend_response():
    """Simulate how the frontend would handle the response"""
    print("\n🖥️  Frontend Response Simulation")
    print("=" * 40)
    
    # Simulate the response from /graph_chat endpoint
    mock_response = {
        "success": True,
        "intent": "generate",
        "response": '{"text": "✅ Generated CAD model based on \'create a cuboid\'. Similarity score: 0.856", "model_url": "/temp_models/model_123.step", "model_type": "step", "original_prompt": "create a cuboid", "similarity_score": 0.856}',
        "agent": "GenBot"
    }
    
    print(f"1. Frontend receives: {mock_response}")
    
    # Parse the response
    response_data = json.loads(mock_response["response"])
    
    print(f"2. Parsed response data:")
    print(f"   - Text: {response_data['text']}")
    print(f"   - Model URL: {response_data['model_url']}")
    print(f"   - Model Type: {response_data['model_type']}")
    
    # Simulate loading the model
    model_url = response_data['model_url']
    print(f"3. Frontend would load model from: {model_url}")
    print(f"4. Full URL: http://localhost:8000{model_url}")

if __name__ == "__main__":
    # Test the complete flow
    asyncio.run(test_complete_flow())
    
    # Simulate frontend response handling
    simulate_frontend_response() 