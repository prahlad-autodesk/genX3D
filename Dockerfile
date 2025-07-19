FROM mambaorg/micromamba:1.5.7

# Set workdir
WORKDIR /app

# Install system dependencies (graphics libs, Node.js, npm)
USER root
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    gnupg \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Switch to mamba user
USER $MAMBA_USER

# Copy environment and backend files
COPY environment.yml ./
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY backend/static/ ./static/

# Copy CascadeStudio app with node_modules
COPY frontend/CascadeStudio/ /app/frontend/CascadeStudio/
# Copy local node_modules into the image
COPY frontend/CascadeStudio/node_modules /app/frontend/CascadeStudio/node_modules

# --- Frontend: Build CascadeStudio (no npm install) ---
USER root
WORKDIR /app/frontend/CascadeStudio

# No npm install - just copy the files
COPY frontend/CascadeStudio/ ./
RUN npm run build || echo "Build failed but continuing..."

# --- Backend: Conda setup ---
USER $MAMBA_USER
WORKDIR /app

RUN micromamba env create -f environment.yml -n genx3d
ENV MAMBA_DOCKERFILE_ACTIVATE=1
ENV CONDA_DEFAULT_ENV=genx3d
ENV PATH=/opt/conda/envs/genx3d/bin:$PATH

# --- Expose API port ---
EXPOSE 8000

# --- Start FastAPI backend using Gunicorn ---
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "backend.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
