---
sidebar_position: 1
---

# Installation Guide

This guide will help you install and set up genx3D on your system.

## Prerequisites

Before installing genx3D, make sure you have the following:

- **Docker** (recommended for production)
- **Git** for cloning the repository
- **API Key** from OpenRouter for AI features

## Quick Installation with Docker

The easiest way to get started with genx3D is using Docker:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/genx3D.git
cd genx3D
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your OpenRouter API key to the `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### 3. Build and Run with Docker

```bash
# Build the Docker image
docker build -t genx3d .

# Run the container
docker run -d --env-file .env -p 8000:8000 genx3d
```

### 4. Access the Application

Open your browser and navigate to:
- **Main App**: [http://localhost:8000/app/](http://localhost:8000/app/)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Local Development Installation

If you prefer to run genx3D locally for development:

### 1. Install Conda/Mamba

Install [mamba](https://github.com/mamba-org/mamba) (recommended) or [conda](https://docs.conda.io/en/latest/miniconda.html):

```bash
# Install mamba (recommended)
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

### 2. Create Environment

```bash
# Using mamba (recommended)
mamba env create -f environment.yml
mamba activate genx3d

# Or using conda
conda env create -f environment.yml
conda activate genx3d
```

### 3. Set Up Environment Variables

Create a `.env` file as described in the Docker section above.

### 4. Run the Application

```bash
# Start the development server
uvicorn backend.main:app --reload
```

## Verification

To verify your installation:

1. **Check the API**: Visit [http://localhost:8000/docs](http://localhost:8000/docs)
2. **Test the CAD Interface**: Visit [http://localhost:8000/app/](http://localhost:8000/app/)
3. **Verify AI Features**: Try the chat assistant in the web interface

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process or use a different port
uvicorn backend.main:app --reload --port 8001
```

**Docker Build Fails**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t genx3d .
```

**Environment Issues**
```bash
# Verify environment is activated
conda info --envs

# Reinstall environment
conda env remove -n genx3d
conda env create -f environment.yml
```

## Next Steps

Now that you have genx3D installed, check out:

- [Quick Start Guide](./quick-start) - Get up and running in minutes
- [Configuration Guide](./configuration) - Customize your setup
- [API Documentation](../api/endpoints) - Learn about available endpoints

## Support

If you encounter any issues:

- 📖 Check the [troubleshooting section](#troubleshooting)
- 🐛 [Report an issue](https://github.com/yourusername/genx3D/issues)
- 💬 [Join discussions](https://github.com/yourusername/genx3D/discussions) 