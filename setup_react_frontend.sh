#!/bin/bash

# genx3D React Frontend Setup Script
# This script sets up the React frontend for the genx3D application

set -e

echo "🚀 Setting up genx3D React Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16 or higher is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Navigate to React frontend directory
cd frontend-react

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
EOF
    echo "✅ Created .env file"
fi

# Build the application
echo "🔨 Building the application..."
npm run build

echo "✅ React frontend setup complete!"
echo ""
echo "🎯 To start the React frontend:"
echo "   cd frontend-react"
echo "   npm start"
echo ""
echo "🌐 The application will be available at: http://localhost:3000"
echo ""
echo "💡 Make sure the backend is running on port 8000 before using the frontend." 