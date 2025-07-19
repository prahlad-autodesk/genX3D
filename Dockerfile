# Use micromamba for fast conda env setup
FROM mambaorg/micromamba:1.5.7

# Set work directory
WORKDIR /app

# Switch to root to install system packages
USER root
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Copy environment and source code
COPY environment.yml ./
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create conda environment
RUN micromamba env create -f environment.yml -n genx3d

# Activate environment and set as default
ENV MAMBA_DOCKERFILE_ACTIVATE=1
ENV CONDA_DEFAULT_ENV=genx3d
ENV PATH=/opt/conda/envs/genx3d/bin:$PATH

# Expose port
EXPOSE 8000

# Start the app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "backend.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"] 