#!/usr/bin/env python3
"""
Simple test for optimized server
"""

import requests
import time
import json

def test_simple():
    """Simple test"""
    print("🧪 Testing Optimized Server...")
    
    # Test health check
    try:
        print("📡 Testing health check...")
        response = requests.get("http://127.0.0.1:5001/api/health/optimized")
        if response.status_code == 200:
            print("✅ Health check passed")
            data = response.json()
            print(f"Status: {data.get('status')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test chat
    try:
        print("\n💬 Testing optimized chat...")
        question = "Thông tin về học phí đại học"
        
        start_time = time.time()
        response = requests.post(
            "http://127.0.0.1:5001/api/chat/optimized",
            json={"message": question},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat response received in {end_time - start_time:.2f}s")
            print(f"📝 Answer: {data.get('answer', '')[:200]}...")
            print(f"⚡ Optimizations: {data.get('optimizations_used', {})}")
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
    
    # Test metrics
    try:
        print("\n📊 Testing metrics...")
        response = requests.get("http://127.0.0.1:5001/api/metrics/performance")
        if response.status_code == 200:
            data = response.json()
            print("✅ Metrics retrieved")
            metrics = data.get('metrics', {})
            print(f"Performance data: {json.dumps(metrics, indent=2)}")
        else:
            print(f"❌ Metrics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Metrics error: {e}")

if __name__ == "__main__":
    test_simple()
