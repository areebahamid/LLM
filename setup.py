#!/usr/bin/env python3
"""
Setup script for Student LLM Assistant
This script helps you get started with the project by setting up the environment
and installing dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=False):
    """Run a command and return the result"""
    try:
        if shell:
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        else:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    success, stdout, stderr = run_command(["node", "--version"])
    if not success:
        print("❌ Node.js is not installed or not in PATH")
        print("Please install Node.js from https://nodejs.org/")
        return False
    
    version_str = stdout.strip().replace('v', '')
    print(f"✅ Node.js {version_str} detected (using existing installation)")
    return True

def setup_backend():
    """Setup the FastAPI backend"""
    print("\n🔧 Setting up Backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    print("Creating virtual environment...")
    success, stdout, stderr = run_command([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
    if not success:
        print(f"❌ Failed to create virtual environment: {stderr}")
        return False
    
    # Determine activation script
    if platform.system() == "Windows":
        activate_script = backend_dir / "venv" / "Scripts" / "activate.bat"
        pip_path = backend_dir / "venv" / "Scripts" / "pip.exe"
    else:
        activate_script = backend_dir / "venv" / "bin" / "activate"
        pip_path = backend_dir / "venv" / "bin" / "pip"
    
    # Install dependencies
    print("Installing Python dependencies...")
    success, stdout, stderr = run_command([str(pip_path), "install", "-r", "requirements.txt"], cwd=backend_dir)
    if not success:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    env_example = backend_dir / "env.example"
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file (please review and modify as needed)")
    
    # Create data directories
    data_dir = backend_dir / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "uploads").mkdir(exist_ok=True)
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Setup the React frontend"""
    print("\n🔧 Setting up Frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    success, stdout, stderr = run_command(["npm", "install"], cwd=frontend_dir)
    if not success:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False
    
    # Create .env file if it doesn't exist
    env_file = frontend_dir / ".env"
    env_example = frontend_dir / "env.example"
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file")
    
    print("✅ Frontend setup complete!")
    return True

def initialize_knowledge_base():
    """Initialize the knowledge base with sample data"""
    print("\n📚 Initializing Knowledge Base...")
    
    backend_dir = Path("backend")
    script_path = backend_dir / "scripts" / "initialize_kb.py"
    
    if not script_path.exists():
        print("❌ Knowledge base initialization script not found")
        return False
    
    # Determine Python path
    if platform.system() == "Windows":
        python_path = backend_dir / "venv" / "Scripts" / "python.exe"
    else:
        python_path = backend_dir / "venv" / "bin" / "python"
    
    success, stdout, stderr = run_command([str(python_path), str(script_path)], cwd=backend_dir)
    if not success:
        print(f"❌ Failed to initialize knowledge base: {stderr}")
        return False
    
    print("✅ Knowledge base initialized!")
    return True

def main():
    """Main setup function"""
    print("🚀 Student LLM Assistant Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_node_version():
        return False
    
    # Setup backend
    if not setup_backend():
        return False
    
    # Setup frontend
    if not setup_frontend():
        return False
    
    # Initialize knowledge base
    if not initialize_knowledge_base():
        print("⚠️  Knowledge base initialization failed, but you can continue")
    
    print("\n🎉 Setup Complete!")
    print("=" * 40)
    print("\nNext steps:")
    print("1. Install Ollama from https://ollama.ai/")
    print("2. Pull a model: ollama pull llama2:7b")
    print("3. Start the backend: cd backend && python main.py")
    print("4. Start the frontend: cd frontend && npm run dev")
    print("5. Open http://localhost:5173 in your browser")
    print("\nFor more information, see the README.md file")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 