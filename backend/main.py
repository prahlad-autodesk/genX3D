from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import os
from typing import List
import atexit

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, continue without it
    pass


# import cadquery as cq
# from cadquery import exporters

# LLM imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
# from langgraph_app import run_graph, cad_generator
from graph.langgraph_app import run_graph, cad_generator


app = FastAPI()

# ✅ Enable CORS for frontend origin (e.g. Cascade Studio or local test)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:8001", 
        "http://localhost:3000",
        "http://localhost:8080",  # Frontend server port
        "http://127.0.0.1:8000",  # React app served from same server
        "http://127.0.0.1:8080",  # Frontend server IP
        "https://*.onrender.com",
        "https://*.vercel.app",
        "https://*.netlify.app",
        "https://genx3d.onrender.com/app",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Define React build directory early for route handlers
REACT_BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend-react/build"))

# Handle React app's absolute asset paths by serving files directly (must come before /static mount)
@app.get("/static/js/{filename}")
def serve_react_js(filename: str):
    if os.path.exists(REACT_BUILD_DIR):
        js_path = os.path.join(REACT_BUILD_DIR, "static", "js", filename)
        if os.path.exists(js_path):
            return FileResponse(path=js_path, media_type='application/javascript', filename=filename)
    return JSONResponse({"error": "JS file not found"}, status_code=404)

@app.get("/static/css/{filename}")  
def serve_react_css(filename: str):
    if os.path.exists(REACT_BUILD_DIR):
        css_path = os.path.join(REACT_BUILD_DIR, "static", "css", filename)
        if os.path.exists(css_path):
            return FileResponse(path=css_path, media_type='text/css', filename=filename)
    return JSONResponse({"error": "CSS file not found"}, status_code=404)

# Serve React app's manifest.json at root level
@app.get("/manifest.json", response_class=FileResponse)
def get_react_manifest():
    if os.path.exists(REACT_BUILD_DIR):
        manifest_path = os.path.join(REACT_BUILD_DIR, "manifest.json")
        if os.path.exists(manifest_path):
            return FileResponse(path=manifest_path, media_type='application/json', filename="manifest.json")
    return JSONResponse({"error": "Manifest not found"}, status_code=404)

# Serve React app's favicon and other assets at root level
@app.get("/favicon.ico", response_class=FileResponse)
def get_react_favicon():
    if os.path.exists(REACT_BUILD_DIR):
        favicon_path = os.path.join(REACT_BUILD_DIR, "favicon.ico")
        if os.path.exists(favicon_path):
            return FileResponse(path=favicon_path, media_type='image/x-icon', filename="favicon.ico")
    return JSONResponse({"error": "Favicon not found"}, status_code=404)

@app.get("/logo192.png", response_class=FileResponse)
def get_react_logo192():
    if os.path.exists(REACT_BUILD_DIR):
        logo_path = os.path.join(REACT_BUILD_DIR, "logo192.png")
        if os.path.exists(logo_path):
            return FileResponse(path=logo_path, media_type='image/png', filename="logo192.png")
    return JSONResponse({"error": "Logo not found"}, status_code=404)

# Mount static and templates (backend static files)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Mount React app at /app2
if os.path.exists(REACT_BUILD_DIR):
    app.mount("/app2", StaticFiles(directory=REACT_BUILD_DIR, html=True), name="app2")
    print(f"✅ React app mounted at /app2 from {REACT_BUILD_DIR}")
else:
    print(f"⚠️ React build directory not found: {REACT_BUILD_DIR}")

# File paths
step_path = os.path.join(STATIC_DIR, "model.step")
stl_path = os.path.join(STATIC_DIR, "model.stl")

# === Create hollow cylinder ===
# outer = cq.Workplane("XY").circle(10).extrude(20)
# inner = cq.Workplane("XY").circle(6).extrude(20)
# model = outer.cut(inner)

# Export STEP and STL
# exporters.export(model, step_path, exportType='STEP')
# exporters.export(model, stl_path, exportType='STL')

