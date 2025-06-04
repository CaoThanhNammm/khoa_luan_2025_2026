"""
Performance Benchmarking và Testing Suite
"""

import asyncio
import time
import statistics
import logging
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import pandas as pd
import json
from datetime import datetime

from optimization.OptimizedChat import OptimizedChat, RetrievalConfig
from optimization.config import get_config
from Chat import Chat  # Original chat system

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceBenchmark:
    """Benchmark suite để so sánh performance"""
    
    def __init__(self):
        self.config = get_config()
        self.original_chat = None
        self.optimized_chat = None
        self.test_questions = []
        self.results = {}
        
    def initialize_systems(self):
        """Initialize both chat systems"""
        try:
            logger.info("Initializing original chat system...")
            # Initialize original chat (adjust based on your original implementation)
            self.original_chat = Chat()
            
            logger.info("Initializing optimized chat system...")
            retrieval_config = RetrievalConfig(
                max_vector_results=self.config.max_vector_results,
                max_graph_results=self.config.max_graph_results,
                enable_cache=True,
                cache_ttl=1800
            )
            self.optimized_chat = OptimizedChat(config=retrieval_config)
            
            logger.info("Both systems initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing systems: {e}")
            raise
    
    def load_test_questions(self, questions_file: str = None):
        """Load test questions"""
        if questions_file:
            with open(questions_file, 'r', encoding='utf-8') as f:
                self.test_questions = json.load(f)
        else:
            # Default test questions
            self.test_questions = [
                "Sinh viên cần làm gì để được miễn học phí?",
                "Quy định về tham gia hoạt động ngoại khóa như thế nào?",
                "Điều kiện để được xét học bổng khuyến khích học tập là gì?",
                "Sinh viên bị cảnh cáo học tập phải làm gì?",
                "Quy trình đăng ký môn học được thực hiện như thế nào?",
                "Thời gian nộp đơn xin thôi học là khi nào?",
                "Sinh viên có thể tham gia nghiên cứu khoa học không?",
                "Điều kiện để được chuyển ngành học là gì?",
                "Quy định về việc bảo lưu kết quả học tập?",
                "Sinh viên vi phạm kỷ luật sẽ bị xử lý như thế nào?"
            ]
    
    async def run_benchmark_test(self, iterations: int = 3) -> Dict[str, Any]:
        """Chạy benchmark test"""
        logger.info(f"Running benchmark with {len(self.test_questions)} questions, {iterations} iterations...")
        
        results = {
            'original_system': [],
            'optimized_system': [],
            'metrics': {}
        }
        
        # Test original system
        logger.info("Testing original system...")
        for iteration in range(iterations):
            for question in self.test_questions:
                start_time = time.time()
                
                try:
                    # Adjust this call based on your original Chat implementation
                    answer = self.original_chat.answer_question(question)
                    response_time = time.time() - start_time
                    
                    results['original_system'].append({
                        'question': question,
                        'answer': answer,
                        'response_time': response_time,
                        'iteration': iteration
                    })
                    
                except Exception as e:
                    logger.error(f"Error in original system: {e}")
                    results['original_system'].append({
                        'question': question,
                        'answer': f"Error: {str(e)}",
                        'response_time': 0,
                        'iteration': iteration
                    })
        
        # Test optimized system
        logger.info("Testing optimized system...")
        for iteration in range(iterations):
            for question in self.test_questions:
                start_time = time.time()
                
                try:
                    answer = await self.optimized_chat.answer_question_optimized(question)
                    response_time = time.time() - start_time
                    
                    results['optimized_system'].append({
                        'question': question,
                        'answer': answer,
                        'response_time': response_time,
                        'iteration': iteration
                    })
                    
                except Exception as e:
                    logger.error(f"Error in optimized system: {e}")
                    results['optimized_system'].append({
                        'question': question,
                        'answer': f"Error: {str(e)}",
                        'response_time': 0,
                        'iteration': iteration
                    })
        
        # Calculate metrics
        results['metrics'] = self._calculate_metrics(results)
        
        return results
    
    def _calculate_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics"""
        original_times = [r['response_time'] for r in results['original_system'] if r['response_time'] > 0]
        optimized_times = [r['response_time'] for r in results['optimized_system'] if r['response_time'] > 0]
        
        metrics = {
            'original_system': {
                'avg_time': statistics.mean(original_times) if original_times else 0,
                'median_time': statistics.median(original_times) if original_times else 0,
                'min_time': min(original_times) if original_times else 0,
                'max_time': max(original_times) if original_times else 0,
                'std_dev': statistics.stdev(original_times) if len(original_times) > 1 else 0,
                'total_requests': len(original_times),
                'errors': len([r for r in results['original_system'] if r['response_time'] == 0])
            },
            'optimized_system': {
                'avg_time': statistics.mean(optimized_times) if optimized_times else 0,
                'median_time': statistics.median(optimized_times) if optimized_times else 0,
                'min_time': min(optimized_times) if optimized_times else 0,
                'max_time': max(optimized_times) if optimized_times else 0,
                'std_dev': statistics.stdev(optimized_times) if len(optimized_times) > 1 else 0,
                'total_requests': len(optimized_times),
                'errors': len([r for r in results['optimized_system'] if r['response_time'] == 0])
            }
        }
        
        # Calculate improvement
        if metrics['original_system']['avg_time'] > 0:
            improvement = (
                (metrics['original_system']['avg_time'] - metrics['optimized_system']['avg_time']) / 
                metrics['original_system']['avg_time'] * 100
            )
            metrics['improvement'] = {
                'speed_improvement_percent': improvement,
                'speed_multiplier': metrics['original_system']['avg_time'] / metrics['optimized_system']['avg_time'] if metrics['optimized_system']['avg_time'] > 0 else 0
            }
        
        # Add cache metrics for optimized system
        if self.optimized_chat:
            optimized_metrics = self.optimized_chat.get_performance_metrics()
            metrics['optimized_system']['cache_metrics'] = optimized_metrics
        
        return metrics
    
    def generate_performance_report(self, results: Dict[str, Any], output_file: str = None):
        """Generate detailed performance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_configuration': {
                'questions_count': len(self.test_questions),
                'iterations': len(results['original_system']) // len(self.test_questions),
                'config': {
                    'max_vector_results': self.config.max_vector_results,
                    'max_graph_results': self.config.max_graph_results,
                    'cache_enabled': self.config.enable_global_cache,
                    'gpu_enabled': self.config.enable_gpu
                }
            },
            'results': results['metrics'],
            'detailed_results': results
        }
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Report saved to {output_file}")
        
        return report
    
    def create_visualization(self, results: Dict[str, Any], output_dir: str = "benchmark_charts"):
        """Create performance visualization charts"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Response time comparison
        original_times = [r['response_time'] for r in results['original_system'] if r['response_time'] > 0]
        optimized_times = [r['response_time'] for r in results['optimized_system'] if r['response_time'] > 0]
        
        plt.figure(figsize=(12, 8))
        
        # Subplot 1: Response time comparison
        plt.subplot(2, 2, 1)
        plt.boxplot([original_times, optimized_times], labels=['Original', 'Optimized'])
        plt.title('Response Time Comparison')
        plt.ylabel('Time (seconds)')
        
        # Subplot 2: Average response time by question
        plt.subplot(2, 2, 2)
        questions_df = pd.DataFrame(results['optimized_system'])
        avg_times = questions_df.groupby('question')['response_time'].mean()
        plt.bar(range(len(avg_times)), avg_times.values)
        plt.title('Average Response Time by Question (Optimized)')
        plt.xlabel('Question Index')
        plt.ylabel('Time (seconds)')
        plt.xticks(rotation=45)
        
        # Subplot 3: Performance metrics comparison
        plt.subplot(2, 2, 3)
        metrics = results['metrics']
        categories = ['avg_time', 'median_time', 'min_time', 'max_time']
        original_values = [metrics['original_system'][cat] for cat in categories]
        optimized_values = [metrics['optimized_system'][cat] for cat in categories]
        
        x = range(len(categories))
        width = 0.35
        plt.bar([i - width/2 for i in x], original_values, width, label='Original')
        plt.bar([i + width/2 for i in x], optimized_values, width, label='Optimized')
        plt.xlabel('Metrics')
        plt.ylabel('Time (seconds)')
        plt.title('Performance Metrics Comparison')
        plt.xticks(x, categories)
        plt.legend()
        
        # Subplot 4: Improvement visualization
        plt.subplot(2, 2, 4)
        if 'improvement' in metrics:
            improvement = metrics['improvement']['speed_improvement_percent']
            plt.bar(['Speed Improvement'], [improvement])
            plt.title(f'Performance Improvement: {improvement:.1f}%')
            plt.ylabel('Improvement (%)')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Charts saved to {output_dir}/")

async def main():
    """Main benchmark execution"""
    benchmark = PerformanceBenchmark()
    
    try:
        # Initialize systems
        benchmark.initialize_systems()
        
        # Load test questions
        benchmark.load_test_questions()
        
        # Run benchmark
        results = await benchmark.run_benchmark_test(iterations=3)
        
        # Generate report
        report = benchmark.generate_performance_report(
            results, 
            f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        # Create visualizations
        benchmark.create_visualization(results)
        
        # Print summary
        metrics = results['metrics']
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK RESULTS")
        print("="*60)
        print(f"Original System - Avg Time: {metrics['original_system']['avg_time']:.3f}s")
        print(f"Optimized System - Avg Time: {metrics['optimized_system']['avg_time']:.3f}s")
        
        if 'improvement' in metrics:
            print(f"Speed Improvement: {metrics['improvement']['speed_improvement_percent']:.1f}%")
            print(f"Speed Multiplier: {metrics['improvement']['speed_multiplier']:.2f}x")
        
        print(f"Cache Hit Rate: {benchmark.optimized_chat.metrics['cache_hits']} hits")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
