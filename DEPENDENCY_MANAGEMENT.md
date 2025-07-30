# Dependency Management for GenX3D

This project uses a **hybrid approach** combining **Conda** (for CadQuery) and **Poetry** (for Python dependencies) to manage dependencies effectively.

## Why This Approach?

- **CadQuery** requires conda and cannot be installed via pip
- **Poetry** provides better dependency management for Python packages
- **Hybrid approach** gives us the best of both worlds

## Setup Instructions

### 1. Install Poetry (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Create Conda Environment
```bash
# Create conda environment with CadQuery
conda env create -f environment.yml

# Activate the environment
conda activate genx3d
```

### 3. Install Python Dependencies with Poetry
```bash
# Install dependencies from pyproject.toml
poetry install

# Or install in development mode
poetry install --with dev
```

### 4. Verify Installation
```bash
# Check if CadQuery is available
python -c "import cadquery as cq; print('✅ CadQuery available')"

# Check if other dependencies are available
python -c "import fastapi, langchain, pinecone; print('✅ All dependencies available')"
```

## Development Workflow

### Starting the Backend
```bash
# Option 1: Using Poetry
poetry run uvicorn backend.main:app --reload --port 8000

# Option 2: Using conda environment directly
conda activate genx3d
uvicorn backend.main:app --reload --port 8000
```

### Adding New Dependencies

#### Python Dependencies (via Poetry)
```bash
# Add production dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name

# Update dependencies
poetry update
```

#### Conda Dependencies
```bash
# Add conda dependency
conda install package-name

# Update environment.yml
conda env export > environment.yml
```

## Project Structure

```
x3D/
├── pyproject.toml          # Poetry configuration
├── environment.yml         # Conda environment
├── poetry.lock            # Poetry lock file (auto-generated)
├── backend/
│   ├── requirements.txt   # Legacy requirements (can be removed)
│   └── ...
└── ...
```

## Deployment Considerations

### Local Development
- Use conda environment + Poetry
- All dependencies managed automatically

### Production Deployment
- **Option A**: Use conda environment in production
- **Option B**: Use Docker with conda base image
- **Option C**: Use cloud platforms that support conda

### Docker Example
```dockerfile
FROM continuumio/miniconda3:latest

# Install conda dependencies
COPY environment.yml .
RUN conda env create -f environment.yml

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy application code
COPY backend/ ./backend/

# Activate conda environment and run
SHELL ["conda", "run", "-n", "genx3d", "/bin/bash", "-c"]
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Poetry Not Found
```bash
# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Conda Environment Issues
```bash
# Recreate environment
conda env remove -n genx3d
conda env create -f environment.yml
```

### Dependency Conflicts
```bash
# Update Poetry lock file
poetry lock --no-update

# Update all dependencies
poetry update
```

## Benefits of This Approach

1. **✅ CadQuery Support**: Works with conda-only packages
2. **✅ Modern Dependency Management**: Poetry's lock file ensures reproducibility
3. **✅ Development Experience**: Better dependency resolution and virtual environments
4. **✅ Deployment Ready**: Can be containerized or deployed to cloud platforms
5. **✅ Team Collaboration**: Clear dependency specifications for all team members

## Migration from Current Setup

If you're currently using just conda or just pip:

1. **Backup current environment**:
   ```bash
   conda env export > environment_backup.yml
   pip freeze > requirements_backup.txt
   ```

2. **Follow setup instructions above**

3. **Test thoroughly** before removing old dependency files

4. **Update team documentation** with new setup process 