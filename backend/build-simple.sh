#!/bin/bash

# Simple build script as fallback
echo "🚀 Simple build process..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install --no-cache-dir --prefer-binary -r requirements.txt

echo "✅ Simple build completed!" 