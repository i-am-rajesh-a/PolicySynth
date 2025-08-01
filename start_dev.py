#!/usr/bin/env python3
"""
Development startup script for Policy Pundit
Starts both frontend and backend servers
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def run_command(command, cwd=None, name="Process"):
    """Run a command and handle output"""
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print(f"🚀 Started {name} (PID: {process.pid})")
        
        # Stream output
        for line in process.stdout:
            print(f"[{name}] {line.rstrip()}")
        
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    print("🎯 Policy Pundit Development Server")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    processes = []
    
    try:
        # Start backend
        print("\n🔧 Starting Backend Server...")
        backend_process = run_command(
            "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000",
            cwd="backend",
            name="Backend"
        )
        if backend_process:
            processes.append(backend_process)
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend
        print("\n🎨 Starting Frontend Server...")
        frontend_process = run_command(
            "npm run dev",
            cwd="frontend",
            name="Frontend"
        )
        if frontend_process:
            processes.append(frontend_process)
        
        print("\n✅ Development servers started!")
        print("📱 Frontend: http://localhost:5173")
        print("🔧 Backend: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop all servers")
        
        # Wait for processes
        for process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping development servers...")
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("✅ All servers stopped")

if __name__ == "__main__":
    main() 