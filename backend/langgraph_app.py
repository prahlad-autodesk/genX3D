from typing import TypedDict, Literal, Union
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
import os

# -----------------------------
# State definition
# -----------------------------
class AppState(TypedDict):
    message: str
    route: Union[Literal["help"], Literal["generate"], Literal["create_cad"]]
    result: str

# -----------------------------
# LLM Setup
# -----------------------------
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    # model="mistralai/mixtral-8x7b",
    temperature=0.0,
    max_tokens=200,
    streaming=False
)

# -----------------------------
# Analyzer Node
# -----------------------------
async def analyze_node(state: AppState) -> AppState:
    message = state["message"]
    response = await llm.ainvoke([
        HumanMessage(content=f'''You are a router. Given this user message: "{message}",
decide whether the user needs:
- help (if they are asking for guidance),
- generate (if they want to generate something),
- create_cad (if they are asking for a CAD model or design).

Only answer with one word: help, generate, or create_cad.''')
    ])
    route = response.content.strip().lower()
    return {**state, "route": route}

# -----------------------------
# Agent Nodes
# -----------------------------
async def help_node(state: AppState) -> AppState:
    message = state["message"]
    prompt = f"You are HelpBot, a helpful assistant for CAD and technical questions. Answer the following user question as helpfully as possible:\n\nUser: {message}\n\nAssistant:"
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {**state, "result": response.content}

async def generate_node(state: AppState) -> AppState:
    message = state["message"]
    response = f"🪄 GenBot: I can generate something based on '{message}'. Here's a mock result."
    return {**state, "result": response}

async def create_cad_node(state: AppState) -> AppState:
    message = state["message"]
    # Provide a URL to the STEP model for the frontend to load
    response = {
        "text": f"🛠 CADBot: Creating a CAD model related to '{message}'. Here is your model.",
        "model_url": "/model.step",
        "model_type": "step"
    }
    return {**state, "result": response}

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

builder.set_entry_point("analyze")

builder.add_conditional_edges("analyze", route_from_analyzer, {
    "help": "help",
    "generate": "generate",
    "create_cad": "create_cad"
})

builder.add_edge("help", END)
builder.add_edge("generate", END)
builder.add_edge("create_cad", END)

graph = builder.compile()

# -----------------------------
# Run Function
# -----------------------------
async def run_graph(input_data: dict):
    state = {"message": input_data.get("message", "")}
    return await graph.ainvoke(state)
