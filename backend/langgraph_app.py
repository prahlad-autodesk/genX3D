from typing import TypedDict, Literal, Union
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
import os
import uuid
import tempfile
import shutil
from pathlib import Path

# RAG imports
from sentence_transformers import SentenceTransformer
import pinecone
import json
import pickle
import faiss
import numpy as np
import pandas as pd
from pathlib import Path

# CADQuery imports
import cadquery as cq
from cadquery import Workplane
CADQUERY_AVAILABLE = True
print("✅ CadQuery is available and ready to generate real CAD models!")

# -----------------------------
# Hybrid RAG Service (Local FAISS + Pinecone)
# -----------------------------
class HybridRAGService:
    def __init__(self):
        # Initialize embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize Pinecone (cloud-based)
        self.pinecone_api_key = "pcsk_4ecFWZ_NVQDcvace68XmvMXouZ2EQY788hyUbRcCLi9i6wzEHUbSB2RNcW1vKScfYwq5Gi"
        self.pinecone_index_name = "genx3d-index"
        
        # Initialize local FAISS
        self.local_index = None
        self.local_data = None
        
        # Try multiple possible paths for the FAISS files
        possible_paths = [
            Path("backend/RAG_PineCone/vector_index.faiss"),  # From project root
            Path("RAG_PineCone/vector_index.faiss"),          # From backend directory
            Path("../backend/RAG_PineCone/vector_index.faiss"), # From other locations
            Path("../../backend/RAG_PineCone/vector_index.faiss")
        ]
        
        # Find the first existing index path
        self.local_index_path = None
        for path in possible_paths:
            if path.exists():
                self.local_index_path = path
                break
        
        # Find the corresponding data path
        self.local_data_path = None
        if self.local_index_path:
            # Replace .faiss with .pkl for data file
            self.local_data_path = self.local_index_path.parent / "vector_data.pkl"
            
        print(f"🔍 FAISS Index path: {self.local_index_path}")
        print(f"🔍 FAISS Data path: {self.local_data_path}")
        
        # Try to initialize both systems
        self._init_pinecone()
        self._init_local_faiss()
        
        print("✅ Hybrid RAG service initialized")
    
    def _init_pinecone(self):
        """Initialize Pinecone cloud-based retrieval"""
        try:
            self.pc = pinecone.Pinecone(api_key=self.pinecone_api_key)
            self.pinecone_index = self.pc.Index(self.pinecone_index_name)
            self.pinecone_available = True
            print("✅ Pinecone cloud RAG initialized")
        except Exception as e:
            print(f"⚠️ Pinecone initialization failed: {e}")
            self.pinecone_available = False
    
    def _init_local_faiss(self):
        """Initialize local FAISS-based retrieval"""
        try:
            if (self.local_index_path and self.local_data_path and 
                self.local_index_path.exists() and self.local_data_path.exists()):
                # Load existing FAISS index and data
                self.local_index = faiss.read_index(str(self.local_index_path))
                with open(self.local_data_path, "rb") as f:
                    self.local_data = pickle.load(f)
                self.local_faiss_available = True
                print(f"✅ Local FAISS RAG initialized with {len(self.local_data)} examples")
            else:
                print("⚠️ Local FAISS files not found, will use fallback data")
                if not self.local_index_path:
                    print("   - Index path is None")
                elif not self.local_data_path:
                    print("   - Data path is None")
                elif not self.local_index_path.exists():
                    print(f"   - Index file not found: {self.local_index_path}")
                elif not self.local_data_path.exists():
                    print(f"   - Data file not found: {self.local_data_path}")
                self.local_faiss_available = False
        except Exception as e:
            print(f"⚠️ Local FAISS initialization failed: {e}")
            self.local_faiss_available = False
    
    def retrieve_code(self, query: str, top_k: int = 3, use_hybrid: bool = True):
        """Retrieve CADQuery code using hybrid approach (local FAISS + Pinecone)"""
        results = []
        
        # Try local FAISS first (faster)
        if self.local_faiss_available:
            try:
                local_results = self._retrieve_local_faiss(query, top_k)
                results.extend(local_results)
                print(f"🔍 Local FAISS: Found {len(local_results)} matches")
            except Exception as e:
                print(f"❌ Local FAISS retrieval failed: {e}")
        
        # Try Pinecone if available and we need more results
        if self.pinecone_available and (len(results) < top_k or not use_hybrid):
            try:
                pinecone_results = self._retrieve_pinecone(query, top_k)
                results.extend(pinecone_results)
                print(f"☁️ Pinecone: Found {len(pinecone_results)} matches")
            except Exception as e:
                print(f"❌ Pinecone retrieval failed: {e}")
        
        # If no results from either system, use fallback
        if not results:
            print("⚠️ No results from RAG systems, using fallback data")
            results = self._get_fallback_matches(query, top_k)
        
        # Remove duplicates and sort by score
        unique_results = self._deduplicate_results(results)
        unique_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        print(f"🎯 Hybrid RAG: Returning {len(unique_results)} unique matches")
        return unique_results[:top_k]
    
    def _retrieve_local_faiss(self, query: str, top_k: int):
        """Retrieve from local FAISS index"""
        if not self.local_faiss_available:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query]).astype("float32")
        
        # Search FAISS index
        D, I = self.local_index.search(query_embedding, k=min(top_k, len(self.local_data)))
        
        results = []
        for i, (distance, idx) in enumerate(zip(D[0], I[0])):
            if idx < len(self.local_data):
                row = self.local_data.iloc[idx]
                # Convert distance to similarity score (1 - normalized distance)
                score = 1.0 - (distance / 2.0)  # Normalize to 0-1 range
                results.append({
                    "metadata": {
                        "code": row.get("code", ""),
                        "prompt": row.get("prompt", "")
                    },
                    "score": score,
                    "source": "local_faiss"
                })
        
        return results
    
    def _retrieve_pinecone(self, query: str, top_k: int):
        """Retrieve from Pinecone cloud index"""
        if not self.pinecone_available:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query])[0].tolist()
        
        # Query Pinecone
        results = self.pinecone_index.query(
            vector=query_embedding, 
            top_k=top_k, 
            include_metadata=True
        )
        
        pinecone_results = []
        for match in results.get("matches", []):
            pinecone_results.append({
                "metadata": match.get("metadata", {}),
                "score": match.get("score", 0),
                "source": "pinecone"
            })
        
        return pinecone_results
    
    def _deduplicate_results(self, results):
        """Remove duplicate results based on code content"""
        seen_codes = set()
        unique_results = []
        
        for result in results:
            code = result.get("metadata", {}).get("code", "")
            # Create a simple hash of the code
            code_hash = hash(code.strip())
            
            if code_hash not in seen_codes:
                seen_codes.add(code_hash)
                unique_results.append(result)
        
        return unique_results
    
    def _get_fallback_matches(self, query: str, top_k: int = 3):
        """Fallback to mock data if both systems fail"""
        print("⚠️ Using fallback mock data")
        mock_data = {
            "create a cuboid": {
                "code": """
# Create a simple cuboid
result = cq.Workplane("XY").box(10, 5, 3)
cq.exporters.export(result, step_file_path, exportType='STEP')
""",
                "prompt": "create a cuboid",
                "score": 0.95
            },
            "make a cylinder": {
                "code": """
# Create a simple cylinder
result = cq.Workplane("XY").circle(5).extrude(10)
cq.exporters.export(result, step_file_path, exportType='STEP')
""",
                "prompt": "make a cylinder", 
                "score": 0.92
            },
            "generate a sphere": {
                "code": """
# Create a simple sphere using Workplane
result = cq.Workplane("XY").sphere(5)
cq.exporters.export(result, step_file_path, exportType='STEP')
""",
                "prompt": "generate a sphere",
                "score": 0.89
            }
        }
        
        # Simple keyword matching for fallback
        query_lower = query.lower()
        matches = []
        
        for key, data in mock_data.items():
            if any(word in query_lower for word in key.split()):
                matches.append({
                    "metadata": {
                        "code": data["code"],
                        "prompt": data["prompt"]
                    },
                    "score": data["score"],
                    "source": "fallback"
                })
        
        if not matches:
            # Return a default cuboid if no match
            matches.append({
                "metadata": {
                    "code": mock_data["create a cuboid"]["code"],
                    "prompt": "default cuboid"
                },
                "score": 0.8,
                "source": "fallback"
            })
        
        return matches[:top_k]

