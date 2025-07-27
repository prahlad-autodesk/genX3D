from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import os
from typing import List

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
from langchain.schema import HumanMessage
try:
    from backend.langgraph_app import run_graph
except ImportError:
    from langgraph_app import run_graph

app = FastAPI()

# ✅ Enable CORS for frontend origin (e.g. Cascade Studio or local test)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:8001", 
        "http://localhost:3000",
        "https://*.onrender.com",
        "https://*.vercel.app",
        "https://*.netlify.app",
        "https://genx3d.onrender.com/app"
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

# Mount static and templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

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
app.mount("/documentation", StaticFiles(directory=DOCS_DIR, html=True), name="documentation")
# Access documentation at http://localhost:8000/documentation/

# Serve STEP model
@app.get("/model.step", response_class=FileResponse)
def get_step():
    return FileResponse(path=step_path, media_type='application/step', filename="model.step")

# ✅ Serve STL model with CORS working
@app.get("/model.stl", response_class=FileResponse)
def get_stl():
    return FileResponse(path=stl_path, media_type='application/sla', filename="model.stl")

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
            "create_cad": "CADBot"
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

# Redirect root to documentation
@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/documentation/")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "genx3D API is running"}