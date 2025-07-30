#!/bin/bash

# Test script for RAG functionality using curl
# Make sure the server is running: uvicorn main:app --reload

echo "🧪 Testing RAG CAD Model Generation via API"
echo "============================================="

# Test 1: Generate a cuboid
echo -e "\n📝 Test 1: Creating a cuboid"
echo "--------------------------------"
curl -X POST "http://localhost:8000/graph_chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "create a cuboid"}' \
     | jq '.'

# Test 2: Generate a cylinder
echo -e "\n📝 Test 2: Creating a cylinder"
echo "--------------------------------"
curl -X POST "http://localhost:8000/graph_chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "make a cylinder"}' \
     | jq '.'

# Test 3: Generate a sphere
echo -e "\n📝 Test 3: Creating a sphere"
echo "--------------------------------"
curl -X POST "http://localhost:8000/graph_chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "generate a sphere"}' \
     | jq '.'

# Test 4: Help query (should not generate model)
echo -e "\n📝 Test 4: Help query (should route to help)"
echo "--------------------------------"
curl -X POST "http://localhost:8000/graph_chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "how do I create a CAD model?"}' \
     | jq '.'

echo -e "\n✅ Testing complete!"
echo "Check the responses above for model URLs and download them if needed." 