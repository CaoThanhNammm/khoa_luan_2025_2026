"""
Tích hợp hệ thống tối ưu hóa vào Flask backend
"""

import asyncio
import time
import logging
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, List
import traceback

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import optimized components
from optimization.OptimizedChat import OptimizedChat, RetrievalConfig
from optimization.config import load_config_from_env, get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
load_config_from_env()
config = get_config()

# Try to use fallback config if needed
try:
    from optimization.fallback_config import get_fallback_config
    # This is just to check if we might need fallbacks later
    logger.info("Fallback configuration is available if needed")
except ImportError:
    logger.warning("Fallback configuration is not available")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Global optimized chat instance
optimized_chat = None

def initialize_optimized_system():
    """Initialize optimized chat system"""
    global optimized_chat, config
    
    try:
        logger.info("Initializing optimized RAG/GRAG system...")
        
        # Create retrieval configuration
        retrieval_config = RetrievalConfig(
            max_vector_results=config.max_vector_results,
            max_graph_results=config.max_graph_results,
            rerank_threshold=config.rerank_threshold,
            fusion_weights=config.fusion_weights,
            enable_cache=config.enable_global_cache,
            cache_ttl=config.cache_ttl_seconds
        )
        
        # Initialize optimized chat
        optimized_chat = OptimizedChat(config=retrieval_config)
        
        logger.info("Optimized system initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize optimized system: {e}")
        logger.error(traceback.format_exc())
        
        # Try with fallback configuration
        try:
            logger.info("Trying with fallback configuration...")
            from optimization.fallback_config import get_fallback_config
            
            # Use fallback config
            config = get_fallback_config()
            
            # Retry with fallback config
            retrieval_config = RetrievalConfig(
                max_vector_results=config.max_vector_results,
                max_graph_results=config.max_graph_results,
                rerank_threshold=config.rerank_threshold,
                fusion_weights=config.fusion_weights,
                enable_cache=config.enable_global_cache,
                cache_ttl=config.cache_ttl_seconds
            )
            
            # Initialize with fallback models
            optimized_chat = OptimizedChat(config=retrieval_config)
            logger.info("System initialized with fallback configuration")
            return True
            
        except Exception as fallback_error:
            logger.error(f"Fallback initialization also failed: {fallback_error}")
            logger.error(traceback.format_exc())
            return False
        logger.error(traceback.format_exc())
        return False

