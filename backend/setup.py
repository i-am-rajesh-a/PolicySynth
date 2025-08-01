#!/usr/bin/env python3
"""
Setup script for Policy Pundit Backend
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🎯 Policy Pundit Backend Setup")
    print("=" * 40)
    
    # Check if we're in the backend directory
    if not Path("app").exists():
        print("❌ Please run this script from the backend directory")
        sys.exit(1)
    
    # Step 1: Install basic requirements
    print("\n📦 Installing basic dependencies...")
    if not run_command("pip install -r requirements-basic.txt", "Installing basic requirements"):
        print("❌ Failed to install basic requirements")
        sys.exit(1)
    
    # Step 2: Try to install FAISS (optional)
    print("\n🔍 Attempting to install FAISS...")
    faiss_success = run_command("pip install faiss-cpu==1.7.2", "Installing FAISS")
    
    if not faiss_success:
        print("⚠️ FAISS installation failed. Using simplified embedder.")
        print("The backend will work with basic functionality.")
    
    # Step 3: Test the server
    print("\n🧪 Testing server startup...")
    try:
        # Test import
        import uvicorn
        from app.main import app
        print("✅ All imports successful")
        
        print("\n🚀 Starting server for testing...")
        print("Press Ctrl+C to stop the test server")
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check your installation")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n✅ Server test completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start the backend: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("2. Start the frontend: cd ../frontend && npm run dev")
        print("3. Open http://localhost:5173 in your browser")

if __name__ == "__main__":
    main() 