#!/bin/bash

# Build script for Policy Pundit backend
# This script handles Rust compilation issues in containerized environments

set -e

echo "🚀 Starting build process..."

# Set up Rust environment variables for temporary directories
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup
export CARGO_TARGET_DIR=/tmp/target

# Create necessary directories
mkdir -p $CARGO_HOME
mkdir -p $RUSTUP_HOME
mkdir -p $CARGO_TARGET_DIR

echo "📦 Upgrading pip and installing build tools..."

# Upgrade pip first
pip install --upgrade pip

# Install build tools first
pip install --no-cache-dir setuptools==69.0.0 wheel==0.42.0

echo "📦 Installing Python dependencies..."

# Try different requirements files in order of preference
REQUIREMENTS_FILES=("requirements-python313.txt" "requirements.txt" "requirements-minimal.txt")

for req_file in "${REQUIREMENTS_FILES[@]}"; do
    if [ -f "$req_file" ]; then
        echo "🔄 Trying to install from $req_file..."
        if pip install --no-cache-dir --prefer-binary -r "$req_file"; then
            echo "✅ Successfully installed dependencies from $req_file"
            break
        else
            echo "❌ Failed to install from $req_file, trying next..."
        fi
    fi
done

echo "🔍 Verifying installation..."
python -c "import uvicorn; print('✅ uvicorn installed successfully')"
python -c "import fastapi; print('✅ fastapi installed successfully')"
python -c "import pydantic; print('✅ pydantic installed successfully')"

echo "🧪 Testing deployment..."
python test_deployment.py

echo "✅ Build completed successfully!" 