@app.route('/api/chat/optimized', methods=['POST'])
def chat_optimized():
    """Optimized chat endpoint"""
    try:
        if not optimized_chat:
            return jsonify({
                'error': 'Optimized system not initialized',
                'status': 'error'
            }), 500
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        question = data['message']
        max_iterations = data.get('max_iterations', config.max_iterations)
        
        # Start timing
        start_time = time.time()
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            answer = loop.run_until_complete(
                optimized_chat.answer_question_optimized(question, max_iterations)
            )
        finally:
            loop.close()
        
        response_time = time.time() - start_time
        
        return jsonify({
            'answer': answer,
            'response_time': f"{response_time:.2f}s",
            'status': 'success',
            'optimizations_used': {
                'parallel_retrieval': True,
                'smart_caching': True,
                'result_fusion': True,
                'multi_iteration': max_iterations > 1
            }
        })
        
    except Exception as e:
        logger.error(f"Error in optimized chat: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/batch/optimized', methods=['POST'])
def batch_chat_optimized():
    """Batch processing với optimized system"""
    try:
        if not optimized_chat:
            return jsonify({
                'error': 'Optimized system not initialized',
                'status': 'error'
            }), 500
        
        data = request.get_json()
        if not data or 'questions' not in data:
            return jsonify({
                'error': 'Questions list is required',
                'status': 'error'
            }), 400
        
        questions = data['questions']
        if not isinstance(questions, list) or len(questions) == 0:
            return jsonify({
                'error': 'Questions must be a non-empty list',
                'status': 'error'
            }), 400
        
        start_time = time.time()
        
        # Run batch processing
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            answers = loop.run_until_complete(
                optimized_chat.batch_process_questions(questions)
            )
        finally:
            loop.close()
        
        response_time = time.time() - start_time
        
        return jsonify({
            'results': [
                {'question': q, 'answer': a} 
                for q, a in zip(questions, answers)
            ],
            'total_questions': len(questions),
            'total_time': f"{response_time:.2f}s",
            'avg_time_per_question': f"{response_time / len(questions):.2f}s",
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error in batch processing: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/metrics/performance', methods=['GET'])
def get_performance_metrics():
    """Lấy performance metrics"""
    try:
        if not optimized_chat:
            return jsonify({
                'error': 'Optimized system not initialized',
                'status': 'error'
            }), 500
        
        metrics = optimized_chat.get_performance_metrics()
        
        return jsonify({
            'metrics': metrics,
            'timestamp': time.time(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health/optimized', methods=['GET'])
def health_check_optimized():
    """Health check cho optimized system"""
    try:
        if not optimized_chat:
            return jsonify({
                'error': 'Optimized system not initialized',
                'status': 'error'
            }), 500
        
        # Run health check
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            health_results = loop.run_until_complete(
                optimized_chat.health_check()
            )
        finally:
            loop.close()
        
        all_healthy = all(health_results.values())
        
        return jsonify({
            'health': health_results,
            'overall_status': 'healthy' if all_healthy else 'degraded',
            'timestamp': time.time(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/config/current', methods=['GET'])
def get_current_config():
    """Lấy cấu hình hiện tại"""
    try:
        return jsonify({
            'config': {
                'environment': config.environment,
                'cache_enabled': config.enable_global_cache,
                'gpu_enabled': config.enable_gpu,
                'max_workers': config.max_workers,
                'max_batch_size': config.max_batch_size,
                'max_vector_results': config.max_vector_results,
                'max_graph_results': config.max_graph_results,
                'embedding_models': config.embedding_models
            },
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/benchmark/compare', methods=['POST'])
def benchmark_compare():
    """So sánh performance giữa optimized và original system"""
    try:
        data = request.get_json()
        if not data or 'test_questions' not in data:
            return jsonify({
                'error': 'Test questions are required',
                'status': 'error'
            }), 400
        
        test_questions = data['test_questions']
        iterations = data.get('iterations', 1)
        
        results = {
            'optimized_system': [],
            'comparison_metrics': {}
        }
        
        # Test optimized system
        for question in test_questions:
            start_time = time.time()
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                answer = loop.run_until_complete(
                    optimized_chat.answer_question_optimized(question)
                )
                response_time = time.time() - start_time
                
                results['optimized_system'].append({
                    'question': question,
                    'answer': answer,
                    'response_time': response_time
                })
                
            finally:
                loop.close()
        
        # Calculate aggregate metrics
        optimized_times = [r['response_time'] for r in results['optimized_system']]
        
        results['comparison_metrics'] = {
            'optimized_avg_time': sum(optimized_times) / len(optimized_times),
            'optimized_min_time': min(optimized_times),
            'optimized_max_time': max(optimized_times),
            'total_questions': len(test_questions),
            'cache_hits': optimized_chat.metrics['cache_hits']
        }
        
        return jsonify({
            'benchmark_results': results,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error in benchmark: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/')
def demo_page():
    """Serve demo page"""
    try:
        import os
        demo_path = os.path.join(os.path.dirname(__file__), 'demo.html')
        with open(demo_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"""
        <html>
        <head><title>Optimized RAG/GRAG Server</title></head>
        <body>
        <h1>🚀 Optimized RAG/GRAG Server Running!</h1>
        <p>Server is operational on port 5001</p>
        <p>API Endpoints:</p>
        <ul>
        <li>POST /api/chat/optimized - Chat with optimized system</li>
        <li>GET /api/health/optimized - Health check</li>
        <li>GET /api/metrics/performance - Performance metrics</li>
        </ul>
        <p>Status: {optimized_chat is not None}</p>
        </body>
        </html>
        """

if __name__ == '__main__':
    # Initialize optimized system
    if initialize_optimized_system():
        logger.info("Starting optimized Flask server...")
        app.run(
            host='0.0.0.0', 
            port=5001,  # Different port to avoid conflicts
            debug=config.debug,
            threaded=True
        )
    else:
        logger.error("Failed to start optimized server due to initialization error")
