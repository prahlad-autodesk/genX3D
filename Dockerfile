# Use conda base image for CadQuery support
FROM continuumio/miniconda3:latest

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy conda environment file
COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Install Poetry
RUN pip install poetry

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Copy application code
COPY backend/ ./backend/

# Copy frontend with custom node_modules (these contain unique packages not available on npm)
COPY frontend/ ./frontend/

# Set environment variables
ENV CONDA_DEFAULT_ENV=genx3d
ENV PATH="/opt/conda/envs/genx3d/bin:$PATH"

# Install Python dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Create temp_models directory
RUN mkdir -p backend/temp_models

# Verify frontend node_modules are present (these contain custom packages)
RUN ls -la frontend/CascadeStudio/node_modules/ || echo "Warning: node_modules not found"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