# -----------------------------
# CAD Model Generator
# -----------------------------
class CADModelGenerator:
    def __init__(self):
        self.rag_service = HybridRAGService()
        self.temp_dir = Path("temp_models")
        self.temp_dir.mkdir(exist_ok=True)
    
    def execute_cadquery_code(self, code: str) -> dict:
        """Execute CADQuery code and return path to generated STEP file"""
        try:
            # Create a unique filename
            model_id = str(uuid.uuid4())
            step_file_path = self.temp_dir / f"model_{model_id}.step"
            
            # Execute the CADQuery code
            # We need to create a safe execution environment
            local_vars = {
                'cq': cq,
                'Workplane': Workplane,
                'step_file_path': str(step_file_path)
            }
            
            # Execute the code
            exec(code, {}, local_vars)
            
            # Look for a solid object in the local variables
            solid = None
            for var_name in ['solid', 'result', 'shape']:
                if var_name in local_vars:
                    solid = local_vars[var_name]
                    break
            
            if solid is None:
                raise Exception("No solid object found in variables 'solid', 'result', or 'shape'. Make sure your code creates a variable called 'result'.")
            
            # Export to STEP format
            if not step_file_path.exists():
                print(f"Adding STEP export statement for {type(solid)}...")
                cq.exporters.export(solid, str(step_file_path), exportType='STEP')
            
            # Check if STEP file was created
            if step_file_path.exists():
                print(f"✅ Successfully generated STEP file: {step_file_path}")
                return {
                    "step_path": str(step_file_path),
                    "model_id": model_id
                }
            else:
                raise Exception("STEP file was not created. Make sure your code includes: cq.exporters.export(result, step_file_path, exportType='STEP')")
                
        except SyntaxError as e:
            error_msg = f"Syntax error in generated code: {e}. Line {e.lineno}: {e.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        except NameError as e:
            error_msg = f"Name error in generated code: {e}. Make sure all variables are properly defined."
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        except AttributeError as e:
            error_msg = f"Attribute error in generated code: {e}. Check CADQuery API usage."
            if "Sphere" in str(e):
                error_msg += " Note: Use 'cq.Workplane(\"XY\").sphere(radius)' instead of 'cq.Sphere(radius)'."
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error executing CADQuery code: {e}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def generate_model(self, user_query: str) -> dict:
        """Generate a CAD model using RAG and CADQuery"""
        try:
            # Retrieve relevant code from RAG
            matches = self.rag_service.retrieve_code(user_query, top_k=1)
            
            if not matches:
                return {
                    "text": "❌ Sorry, I couldn't find any relevant CAD code for your request.",
                    "error": "No matching code found"
                }
            
            # Get the best match
            best_match = matches[0]
            code = best_match["metadata"].get("code", "")
            prompt = best_match["metadata"].get("prompt", "")
            score = best_match["score"]
            
            if not code:
                return {
                    "text": "❌ Retrieved code is empty or invalid.",
                    "error": "Empty code"
                }
            
            # Execute the code to generate the model
            file_paths = self.execute_cadquery_code(code)
            
            # Create relative URL for the frontend
            step_relative_path = f"/temp_models/{Path(file_paths['step_path']).name}"
            
            return {
                "text": f"✅ Generated CAD model based on '{user_query}'. Similarity score: {score:.3f}",
                "step_url": step_relative_path,
                "model_type": "step",
                "original_prompt": prompt,
                "similarity_score": score,
                "model_id": file_paths['model_id']
            }
            
        except Exception as e:
            return {
                "text": f"❌ Error generating model: {str(e)}",
                "error": str(e)
            }

