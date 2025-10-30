# Docker Setup with Conda Environment

## Overview

This Dockerfile creates a containerized environment that properly integrates:
- **Conda** for CadQuery and scientific computing dependencies
- **Poetry** for Python package management
- **FastAPI** for the web application
- **Cleanup service** for temp file management

## Key Features

✅ **Proper Conda Environment Integration**  
✅ **CadQuery Support** via conda-forge  
✅ **Poetry Package Management**  
✅ **Multi-stage Optimization**  
✅ **Health Checks**  
✅ **Temp Models Cleanup**  

## Dockerfile Structure

### Base Image
```dockerfile
FROM continuumio/miniconda3:latest
```
- Uses official Miniconda3 image
- Provides conda package manager
- Includes Python and essential tools

### System Dependencies
```dockerfile
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```
- **curl**: Health checks and API testing
- **git**: Package installation and version control
- **build-essential**: Compilation tools for native extensions

### Conda Environment Setup
```dockerfile
# Copy conda environment file
COPY environment.yml .

# Create conda environment and activate it
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "genx3d", "/bin/bash", "-c"]
```

### Poetry Integration
```dockerfile
# Install Poetry in the conda environment
RUN pip install poetry

# Install Python dependencies with Poetry in the conda environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
```

## Environment Configuration

### Conda Environment (`environment.yml`)
```yaml
name: genx3d
channels:
  - conda-forge
  - cadquery
dependencies:
  - python=3.11
  - cadquery
  - pip
  - pip:
    - fastapi>=0.104.0
    - uvicorn[standard]>=0.24.0
    - langchain>=0.1.0
    - langchain-openai>=0.0.5
    - langchain-core>=0.1.0
    - langgraph>=0.0.20
    - sentence-transformers>=2.2.2
    - pinecone-client>=2.2.4
    - pinecone>=7.3.0
    - pydantic>=2.5.0
    - jinja2>=3.1.0
    - aiofiles>=23.0.0
    - python-dotenv>=1.0.0
```

### Environment Variables
```dockerfile
ENV CONDA_DEFAULT_ENV=genx3d
ENV PATH="/opt/conda/envs/genx3d/bin:$PATH"
```

## Building and Running

### Build the Image
```bash
# Build with tag
docker build -t genx3d .

# Build with specific platform
docker build --platform linux/amd64 -t genx3d .

# Build with no cache (for debugging)
docker build --no-cache -t genx3d .
```

### Run the Container
```bash
# Basic run
docker run -p 8000:8000 genx3d

# Run with environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
  genx3d

# Run with volume mounts
docker run -p 8000:8000 \
  -v $(pwd)/temp_models:/app/backend/temp_models \
  -v $(pwd)/.env:/app/.env \
  genx3d
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  genx3d:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
    volumes:
      - ./temp_models:/app/backend/temp_models
      - ./.env:/app/.env
    healthcheck:
      test: ["CMD", "conda", "run", "-n", "genx3d", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Verification Steps

### Check Conda Environment
```bash
# Enter container
docker exec -it <container_id> bash

# Check conda environment
conda env list

# Activate environment
conda activate genx3d

# Verify CadQuery
python -c "import cadquery as cq; print(cq.__version__)"
```

### Check Application
```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/api/info

# Cleanup stats
curl http://localhost:8000/cleanup/stats
```

## Troubleshooting

### Common Issues

#### 1. CadQuery Not Found
```bash
# Check if conda environment is active
conda info --envs

# Reinstall CadQuery
conda install -c conda-forge cadquery
```

#### 2. Poetry Dependencies
```bash
# Check Poetry environment
poetry env info

# Reinstall dependencies
poetry install --sync
```

#### 3. Port Conflicts
```bash
# Check if port is in use
docker ps

# Use different port
docker run -p 8001:8000 genx3d
```

#### 4. Build Failures
```bash
# Clean build
docker system prune -a
docker build --no-cache -t genx3d .
```

### Debug Mode
```bash
# Run with interactive shell
docker run -it --entrypoint /bin/bash genx3d

# Check environment
conda activate genx3d
python -c "import sys; print(sys.path)"
```

## Performance Optimization

### Multi-stage Build (Optional)
```dockerfile
# Build stage
FROM continuumio/miniconda3:latest as builder
# ... build dependencies

# Runtime stage
FROM continuumio/miniconda3:latest
# ... copy from builder
```

### Layer Optimization
- Copy dependency files first
- Install dependencies before copying code
- Use .dockerignore to exclude unnecessary files

## Security Considerations

### Non-root User
```dockerfile
# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser
```

### Environment Variables
- Use .env files for sensitive data
- Don't hardcode API keys in Dockerfile
- Use Docker secrets for production

## Monitoring

### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD conda run -n genx3d curl -f http://localhost:8000/health || exit 1
```

### Logs
```bash
# View logs
docker logs <container_id>

# Follow logs
docker logs -f <container_id>
```

## Production Deployment

### Environment Variables
```bash
# Production .env
OPENAI_API_KEY=your_production_key
PINECONE_API_KEY=your_production_key
GROQ_API_KEY=your_production_key
```

### Resource Limits
```bash
docker run -p 8000:8000 \
  --memory=2g \
  --cpus=2 \
  genx3d
```

### Reverse Proxy
```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
``` 