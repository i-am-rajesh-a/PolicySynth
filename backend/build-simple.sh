#!/bin/bash

# Simple build script as fallback
echo "🚀 Simple build process..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install --no-cache-dir --prefer-binary -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
python -c "import uvicorn; print('✅ uvicorn installed successfully')"
python -c "import fastapi; print('✅ fastapi installed successfully')"
python -c "import pydantic; print('✅ pydantic installed successfully')"

echo "✅ Simple build completed!" 