# Initialize the CAD model generator
cad_generator = CADModelGenerator()

# -----------------------------
# State definition
# -----------------------------
class AppState(TypedDict):
    message: str
    route: Union[Literal["help"], Literal["generate"], Literal["create_cad"], Literal["code_gen"]]
    result: str

# -----------------------------
# LLM Setup
# -----------------------------
# For testing, create a mock LLM
class MockLLM:
    async def ainvoke(self, messages):
        class MockResponse:
            def __init__(self, content):
                self.content = content
        
        # Enhanced routing logic for testing
        message_content = messages[0].content if messages else ""
        
        # Check if this is a routing request
        if "router" in message_content.lower() or "available actions" in message_content.lower():
            # Extract the user message from the routing prompt
            user_message = ""
            if 'User message:' in message_content:
                user_message = message_content.split('User message:')[1].split('\n')[0].strip().strip('"')
            
            # Enhanced routing logic
            user_message_lower = user_message.lower()
            
            # Generation keywords (RAG-based)
            generation_keywords = [
                "create", "generate", "make", "build", "design", "model",
                "cylinder", "cube", "sphere", "cuboid", "box", "gear", "bracket",
                "part", "object", "shape", "component"
            ]
            
            # Code generation keywords
            code_gen_keywords = [
                "write code", "generate code", "cadquery code", "custom code",
                "program", "script", "complex", "assembly", "staircase", "parametric"
            ]
            
            # Help keywords
            help_keywords = [
                "what is", "how to", "explain", "help", "understand", "difference",
                "concept", "guide", "tutorial", "question", "why", "when", "where"
            ]
            
            # Check for code generation requests first
            if any(keyword in user_message_lower for keyword in code_gen_keywords):
                return MockResponse("code_gen")
            
            # Check for generation requests (RAG-based)
            elif any(keyword in user_message_lower for keyword in generation_keywords):
                return MockResponse("generate")
            
            # Check for help requests
            elif any(keyword in user_message_lower for keyword in help_keywords):
                return MockResponse("help")
            
            # Default to generate for CAD-related requests
            else:
                return MockResponse("generate")
        
        # For non-routing requests, provide a helpful response
        else:
            return MockResponse("This is a mock response for testing. Set up a real LLM API key for full functionality.")

