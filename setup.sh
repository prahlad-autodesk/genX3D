#!/bin/bash

# GenX3D Setup Script
# This script sets up the hybrid Poetry + Conda environment

set -e  # Exit on any error

echo "🚀 Setting up GenX3D with Poetry + Conda..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    print_error "Conda is not installed. Please install Miniconda or Anaconda first."
    print_status "Visit: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    print_warning "Poetry is not installed. Installing now..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    print_success "Poetry installed successfully"
else
    print_success "Poetry is already installed"
fi

# Create conda environment
print_status "Creating conda environment 'genx3d'..."
if conda env list | grep -q "genx3d"; then
    print_warning "Conda environment 'genx3d' already exists. Removing it..."
    conda env remove -n genx3d -y
fi

conda env create -f environment.yml
print_success "Conda environment created successfully"

# Activate conda environment
print_status "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate genx3d

# Install Poetry dependencies
print_status "Installing Python dependencies with Poetry..."
poetry install

# Verify installation
print_status "Verifying installation..."

# Test CadQuery
if python -c "import cadquery as cq; print('CadQuery version:', cq.__version__)" 2>/dev/null; then
    print_success "CadQuery is working correctly"
else
    print_error "CadQuery installation failed"
    exit 1
fi

# Test other dependencies
if python -c "import fastapi, langchain, pinecone; print('All dependencies available')" 2>/dev/null; then
    print_success "All Python dependencies are working correctly"
else
    print_error "Some Python dependencies failed to install"
    exit 1
fi

print_success "🎉 Setup completed successfully!"

echo ""
echo "📋 Next steps:"
echo "1. Activate the environment: conda activate genx3d"
echo "2. Start the backend: poetry run uvicorn backend.main:app --reload --port 8000"
echo "3. Start the frontend: cd frontend/CascadeStudio && npm start"
echo ""
echo "📚 For more information, see DEPENDENCY_MANAGEMENT.md"
echo "" 