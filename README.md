# GenX3D

A next-generation 3D CAD assistant platform combining browser-based parametric modeling (Cascade Studio) with an AI-powered backend for chat, model generation, and analysis.

## Features
- Web-based 3D CAD modeling (Cascade Studio)
- AI chat assistant (LLM-powered)
- Intelligent routing system for different query types
- Model generation, analysis, and help agents
- **LLM-powered CADQuery code generation** (NEW!)
- RAG-powered CAD code retrieval and generation
- FastAPI backend with LangGraph orchestration
- Production-ready Docker deployment
- Modern dependency management (Poetry + Conda)

## Project Structure
```
backend/           # FastAPI, LangGraph, LLM, CAD endpoints
frontend/          # Cascade Studio static files
static/            # Exported models (STEP, STL)
docs/              # Documentation
Dockerfile         # Production build
docker-compose.yml # Development environment
environment.yml    # Conda environment for CadQuery
pyproject.toml     # Poetry configuration
setup.sh           # Automated setup script
```

## System Architecture

### LangGraph Nodes

The system uses intelligent routing to direct user queries to the most appropriate node:

| Node | Purpose | Trigger Keywords | Example Queries |
|------|---------|------------------|-----------------|
| **help** | General assistance and explanations | "what is", "how to", "explain", "help" | "What is parametric modeling?", "How to export models?" |
| **generate** | RAG-based model generation | "create", "make", "build", "design" | "Create a cylinder", "Make me a cube" |
| **code_gen** | RAG-assisted LLM code generation | "write code", "generate code", "custom" | "Write CADQuery code for a gear", "Generate custom code" |
| **create_cad** | Legacy CAD operations | Specific CAD requests | "Create a CAD model" |

### Key Features

- **🤖 Intelligent Routing**: Automatically determines the best node based on user intent
- **🔍 RAG Integration**: Retrieves existing CADQuery code from knowledge base
- **💻 RAG-Assisted Code Generation**: Creates custom CADQuery code using LLM with RAG examples
- **🎯 Model Execution**: Executes generated code to create real STEP models
- **📱 Frontend Integration**: Seamlessly loads generated models in CascadeStudio

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/yourusername/genx3D.git
cd genx3D
./setup.sh

# Setup LLM (optional but recommended)
python setup_llm.py
```

### Option 2: Manual Setup
1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/genx3D.git
   cd genx3D
   ```

2. **Install Poetry:**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Create conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate genx3d
   ```

4. **Install Python dependencies:**
   ```bash
   poetry install
   ```

5. **Setup LLM (optional but recommended):**
   ```bash
   python setup_llm.py
   ```

6. **Start the backend:**
   ```bash
   poetry run uvicorn backend.main:app --reload --port 8000
   ```

7. **Start the frontend:**
   ```bash
   cd frontend/CascadeStudio
   npm start  # or http-server .
   ```

### Option 3: Docker (Production)
```bash
# Using docker-compose (recommended)
docker-compose up --build

# Or using Docker directly
docker build -t genx3d .
docker run -d -p 8000:8000 genx3d
```

## Development

### Adding Dependencies
```bash
# Python dependencies (via Poetry)
poetry add package-name
poetry add --group dev package-name  # Development dependencies

# Conda dependencies
conda install package-name
conda env export > environment.yml  # Update environment file
```

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black backend/
poetry run flake8 backend/
```

### Testing Routing Logic
```bash
# Test the intelligent routing system
python test_routing.py

# Or test specific queries
python test_routing.py
# Then choose option 2 for interactive testing
```

### Testing Code Generation
```bash
# Test the RAG-assisted code generation
python test_rag_assisted_generation.py

# Test retry logic for code generation
python test_retry_logic.py

# Test basic code generation (legacy)
python test_code_generation.py

# Or test specific queries interactively
python test_rag_assisted_generation.py
# Then choose option 2 for interactive testing
```

## Dependency Management

This project uses a **hybrid approach**:
- **Conda**: For CadQuery and system-level dependencies
- **Poetry**: For Python package management

See [DEPENDENCY_MANAGEMENT.md](DEPENDENCY_MANAGEMENT.md) for detailed information.

## License
MIT (see LICENSE)

## Contact
For questions or contributions, open an issue or contact the maintainer. 