#!/usr/bin/env python3
"""
Quick start script for Student LLM Assistant
This script starts both the backend and frontend servers.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

def run_command(command, cwd=None, shell=False):
    """Run a command and return the process"""
    try:
        if shell:
            process = subprocess.Popen(command, shell=True, cwd=cwd)
        else:
            process = subprocess.Popen(command, cwd=cwd)
        return process
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 Starting Student LLM Assistant...")
    print("=" * 50)
    
    # Check if Ollama is running
    if not check_ollama():
        print("⚠️  Warning: Ollama is not running or not accessible")
        print("   Please start Ollama first: ollama serve")
        print("   Then pull a model: ollama pull llama2:7b")
        print()
    
    # Get current directory
    current_dir = Path.cwd()
    backend_dir = current_dir / "backend"
    frontend_dir = current_dir / "frontend"
    
    # Check if directories exist
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    processes = []
    
    try:
        # Start backend
        print("🔧 Starting FastAPI backend...")
        if os.name == 'nt':  # Windows
            backend_process = run_command(
                ["venv\\Scripts\\python.exe", "main.py"], 
                cwd=backend_dir
            )
        else:  # Unix/Linux/Mac
            backend_process = run_command(
                ["./venv/bin/python", "main.py"], 
                cwd=backend_dir
            )
        
        if backend_process:
            processes.append(("Backend", backend_process))
            print("✅ Backend started")
        else:
            print("❌ Failed to start backend")
            return False
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Start frontend
        print("🎨 Starting React frontend...")
        frontend_process = run_command(["npm", "run", "dev"], cwd=frontend_dir)
        
        if frontend_process:
            processes.append(("Frontend", frontend_process))
            print("✅ Frontend started")
        else:
            print("❌ Failed to start frontend")
            return False
        
        print("\n🎉 Student LLM Assistant is running!")
        print("=" * 50)
        print("📱 Frontend: http://localhost:5173")
        print("🔧 Backend:  http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop all services")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...")
        
        # Stop all processes
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️  {name} force stopped")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
        
        print("\n👋 Goodbye!")
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 