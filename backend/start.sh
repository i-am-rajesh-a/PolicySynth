#!/bin/bash

# Start script with debugging
echo "🚀 Starting Policy Pundit backend..."

# Check Python environment
echo "🔍 Python environment:"
which python
python --version

# Check if uvicorn is available
echo "🔍 Checking uvicorn availability:"
python -c "import uvicorn; print('✅ uvicorn found')" || echo "❌ uvicorn not found"

# List installed packages
echo "🔍 Installed packages:"
pip list | grep -E "(uvicorn|fastapi|pydantic)"

# Start the application
echo "🚀 Starting uvicorn server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT 