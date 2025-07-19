FROM mambaorg/micromamba:1.5.7

WORKDIR /app

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Copy files
COPY environment.yml ./
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Setup conda env
RUN micromamba env create -f environment.yml -n genx3d
ENV MAMBA_DOCKERFILE_ACTIVATE=1
ENV CONDA_DEFAULT_ENV=genx3d
ENV PATH=/opt/conda/envs/genx3d/bin:$PATH

# Expose Render port
EXPOSE 8000

# Start FastAPI app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "backend.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