# LLM Configuration
# Choose one of the following options:

# Option 1: Groq (Fast & Free tier available)
# Get API key from: https://console.groq.com/
if os.getenv("GROQ_API_KEY"):
    llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192"  # Fast and powerful
    )
    print("✅ Using Groq LLM")

# Option 2: OpenAI (Requires API key)
elif os.getenv("OPENAI_API_KEY"):
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"  # Fast and cost-effective
    )
    print("✅ Using OpenAI LLM")

# Option 3: Anthropic Claude (Requires API key)
elif os.getenv("ANTHROPIC_API_KEY"):
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-haiku-20240307"  # Fast and cost-effective
    )
    print("✅ Using Anthropic Claude LLM")

# Option 4: Local Ollama (Free, requires Ollama installation)
elif os.getenv("USE_OLLAMA"):
    from langchain_community.llms import Ollama
    llm = Ollama(
        model="llama3.2:3b",  # Fast local model
        base_url="http://localhost:11434"
    )
    print("✅ Using local Ollama LLM")

# Fallback to mock LLM
else:
    llm = MockLLM()
    print("⚠️ Using Mock LLM - Set an API key to use a real LLM")
    print("💡 Available options:")
    print("   - GROQ_API_KEY (recommended - free tier available)")
    print("   - OPENAI_API_KEY")
    print("   - ANTHROPIC_API_KEY")
    print("   - USE_OLLAMA=true (requires Ollama installation)")

