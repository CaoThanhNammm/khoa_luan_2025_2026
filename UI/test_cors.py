#!/usr/bin/env python3
"""
Script to test CORS configuration
"""
import requests
import json

def test_cors():
    base_url = "http://localhost:8000"
    
    print("Testing CORS configuration...")
    
    # Test preflight request
    print("\n1. Testing preflight request (OPTIONS)...")
    try:
        response = requests.options(
            f"{base_url}/api/auth/register",
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        print(f"Preflight Status: {response.status_code}")
        print(f"Preflight Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"Preflight Error: {e}")
    
    # Test actual register request
    print("\n2. Testing register request (POST)...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com", 
                "password": "testpassword123"
            },
            headers={
                'Origin': 'http://localhost:5173',
                'Content-Type': 'application/json'
            }
        )
        print(f"Register Status: {response.status_code}")
        print(f"Register Headers: {dict(response.headers)}")
        print(f"Register Response: {response.text}")
    except Exception as e:
        print(f"Register Error: {e}")
    
    # Test health endpoint
    print("\n3. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
    except Exception as e:
        print(f"Health Error: {e}")

if __name__ == "__main__":
    test_cors()