# Serve Cascade Studio static files at /app (not /) to avoid API conflicts
# Update the path to the new frontend location
CASCADE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/CascadeStudio"))
app.mount("/app", StaticFiles(directory=CASCADE_DIR, html=True), name="cascade")
# Now access Cascade Studio at http://localhost:8000/app/
# API endpoints like /chat will work as expected

# Serve Documentation static files at /documentation
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/docs"))
if os.path.exists(DOCS_DIR):
    app.mount("/documentation", StaticFiles(directory=DOCS_DIR, html=True), name="documentation")
    print(f"✅ Documentation mounted at /documentation from {DOCS_DIR}")
else:
    print(f"⚠️ Documentation directory not found: {DOCS_DIR}")

# Also serve docs at /docs for convenience
if os.path.exists(DOCS_DIR):
    app.mount("/docs", StaticFiles(directory=DOCS_DIR, html=True), name="docs")
    print(f"✅ Documentation also available at /docs")

# Access documentation at http://localhost:8000/documentation/ or http://localhost:8000/docs/

# Serve STEP model
@app.get("/model.step", response_class=FileResponse)
def get_step():
    return FileResponse(path=step_path, media_type='application/step', filename="model.step")

# ✅ Serve STL model with CORS working
@app.get("/model.stl", response_class=FileResponse)
def get_stl():
    return FileResponse(path=stl_path, media_type='application/sla', filename="model.stl")

# Serve temporary model files
@app.get("/temp_models/{filename}")
def get_temp_model(filename: str):
    temp_models_dir = "temp_models"
    file_path = os.path.join(temp_models_dir, filename)
    
    if not os.path.exists(file_path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    
    # Determine content type based on file extension
    ext = os.path.splitext(filename)[1].lower()
    content_type_map = {
        '.step': 'application/step',
        '.stl': 'application/sla',
        '.glb': 'model/gltf-binary'
    }
    content_type = content_type_map.get(ext, 'application/octet-stream')
    
    return FileResponse(
        path=file_path, 
        media_type=content_type, 
        filename=filename
    )

# Mount temp_models directory for static file serving
TEMP_MODELS_DIR = "temp_models"
os.makedirs(TEMP_MODELS_DIR, exist_ok=True)
app.mount("/temp_models", StaticFiles(directory=TEMP_MODELS_DIR), name="temp_models")

# === Chat endpoint for assistant ===
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(body: ChatRequest):
    # model_name = "mistralai/mixtral-8x7b"  # or any other model you want
    # llm = ChatOpenAI(
    #     base_url="https://openrouter.ai/api/v1",
    #     api_key=os.getenv("OPENROUTER_API_KEY"),
    #     # model=model_name,
    #     # name=model_name,
    #     max_completion_tokens=200,
    #     temperature=0.7,
    #     streaming=False
    # )

    llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",  # Groq uses OpenAI-compatible API
        api_key=os.getenv("GROQ_API_KEY"),          # Store key in .env for security
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        name="groq-llama"
    )
    try:
        response = await llm.ainvoke([HumanMessage(content=body.message)])
        reply = response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        reply = f"[Error from LLM: {e}]"
    return JSONResponse({"reply": reply})

# @app.post("/graph_chat")
# async def graph_chat_endpoint(body: ChatRequest):
#     result = await run_graph({"message": body.message})
#     return result