# -----------------------------
# Analyzer Node
# -----------------------------
async def analyze_node(state: AppState) -> AppState:
    message = state["message"]
    
    # Enhanced routing logic with better prompts
    routing_prompt = f"""You are an intelligent router for a CAD assistant system. Analyze the user's message and determine the best action to take.

User message: "{message}"

Available actions:
1. "help" - For questions about CAD concepts, how-to guides, explanations, troubleshooting, or general assistance
2. "generate" - For requests to create, build, make, design, or generate CAD models, parts, or 3D objects (using RAG)
3. "code_gen" - For requests to generate custom CADQuery code from scratch, complex designs, or when user wants code generation
4. "create_cad" - For specific CAD modeling requests, technical design questions, or parametric modeling

Examples:
- "How do I create a cylinder?" → generate
- "What is parametric modeling?" → help  
- "Create a gear with 20 teeth" → generate
- "Help me understand STEP files" → help
- "Design a bracket for mounting" → generate
- "What's the difference between STL and STEP?" → help
- "Make me a cube" → generate
- "I need help with this design" → help
- "Generate CADQuery code for a spiral staircase" → code_gen
- "Write code to create a custom part" → code_gen
- "Create CADQuery code for a complex assembly" → code_gen

Respond with ONLY one word: help, generate, code_gen, or create_cad."""

    try:
        response = await llm.ainvoke([HumanMessage(content=routing_prompt)])
        route = response.content.strip().lower()
        
        # Validate the route
        valid_routes = ["help", "generate", "create_cad", "code_gen"]
        if route not in valid_routes:
            print(f"⚠️ Invalid route '{route}' from LLM, defaulting to 'help'")
            route = "help"
        
        print(f"🔀 Router decision: '{message}' → {route}")
        return {**state, "route": route}
        
    except Exception as e:
        print(f"❌ Router error: {e}, defaulting to 'help'")
        return {**state, "route": "help"}

# -----------------------------
# Agent Nodes
# -----------------------------
async def help_node(state: AppState) -> AppState:
    message = state["message"]
    prompt = f"""You are HelpBot, a knowledgeable CAD and technical assistant. Provide helpful, accurate, and detailed answers to user questions.

Context: You're helping users with CAD concepts, technical questions, and design guidance.

User question: {message}

Guidelines:
- Be clear and concise
- Use examples when helpful
- Explain technical concepts in accessible terms
- If the question is about CAD software or tools, mention relevant options
- If you're not sure about something, say so rather than guessing

Assistant:"""
    
    try:
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        return {**state, "result": response.content}
    except Exception as e:
        error_response = f"I'm sorry, I encountered an error while processing your question. Please try again or contact support if the issue persists. Error: {str(e)}"
        return {**state, "result": error_response}

async def generate_node(state: AppState) -> AppState:
    message = state["message"]
    
    print(f"🎯 Generating CAD model for: '{message}'")
    
    try:
        # Use RAG to generate CAD model
        result = cad_generator.generate_model(message)
        
        # Convert result to string for state
        if isinstance(result, dict):
            result_str = json.dumps(result)
            print(f"✅ Model generation successful: {result.get('model_id', 'unknown')}")
        else:
            result_str = str(result)
            print(f"✅ Model generation completed")
        
        return {**state, "result": result_str}
        
    except Exception as e:
        error_msg = f"❌ Error generating CAD model: {str(e)}"
        print(error_msg)
        return {**state, "result": json.dumps({"error": error_msg})}

async def create_cad_node(state: AppState) -> AppState:
    message = state["message"]
    # Provide a URL to the STEP model for the frontend to load
    response = {
        "text": f"🛠 CADBot: Creating a CAD model related to '{message}'. Here is your model.",
        "model_url": "/model.step",
        "model_type": "step"
    }
    return {**state, "result": response}

