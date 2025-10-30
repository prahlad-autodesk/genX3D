########################
# 1️⃣ Builder Stage
########################
FROM mambaorg/micromamba:1.5.8 AS builder

WORKDIR /app

# Install only what's needed for CadQuery/OpenCascade
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglu1-mesa \
    libxrender1 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Create conda env
COPY environment.yml /tmp/environment.yml
RUN micromamba create -y -n genx3d -f /tmp/environment.yml -c conda-forge \
    && micromamba install -y -n genx3d -c conda-forge cadquery pip \
    && micromamba clean --all --yes

ENV PATH="/opt/conda/envs/genx3d/bin:$PATH"

# Install Poetry in env
RUN pip install --no-cache-dir poetry

# Copy only poetry files for cache
COPY pyproject.toml poetry.lock* ./

# Install dependencies (no dev)
RUN poetry config virtualenvs.create false \
 && pip uninstall -y pinecone pinecone-client || true \
 && (poetry install --only main --no-root --no-interaction --no-ansi \
     || (poetry lock --no-update && poetry install --only main --no-root --no-interaction --no-ansi)) \
 && pip install --no-cache-dir "ezdxf==0.17.2"

# Copy full app
COPY backend/ backend/
COPY frontend-react/build/ frontend-react/build/
COPY frontend/CascadeStudio/ frontend/CascadeStudio/

# Prepare runtime dir
RUN mkdir -p backend/temp_models && chmod 755 backend/temp_models

########################
# 2️⃣ Runtime Stage
########################
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install only runtime OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglu1-mesa \
    libxrender1 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python env from builder
COPY --from=builder /opt/conda/envs/genx3d /opt/conda/envs/genx3d

ENV PATH="/opt/conda/envs/genx3d/bin:$PATH"
ENV PYTHONPATH="/app/backend"

# Copy only final app files from builder
COPY --from=builder /app/backend /app/backend
COPY --from=builder /app/frontend-react/build /app/frontend-react/build
COPY --from=builder /app/frontend/CascadeStudio /app/frontend/CascadeStudio

# Expose and healthcheck
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
