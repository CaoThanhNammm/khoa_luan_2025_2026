#!/usr/bin/env python3
"""
Script to start both frontend and backend for development
"""
import os
import sys
import subprocess
import threading
import time

def start_backend():
    """Start the FastAPI backend"""
    backend_dir = "d:/PycharmProjects/UI/chat-backend/be"
    os.chdir(backend_dir)
    
    print("🚀 Starting FastAPI backend on http://localhost:8000")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except Exception as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start the React frontend"""
    frontend_dir = "d:/PycharmProjects/UI/chatbot-frontend"
    os.chdir(frontend_dir)
    
    print("🚀 Starting React frontend on http://localhost:5173")
    try:
        subprocess.run(["npm", "run", "dev"], check=True, shell=True)
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    print("🔧 Starting development environment...")
    print("📋 Make sure you have:")
    print("   - Installed Python dependencies: pip install -r chat-backend/be/requirements.txt")
    print("   - Installed Node dependencies: cd chatbot-frontend && npm install")
    print("   - MySQL server running (if using database)")
    print("-" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Development servers stopped by user")

if __name__ == "__main__":
    main()