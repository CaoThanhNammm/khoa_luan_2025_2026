#!/usr/bin/env python3
"""
Script to start the backend with proper CORS configuration
"""
import os
import sys
import subprocess

def start_backend():
    # Change to backend directory
    backend_dir = "d:/PycharmProjects/UI/chat-backend/be"
    os.chdir(backend_dir)
    
    print(f"Starting backend from: {backend_dir}")
    print("Make sure you have installed requirements: pip install -r requirements.txt")
    print("Starting server on http://localhost:8000")
    print("CORS enabled for: http://localhost:5173, http://localhost:3000")
    print("-" * 50)
    
    # Start the server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    start_backend()