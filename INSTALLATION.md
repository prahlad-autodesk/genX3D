# Installation Guide

This project supports multiple dependency management approaches. Choose the method that works best for your setup.

## Option 1: Poetry (Recommended)

Poetry is the primary dependency management tool for this project.

### Install Poetry
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Or via pip
pip install poetry
```

### Install Dependencies
```bash
# Install all dependencies
poetry install

# Install only production dependencies
poetry install --no-dev

# Activate the virtual environment
poetry shell
```

### Run the Application
```bash
# Start the backend server
poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Or use the script
poetry run start-backend

# Run cleanup tests
poetry run test-cleanup
```

## Option 2: Conda + Pip

Use conda for CadQuery and pip for Python packages.

### Create Conda Environment
```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Activate environment
conda activate genx3d
```

### Install Additional Dependencies
```bash
# Install remaining dependencies via pip
pip install -r requirements.txt

# Or install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy httpx
```

## Option 3: Pip Only

For users who prefer pip-only installation.

### Create Virtual Environment
```bash
# Create virtual environment
python -m venv genx3d-env

# Activate on Linux/Mac
source genx3d-env/bin/activate

# Activate on Windows
genx3d-env\Scripts\activate
```

### Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Note: CadQuery and OpenCascade need to be installed separately
# via conda or system packages
```

## Docker Installation

The easiest way to get started with all dependencies pre-configured.

### Build and Run
```bash
# Build the Docker image
docker build -t genx3d .

# Run the container
docker run -p 8000:8000 genx3d

# Or use docker-compose
docker-compose up
```

## Development Setup

### Install Development Dependencies
```bash
# With Poetry
poetry install --with dev

# With pip
pip install -r requirements.txt
```

### Code Quality Tools
```bash
# Format code
poetry run black backend/

# Lint code
poetry run flake8 backend/

# Type checking
poetry run mypy backend/

# Run tests
poetry run pytest
```

## Key Dependencies

### Core Dependencies
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **LangChain**: AI/LLM framework
- **LangGraph**: Workflow orchestration
- **CadQuery**: CAD modeling (via conda)

### RAG Dependencies
- **Sentence Transformers**: Text embeddings
- **Pinecone**: Vector database
- **FAISS**: Local vector search
- **Pandas**: Data manipulation

### Cleanup System Dependencies
- **Threading**: Background cleanup service
- **Pathlib**: File path management
- **Time**: Timestamp tracking

## Troubleshooting

### CadQuery Installation Issues
```bash
# Ensure conda-forge channel is available
conda config --add channels conda-forge

# Install CadQuery
conda install -c conda-forge cadquery
```

### Poetry Issues
```bash
# Clear Poetry cache
poetry cache clear . --all

# Reinstall dependencies
poetry install --sync
```

### Port Conflicts
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
poetry run uvicorn backend.main:app --port 8001
```

## Environment Variables

Create a `.env` file in the project root:

```env
# LLM API Keys (choose one)
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
ANTHROPIC_API_KEY=your_anthropic_key

# Pinecone
PINECONE_API_KEY=your_pinecone_key

# Optional: Use local Ollama
USE_OLLAMA=true
```

## Verification

After installation, verify everything works:

```bash
# Check cleanup system
curl http://localhost:8000/cleanup/stats

# Test API
curl http://localhost:8000/health

# Run tests
poetry run test-cleanup
``` 