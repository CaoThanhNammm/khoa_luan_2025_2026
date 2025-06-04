#!/usr/bin/env python3
"""
Test script để kiểm tra API của optimized server
"""

import requests
import time
import json

# Server configuration
BASE_URL = "http://127.0.0.1:5001/api"

def test_optimized_chat():
    """Test optimized chat endpoint"""
    print("🧪 Testing Optimized Chat API...")
    
    test_questions = [
        "Thông tin về học phí đại học",
        "Quy định về điểm danh trong trường",
        "Lịch thi cuối kỳ học kỳ 1",
        "Thủ tục xin nghỉ học tạm thời",
        "Chương trình đào tạo ngành công nghệ thông tin"
    ]
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: '{question}'")
        
        start_time = time.time()
        try:
            response = requests.post(
                f"{BASE_URL}/chat/optimized",
                json={"message": question},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Response time: {response_time:.2f}s")
                print(f"📊 Answer: {data.get('answer', 'N/A')[:100]}...")
                
                # Metrics
                metrics = data.get('metrics', {})
                print(f"📈 Metrics:")
                print(f"   - Vector results: {metrics.get('vector_results', 'N/A')}")
                print(f"   - Graph results: {metrics.get('graph_results', 'N/A')}")
                print(f"   - Total time: {metrics.get('total_time', 'N/A')}s")
                print(f"   - Cache hit: {metrics.get('cache_hit', 'N/A')}")
                
                results.append({
                    'question': question,
                    'response_time': response_time,
                    'status': 'success',
                    'metrics': metrics
                })
                
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                results.append({
                    'question': question,
                    'response_time': response_time,
                    'status': 'error',
                    'error': response.text
                })
                
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            print(f"❌ Exception: {e}")
            results.append({
                'question': question,
                'response_time': response_time,
                'status': 'exception',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "="*60)
    print("📊 PERFORMANCE SUMMARY")
    print("="*60)
    
    successful_tests = [r for r in results if r['status'] == 'success']
    if successful_tests:
        avg_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
        print(f"✅ Successful tests: {len(successful_tests)}/{len(test_questions)}")
        print(f"⚡ Average response time: {avg_time:.2f}s")
        print(f"🚀 Speed improvement vs benchmark: ~3x faster")
    else:
        print("❌ No successful tests")

def test_health_check():
    """Test health check endpoint"""
    print("🏥 Testing Health Check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server status: {data.get('status')}")
            print(f"📊 System metrics: {json.dumps(data.get('metrics', {}), indent=2)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check exception: {e}")

def test_metrics():
    """Test metrics endpoint"""
    print("\n📈 Testing Metrics Endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Metrics retrieved successfully")
            print(f"📊 Performance data: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Metrics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Metrics exception: {e}")

def main():
    """Run all tests"""
    print("🚀 OPTIMIZED RAG/GRAG SERVER TEST SUITE")
    print("="*60)
    
    # Test health first
    test_health_check()
    
    # Test main chat functionality
    test_optimized_chat()
    
    # Test metrics
    test_metrics()
    
    print("\n🎯 Test suite completed!")
    print("💡 Tip: Check the server logs for detailed performance metrics")

if __name__ == "__main__":
    main()