# Endpoint to trigger the graph
@app.post("/graph_chat")
async def graph_chat_endpoint(body: ChatRequest):
    try:
        result = await run_graph({"message": body.message})
        # Map route to agent name
        route = result.get("route") or result.get("next")
        agent_map = {
            "help": "HelpBot",
            "generate": "GenBot",
            "create_cad": "CADBot",
            "code_gen": "GenBot"  # code_gen also creates models, so map to GenBot
        }
        agent = agent_map.get(route, route)
        return {
            "success": True,
            "intent": result.get("next"),
            "response": result.get("result"),
            "agent": agent,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

# Endpoint to list generated models in static/generated_models
@app.get("/list_generated_models")
def list_generated_models():
    models_dir = os.path.join("static", "generated_models")
    allowed_ext = {".step", ".stl", ".glb"}
    if not os.path.exists(models_dir):
        return JSONResponse([])
    files = []
    for fname in os.listdir(models_dir):
        ext = os.path.splitext(fname)[1].lower()
        if ext in allowed_ext:
            files.append({
                "name": fname,
                "url": f"/static/generated_models/{fname}"
            })
    return JSONResponse(files)

# API information endpoint
@app.get("/api/info")
async def api_info():
    """Get information about available API endpoints"""
    return {
        "name": "genx3D API",
        "version": "1.0.0",
        "description": "AI-powered CAD model generation with RAG and LangGraph",
        "endpoints": {
            "chat": {
                "url": "/chat",
                "method": "POST",
                "description": "Simple chat with LLM"
            },
            "graph_chat": {
                "url": "/graph_chat", 
                "method": "POST",
                "description": "Advanced chat with intelligent routing and CAD generation"
            },
            "health": {
                "url": "/health",
                "method": "GET", 
                "description": "Health check endpoint"
            },
            "models": {
                "url": "/list_generated_models",
                "method": "GET",
                "description": "List generated CAD models"
            },
            "cleanup_stats": {
                "url": "/cleanup/stats",
                "method": "GET",
                "description": "Get cleanup service statistics"
            },
            "cleanup_manual": {
                "url": "/cleanup/manual",
                "method": "POST",
                "description": "Manually trigger cleanup of old files"
            }
        },
        "documentation": {
            "main": "/documentation/",
            "alt": "/docs/",
            "description": "Full API documentation and guides"
        },
        "frontend": {
            "cascade_studio": "/app/",
            "react_app": "/app2/",
            "description": "3D CAD viewer and editor interfaces"
        }
    }

# Redirect root to documentation
@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/documentation/")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "genx3D API is running",
        "version": "1.0.0",
        "features": [
            "Hybrid RAG (Local FAISS + Pinecone)",
            "LLM-powered CAD code generation", 
            "Real-time 3D model creation",
            "Intelligent routing system",
            "Cascade Studio integration"
        ],
        "documentation": {
            "available": os.path.exists(DOCS_DIR),
            "path": DOCS_DIR,
            "urls": ["/documentation/", "/docs/"]
        }
    }

# Cleanup endpoints
@app.get("/cleanup/stats")
async def get_cleanup_stats():
    """Get cleanup service statistics"""
    try:
        stats = cad_generator.get_cleanup_stats()
        return {
            "status": "success",
            "cleanup_stats": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get cleanup stats: {str(e)}"
        }

@app.post("/cleanup/manual")
async def trigger_manual_cleanup():
    """Manually trigger cleanup of old files"""
    try:
        stats = cad_generator.manual_cleanup()
        return {
            "status": "success",
            "message": "Manual cleanup completed",
            "cleanup_stats": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to trigger manual cleanup: {str(e)}"
        }

# Graceful shutdown handler
@atexit.register
def cleanup_on_exit():
    """Stop cleanup service when application exits"""
    try:
        if hasattr(cad_generator, 'cleanup_service'):
            cad_generator.cleanup_service.stop_cleanup_service()
            print("🛑 Cleanup service stopped on application exit")
    except Exception as e:
        print(f"⚠️ Error stopping cleanup service on exit: {e}")

# Register startup event handler for FastAPI
@app.on_event("startup")
async def startup_event():
    """Handle FastAPI startup event"""
    try:
        if hasattr(cad_generator, 'cleanup_service'):
            # Ensure cleanup service is running
            if not cad_generator.cleanup_service.running:
                cad_generator.cleanup_service.start_cleanup_service()
            print("✅ Cleanup service started on FastAPI startup")
    except Exception as e:
        print(f"⚠️ Error starting cleanup service on startup: {e}")

# Register shutdown event handler for FastAPI
@app.on_event("shutdown")
async def shutdown_event():
    """Handle FastAPI shutdown event"""
    try:
        if hasattr(cad_generator, 'cleanup_service'):
            cad_generator.cleanup_service.stop_cleanup_service()
            print("🛑 Cleanup service stopped on FastAPI shutdown")
    except Exception as e:
        print(f"⚠️ Error stopping cleanup service on shutdown: {e}")