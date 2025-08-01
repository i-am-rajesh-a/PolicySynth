#!/bin/bash
set -euo pipefail

echo "🚀 Enhanced simple build process..."

# Show Python version
PYVER=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Detected Python version: $PYVER"

if [[ "$PYVER" == "3.13"* ]]; then
  echo "⚠️ Warning: Python 3.13 may not have prebuilt wheels for pydantic-core; build may fall back to source which requires Rust."
  echo "✅ Recommended: switch to Python 3.12.x to avoid this complication."
fi

# Upgrade pip to latest
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Prepare Rust/Cargo environment to avoid read-only filesystem issues if source build happens
export CARGO_HOME="$PWD/.cargo"
export CARGO_TARGET_DIR="$PWD/.cargo-target"
mkdir -p "$CARGO_HOME"
mkdir -p "$CARGO_TARGET_DIR"

# Minimal cargo config to reduce index pressure (optional but helpful)
mkdir -p .cargo
cat <<'EOF' > .cargo/config.toml
[registries.crates-io]
protocol = "sparse"
EOF

# Install Rust toolchain only if needed (i.e., if maturin/pydantic-core build is going to run)
# We'll check for presence of rustup; if not present, install it so source builds can succeed.
if ! command -v cargo >/dev/null 2>&1; then
  echo "🛠 Installing Rust toolchain (needed for building pydantic-core from source)..."
  # Non-interactive install
  curl https://sh.rustup.rs -sSf | sh -s -- -y
  # Source the environment for this shell
  source "$HOME/.cargo/env"
else
  echo "🛠 Rust toolchain already available."
fi

# Ensure rust binaries are on PATH (rustup default installs to $HOME/.cargo/bin)
export PATH="$HOME/.cargo/bin:$PATH"

# Install dependencies, preferring binaries but allowing fallback
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir --prefer-binary -r requirements.txt || {
  echo "⚠️ Initial install failed. Retrying with verbose output to diagnose..."
  pip install -vvv --no-cache-dir --prefer-binary -r requirements.txt
}

# Verify installation
echo "🔍 Verifying installation..."
python -c "import uvicorn; print('✅ uvicorn installed successfully')" || echo "❌ uvicorn import failed"
python -c "import fastapi; print('✅ fastapi installed successfully')" || echo "❌ fastapi import failed"
python -c "import pydantic; print('✅ pydantic installed successfully')" || echo "❌ pydantic import failed"

echo "✅ Simple build completed!"