async def code_gen_node(state: AppState) -> AppState:
    """Generate CADQuery code using LLM and execute it to create a model"""
    message = state["message"]
    
    print(f"🤖 Generating CADQuery code for: '{message}'")
    
    max_retries = 3
    attempt = 0
    
    while attempt < max_retries:
        attempt += 1
        print(f"🔄 Attempt {attempt}/{max_retries}")
        
        try:
            # Step 1: Retrieve relevant examples from hybrid RAG (local FAISS + Pinecone)
            print(f"🔍 Retrieving relevant CADQuery examples from hybrid RAG...")
            rag_examples = cad_generator.rag_service.retrieve_code(message, top_k=3, use_hybrid=True)
            
            # Step 2: Build examples string for the prompt
            examples_text = ""
            if rag_examples and len(rag_examples) > 0:
                examples_text = "\n\nHere are some relevant CADQuery examples from our knowledge base:\n"
                for i, example in enumerate(rag_examples[:2], 1):
                    example_code = example["metadata"].get("code", "")
                    example_prompt = example["metadata"].get("prompt", "")
                    similarity_score = example.get("score", 0)
                    
                    if example_code:
                        examples_text += f"\nExample {i} (similarity: {similarity_score:.3f}):\n"
                        examples_text += f"Prompt: {example_prompt}\n"
                        examples_text += f"Code:\n```python\n{example_code}\n```\n"
                
                print(f"📚 Found {len(rag_examples)} relevant examples")
            else:
                examples_text = "\n\nNo specific examples found, but here's a basic structure:\n"
                examples_text += "```python\nimport cadquery as cq\nfrom cadquery import Workplane\n\n# Create the model\nresult = cq.Workplane(\"XY\").box(10, 5, 3)\n\n# Export to STEP (use the provided step_file_path variable)\ncq.exporters.export(result, step_file_path, exportType='STEP')\n```\n"
                examples_text += "\n\nCommon CADQuery patterns:\n"
                examples_text += "- Sphere: `cq.Workplane(\"XY\").sphere(radius)`\n"
                examples_text += "- Cylinder: `cq.Workplane(\"XY\").circle(radius).extrude(height)`\n"
                examples_text += "- Box: `cq.Workplane(\"XY\").box(width, length, height)`\n"
                print(f"📚 No specific examples found, using basic template")
            
            # Step 3: Generate CADQuery code using LLM with RAG examples
            if attempt == 1:
                # Initial prompt with RAG examples
                code_generation_prompt = f"""You are an expert CADQuery programmer. Generate Python CADQuery code to create a 3D model based on the user's request.

User request: "{message}"

Requirements:
1. Use only CADQuery (import as cq) and its standard library
2. Create a complete, runnable Python script
3. The final object should be stored in a variable called 'result'
4. IMPORTANT: Use the provided 'step_file_path' variable for export, do NOT create your own path
5. Export using: cq.exporters.export(result, step_file_path, exportType='STEP')
6. Make the design parametric where appropriate
7. Include comments explaining the design steps
8. Handle edge cases and errors gracefully
9. Ensure the code is syntactically correct and follows CADQuery best practices
10. Use the examples below as inspiration, but adapt them to the specific request
11. IMPORTANT: Use Workplane methods like 'cq.Workplane("XY").sphere(radius)' NOT 'cq.Sphere(radius)'

{examples_text}

IMPORTANT: Generate ONLY the Python code. Do NOT include any explanations, markdown formatting, or text outside of the code. The response should be pure Python code that can be executed directly."""
            else:
                # Retry prompt with error context and RAG examples
                code_generation_prompt = f"""You are an expert CADQuery programmer. The previous code generation failed with this error: "{last_error}"

User request: "{message}"

Please fix the code and generate a corrected version. Common issues to avoid:
1. Syntax errors (missing colons, parentheses, etc.)
2. Undefined variables or imports
3. Incorrect CADQuery API usage (use Workplane methods, not direct classes)
4. Missing export statement
5. Invalid geometry operations
6. Using hardcoded file paths instead of the provided 'step_file_path' variable

Requirements:
1. Use only CADQuery (import as cq) and its standard library
2. Create a complete, runnable Python script
3. The final object should be stored in a variable called 'result'
4. IMPORTANT: Use the provided 'step_file_path' variable for export, do NOT create your own path
5. Export using: cq.exporters.export(result, step_file_path, exportType='STEP')
6. Make the design parametric where appropriate
7. Include comments explaining the design steps
8. Handle edge cases and errors gracefully
9. Ensure the code is syntactically correct and follows CADQuery best practices
10. Use the examples below as inspiration, but adapt them to the specific request
11. IMPORTANT: Use Workplane methods like 'cq.Workplane("XY").sphere(radius)' NOT 'cq.Sphere(radius)'

{examples_text}

IMPORTANT: Generate ONLY the Python code. Do NOT include any explanations, markdown formatting, or text outside of the code. The response should be pure Python code that can be executed directly."""

            # Generate the code
            code_response = await llm.ainvoke([HumanMessage(content=code_generation_prompt)])
            generated_code = code_response.content.strip()
            
            # Enhanced code cleaning logic
            print(f"🔧 Raw LLM response:\n{generated_code}")
            
            # Remove markdown code blocks
            if "```python" in generated_code:
                # Extract code between ```python and ```
                start_marker = "```python"
                end_marker = "```"
                start_idx = generated_code.find(start_marker)
                if start_idx != -1:
                    start_idx += len(start_marker)
                    end_idx = generated_code.find(end_marker, start_idx)
                    if end_idx != -1:
                        generated_code = generated_code[start_idx:end_idx].strip()
                    else:
                        # No closing ```, take everything after ```python
                        generated_code = generated_code[start_idx:].strip()
            elif "```" in generated_code:
                # Extract code between ``` and ```
                start_marker = "```"
                end_marker = "```"
                start_idx = generated_code.find(start_marker)
                if start_idx != -1:
                    start_idx += len(start_marker)
                    end_idx = generated_code.find(end_marker, start_idx)
                    if end_idx != -1:
                        generated_code = generated_code[start_idx:end_idx].strip()
                    else:
                        # No closing ```, take everything after ```
                        generated_code = generated_code[start_idx:].strip()
            
            # Remove explanatory text (lines that don't look like Python code)
            lines = generated_code.split('\n')
            cleaned_lines = []
            in_code_block = False
            
            for line in lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                # Skip lines that are clearly explanatory text
                if (line.startswith("Here is") or 
                    line.startswith("This code") or 
                    line.startswith("The code") or
                    line.startswith("You can") or
                    line.startswith("To create") or
                    line.startswith("This will") or
                    line.startswith("The result") or
                    line.startswith("Note:") or
                    line.startswith("Example:") or
                    line.startswith("Output:") or
                    line.startswith("Result:") or
                    line.startswith("Code:") or
                    line.startswith("Python code:") or
                    line.startswith("CADQuery code:")):
                    continue
                
                # Keep lines that look like Python code
                if (line.startswith('import') or 
                    line.startswith('from') or
                    line.startswith('#') or
                    line.startswith('result') or
                    line.startswith('cq.') or
                    line.startswith('step_file_path') or
                    line.startswith('def ') or
                    line.startswith('class ') or
                    line.startswith('if ') or
                    line.startswith('for ') or
                    line.startswith('while ') or
                    line.startswith('try:') or
                    line.startswith('except:') or
                    line.startswith('finally:') or
                    line.startswith('with ') or
                    line.startswith('return ') or
                    line.startswith('print(') or
                    line.startswith('assert ') or
                    '=' in line or  # Variable assignments
                    '(' in line or  # Function calls
                    '[' in line or  # Lists/arrays
                    '{' in line or  # Dictionaries
                    '.' in line):   # Method calls
                    cleaned_lines.append(line)
            
            generated_code = '\n'.join(cleaned_lines)
            generated_code = generated_code.strip()
            
            print(f"📝 Generated CADQuery code (attempt {attempt}):\n{generated_code}")
            
            # Step 2: Validate the generated code
            if not generated_code:
                raise Exception("No valid Python code was generated. The LLM response was empty or contained only explanatory text.")
            
            # Basic validation - check if it looks like Python code
            if not any(keyword in generated_code.lower() for keyword in ['import', 'cq.', 'result']):
                raise Exception("Generated code doesn't appear to be valid CADQuery Python code. Missing essential elements like imports or CADQuery operations.")
            
            # Check if the code uses the correct step_file_path variable
            if 'step_file_path' not in generated_code:
                raise Exception("Generated code doesn't use the required 'step_file_path' variable. Please use the provided variable instead of creating your own path.")
            
            # Check for hardcoded file paths
            if any(hardcoded in generated_code.lower() for hardcoded in ['"sphere.step"', '"cube.step"', '"cylinder.step"', '"model.step"', '"output.step"']):
                raise Exception("Generated code contains hardcoded file paths. Please use the provided 'step_file_path' variable instead.")
            
            # Step 3: Execute the generated code
            result = cad_generator.execute_cadquery_code(generated_code)
            
            # Step 4: Create response
            step_relative_path = f"/temp_models/{Path(result['step_path']).name}"
            
            # Prepare RAG examples info for response
            rag_info = []
            rag_sources = set()
            if rag_examples and len(rag_examples) > 0:
                for example in rag_examples[:3]:
                    rag_info.append({
                        "prompt": example["metadata"].get("prompt", ""),
                        "similarity_score": example.get("score", 0),
                        "source": example.get("source", "unknown")
                    })
                    rag_sources.add(example.get("source", "unknown"))
            
            response = {
                "text": f"✅ Generated custom CADQuery code and created model for '{message}' (attempt {attempt})",
                "step_url": step_relative_path,
                "model_type": "step",
                "generated_code": generated_code,
                "model_id": result['model_id'],
                "method": "llm_code_generation_with_hybrid_rag",
                "attempts": attempt,
                "rag_examples_used": rag_info,
                "examples_count": len(rag_info),
                "rag_sources": list(rag_sources)
            }
            
            print(f"✅ Code generation successful on attempt {attempt}: {result['model_id']}")
            return {**state, "result": json.dumps(response)}
            
        except Exception as e:
            last_error = str(e)
            print(f"❌ Attempt {attempt} failed: {last_error}")
            
            if attempt >= max_retries:
                # Final failure - provide detailed error response
                error_msg = f"❌ Code generation failed after {max_retries} attempts. Last error: {last_error}"
                print(error_msg)
                
                # Try to provide a fallback response with debugging info
                fallback_response = {
                    "error": error_msg,
                    "attempts": max_retries,
                    "last_generated_code": generated_code if 'generated_code' in locals() else "No code generated",
                    "last_error": last_error,
                    "rag_examples_attempted": rag_info if 'rag_info' in locals() else [],
                    "suggestion": "Try simplifying your request or check if the requested geometry is valid."
                }
                return {**state, "result": json.dumps(fallback_response)}
            else:
                # Continue to next attempt
                print(f"🔄 Retrying with error context...")
                continue

# -----------------------------
# Router Function
# -----------------------------
def route_from_analyzer(state: AppState) -> str:
    return state["route"]

# -----------------------------
# Graph Build
# -----------------------------
builder = StateGraph(AppState)

builder.add_node("analyze", analyze_node)
builder.add_node("help", help_node)
builder.add_node("generate", generate_node)
builder.add_node("create_cad", create_cad_node)
builder.add_node("code_gen", code_gen_node)

builder.set_entry_point("analyze")

builder.add_conditional_edges("analyze", route_from_analyzer, {
    "help": "help",
    "generate": "generate",
    "create_cad": "create_cad",
    "code_gen": "code_gen"
})

builder.add_edge("help", END)
builder.add_edge("generate", END)
builder.add_edge("create_cad", END)
builder.add_edge("code_gen", END)

graph = builder.compile()

# -----------------------------
# Run Function
# -----------------------------
async def run_graph(input_data: dict):
    state = {"message": input_data.get("message", "")}
    return await graph.ainvoke(state)
