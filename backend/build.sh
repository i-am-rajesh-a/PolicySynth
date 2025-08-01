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
pip install --no-cache-dir setuptools==65.5.1 wheel==0.38.4

echo "📦 Installing Python dependencies..."

# Install dependencies with specific flags to avoid compilation issues
pip install --no-cache-dir --prefer-binary -r requirements.txt

echo "🧪 Testing deployment..."
python test_deployment.py

echo "✅ Build completed successfully!" 