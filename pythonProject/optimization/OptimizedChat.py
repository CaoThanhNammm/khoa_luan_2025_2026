"""
Tối ưu hóa Chat System với cải tiến về:
1. Parallel processing
2. Smart caching
3. Adaptive retrieval
4. Response fusion
5. Memory optimization
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import lru_cache
import logging
from contextlib import asynccontextmanager

from langchain_core.prompts import PromptTemplate

# Import optimized components
from optimization.OptimizedQdrant import OptimizedQdrant
from optimization.OptimizedNeo4jDatabase import OptimizedNeo4jDatabase
from optimization.OptimizedEmbeddingFactory import OptimizedEmbeddingFactory
from optimization.text_processing import vietnamese_processor

@dataclass
class RetrievalConfig:
    """Cấu hình retrieval"""
    max_vector_results: int = 25
    max_graph_results: int = 20
    rerank_threshold: float = 0.1
    fusion_weights: Dict[str, float] = None
    enable_cache: bool = True
    cache_ttl: int = 1800  # 30 minutes

@dataclass
class QueryResult:
    """Kết quả query với metadata"""
    content: str
    source: str  # 'vector' or 'graph'
    score: float
    execution_time: float

class OptimizedChat:
    """Chat system tối ưu hóa với parallel retrieval và smart caching"""
    
    def __init__(self, config: RetrievalConfig = None):
        self.config = config or RetrievalConfig()
        if self.config.fusion_weights is None:
            self.config.fusion_weights = {'vector': 0.6, 'graph': 0.4}
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Initialize optimized components
        self._initialize_components()
        
        # Cache và performance
        self.response_cache = {}
        self.retrieval_cache = {}
        self.metrics = {
            'queries_processed': 0,
            'cache_hits': 0,
            'avg_response_time': 0,
            'response_times': []
        }
        
        # Async executors
        self.executor = ThreadPoolExecutor(max_workers=8)
        
        self.logger = logging.getLogger(__name__)
        
    def _initialize_components(self):
        """Initialize optimized components"""
        # Initialize embedding factory
        self.embedding_factory = OptimizedEmbeddingFactory(
            enable_gpu=True,
            max_models_in_memory=4
        )
          # Initialize optimized Qdrant
        self.qdrant = OptimizedQdrant(
            host="https://0d9e031b-a61d-479b-8a5e-1b1aeeba93a0.us-west-1-0.aws.cloud.qdrant.io:6333",
            api="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.kVTMd_unNC9-pK_NsxehcjvoHSVzeHT7OmmmCdgppis",
            models_config={
                'model_512': self.embedding_factory.create_embed_model("sentence-transformers/distiluse-base-multilingual-cased-v2"),
                'model_768': self.embedding_factory.create_embed_model("Alibaba-NLP/gte-multilingual-base"),
                'model_1024': self.embedding_factory.create_embed_model("intfloat/multilingual-e5-large-instruct"),
                'model_late_interaction': self.embedding_factory.create_embed_model("colbert-ir/colbertv2.0")
            },
            collection_name="Số tay sinh viên",
            pre_processing=vietnamese_processor  # Use the optimized Vietnamese processor
        )
        
        # Initialize optimized Neo4j
        self.neo4j = OptimizedNeo4jDatabase(
            uri="neo4j+s://4e1a09c4.databases.neo4j.io",
            user="neo4j",
            password="0hEim02sJ0LOqIArIDcQ0StvSntXIMc2qZyaDVAM37k"
        )
        
        self.logger.info("Optimized components initialized successfully")

    async def answer_question_optimized(self, question: str, max_iterations: int = 2) -> str:
        """Trả lời câu hỏi với tối ưu hóa đầy đủ"""
        start_time = time.time()
        
        # Check response cache
        cache_key = f"response_{hash(question)}"
        if self.config.enable_cache and cache_key in self.response_cache:
            cached_response, cache_time = self.response_cache[cache_key]
            if time.time() - cache_time < self.config.cache_ttl:
                self.metrics['cache_hits'] += 1
                return cached_response
        
        try:
            # Multi-iteration reasoning với optimization
            final_answer = await self._multi_iteration_reasoning(question, max_iterations)
            
            # Cache response
            if self.config.enable_cache:
                self.response_cache[cache_key] = (final_answer, time.time())
                self._clean_old_cache()
            
            # Update metrics
            response_time = time.time() - start_time
            self.metrics['queries_processed'] += 1
            self.metrics['response_times'].append(response_time)
            
            self.logger.info(f"Question answered in {response_time:.2f}s")
            return final_answer
            
        except Exception as e:
            self.logger.error(f"Error answering question: {e}")
            return "Xin lỗi, tôi không thể trả lời câu hỏi này lúc này."

    async def _multi_iteration_reasoning(self, question: str, max_iterations: int) -> str:
        """Multi-iteration reasoning với feedback loop"""
        current_answer = ""
        feedback = ""
        
        for iteration in range(max_iterations):
            self.logger.info(f"Iteration {iteration + 1}/{max_iterations}")
            
            # Determine retrieval strategy
            retrieval_strategy = await self._determine_retrieval_strategy(question, feedback)
            
            # Parallel retrieval
            retrieval_results = await self._parallel_retrieval(question, retrieval_strategy)
            
            # Generate answer
            current_answer = await self._generate_answer(question, retrieval_results)
            
            # Validate answer
            is_valid = await self._validate_answer(question, current_answer)
            
            if is_valid:
                break
                
            # Generate feedback for next iteration
            feedback = await self._generate_feedback(question, current_answer, retrieval_results)
        
        return current_answer

    async def _determine_retrieval_strategy(self, question: str, feedback: str = "") -> Dict[str, bool]:
        """Xác định strategy retrieval thông minh"""
        # Simplified strategy determination
        # Có thể cải tiến với ML model
        
        strategy = {
            'use_vector': True,
            'use_graph': True,
            'use_hybrid_fusion': True,
            'priority': 'balanced'  # 'vector', 'graph', 'balanced'
        }
        
        # Adjust based on question type and feedback
        if "số liệu" in question.lower() or "thống kê" in question.lower():
            strategy['priority'] = 'vector'
            strategy['use_graph'] = False
        elif "quy định" in question.lower() or "luật" in question.lower():
            strategy['priority'] = 'graph'
            strategy['use_vector'] = False
        elif feedback and "không đủ thông tin" in feedback:
            strategy['use_hybrid_fusion'] = True
            strategy['priority'] = 'balanced'
            
        return strategy

    async def _parallel_retrieval(self, question: str, strategy: Dict[str, bool]) -> List[QueryResult]:
        """Parallel retrieval từ multiple sources"""
        tasks = []
        
        # Vector search task
        if strategy['use_vector']:
            tasks.append(self._vector_retrieval_task(question))
            
        # Graph search task  
        if strategy['use_graph']:
            tasks.append(self._graph_retrieval_task(question))
        
        # Execute tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine and process results
        all_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Retrieval error: {result}")
                continue
            all_results.extend(result)
        
        # Apply fusion if enabled
        if strategy['use_hybrid_fusion'] and len(all_results) > 1:
            all_results = self._apply_result_fusion(all_results, strategy['priority'])
        
        return all_results

    async def _vector_retrieval_task(self, question: str) -> List[QueryResult]:
        """Vector retrieval task"""
        start_time = time.time()
        
        try:
            # Use optimized hybrid search
            documents = await self.qdrant.hybrid_search_optimized(
                question, 
                limit=self.config.max_vector_results
            )
            
            # Re-rank if needed
            if len(documents) > 10:
                documents = await self.qdrant.re_ranking_optimized(question, documents)
            
            execution_time = time.time() - start_time
            
            results = []
            for i, doc in enumerate(documents):
                results.append(QueryResult(
                    content=doc,
                    source='vector',
                    score=1.0 - (i * 0.1),  # Decreasing score by rank
                    execution_time=execution_time
                ))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Vector retrieval error: {e}")
            return []    
    async def _graph_retrieval_task(self, question: str) -> List[QueryResult]:
        """Graph retrieval task"""
        start_time = time.time()
        
        try:
            # Use intelligent query generation
            triplets = await self.neo4j.intelligent_query_from_question(question)
            
            execution_time = time.time() - start_time
            
            results = []
            if not triplets:
                return results
                
            # Handle different response formats
            if isinstance(triplets, list):
                for i, triplet in enumerate(triplets[:self.config.max_graph_results]):
                    # Convert triplet to string if needed
                    content = triplet
                    if isinstance(triplet, dict):
                        content = json.dumps(triplet)
                    elif not isinstance(triplet, str):
                        content = str(triplet)
                        
                    results.append(QueryResult(
                        content=content,
                        source='graph',
                        score=1.0 - (i * 0.05),  # Decreasing score by rank
                        execution_time=execution_time
                    ))
            elif isinstance(triplets, dict):
                # Handle dictionary response format
                results.append(QueryResult(
                    content=json.dumps(triplets),
                    source='graph',
                    score=1.0,
                    execution_time=execution_time
                ))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Graph retrieval error: {e}")
            return []

    def _apply_result_fusion(self, results: List[QueryResult], priority: str) -> List[QueryResult]:
        """Apply fusion algorithm to combine results"""
        vector_results = [r for r in results if r.source == 'vector']
        graph_results = [r for r in results if r.source == 'graph']
        
        # Apply weighted scoring based on priority
        if priority == 'vector':
            vector_weight = 0.8
            graph_weight = 0.2
        elif priority == 'graph':
            vector_weight = 0.2
            graph_weight = 0.8
        else:  # balanced
            vector_weight = self.config.fusion_weights['vector']
            graph_weight = self.config.fusion_weights['graph']
        
        # Reweight scores
        for result in vector_results:
            result.score *= vector_weight
        for result in graph_results:
            result.score *= graph_weight
        
        # Combine and sort by final score
        all_results = vector_results + graph_results
        all_results.sort(key=lambda x: x.score, reverse=True)
        
        # Return top results
        return all_results[:min(20, len(all_results))]

    async def _generate_answer(self, question: str, retrieval_results: List[QueryResult]) -> str:
        """Generate answer từ retrieval results"""
        if not retrieval_results:
            return "Tôi không tìm thấy thông tin liên quan để trả lời câu hỏi này."
        
        # Combine high-score results
        high_quality_results = [
            r for r in retrieval_results 
            if r.score > self.config.rerank_threshold
        ]
        
        if not high_quality_results:
            high_quality_results = retrieval_results[:5]  # Take top 5 if none meet threshold
        
        # Create context from results
        context = "\n".join([result.content for result in high_quality_results])
        
        # Generate answer (placeholder - integrate with your LLM)
        prompt = f"""
        Câu hỏi: {question}
        
        Thông tin tham khảo:
        {context}
        
        Hãy trả lời câu hỏi dựa trên thông tin được cung cấp.
        """
        
        # Here you would call your LLM (Gemini) to generate the answer
        # For now, returning a placeholder
        return f"Dựa trên thông tin tìm được, câu trả lời cho '{question}' là: [Generated Answer]"

    async def _validate_answer(self, question: str, answer: str) -> bool:
        """Validate answer quality"""
        # Simple validation rules
        if len(answer) < 20:
            return False
        if "không tìm thấy" in answer.lower():
            return False
        if "xin lỗi" in answer.lower():
            return False
            
        # More sophisticated validation can be added
        return True

    async def _generate_feedback(self, question: str, answer: str, retrieval_results: List[QueryResult]) -> str:
        """Generate feedback for next iteration"""
        if not retrieval_results:
            return "Cần tìm kiếm thêm thông tin từ các nguồn khác."
        
        vector_count = len([r for r in retrieval_results if r.source == 'vector'])
        graph_count = len([r for r in retrieval_results if r.source == 'graph'])
        
        if vector_count == 0:
            return "Cần thêm thông tin từ tài liệu vector."
        elif graph_count == 0:
            return "Cần thêm thông tin từ knowledge graph."
        else:
            return "Cần cải thiện chất lượng thông tin được truy xuất."

    def _clean_old_cache(self):
        """Clean expired cache entries"""
        current_time = time.time()
        
        # Clean response cache
        expired_keys = [
            key for key, (_, cache_time) in self.response_cache.items()
            if current_time - cache_time > self.config.cache_ttl
        ]
        for key in expired_keys:
            del self.response_cache[key]
        
        # Clean retrieval cache
        expired_keys = [
            key for key, (_, cache_time) in self.retrieval_cache.items()
            if current_time - cache_time > self.config.cache_ttl
        ]
        for key in expired_keys:
            del self.retrieval_cache[key]

    async def batch_process_questions(self, questions: List[str]) -> List[str]:
        """Process multiple questions in parallel"""
        tasks = [self.answer_question_optimized(q) for q in questions]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        answers = []
        for result in results:
            if isinstance(result, Exception):
                answers.append(f"Error: {str(result)}")
            else:
                answers.append(result)
        
        return answers

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        cache_total = self.metrics['queries_processed'] + self.metrics['cache_hits']
        cache_hit_rate = (self.metrics['cache_hits'] / cache_total * 100) if cache_total > 0 else 0
        
        avg_response_time = (
            sum(self.metrics['response_times']) / len(self.metrics['response_times'])
            if self.metrics['response_times'] else 0
        )
        
        return {
            'chat_metrics': {
                'total_queries': self.metrics['queries_processed'],
                'cache_hits': self.metrics['cache_hits'],
                'cache_hit_rate': f"{cache_hit_rate:.2f}%",
                'avg_response_time': f"{avg_response_time:.3f}s",
                'cache_size': len(self.response_cache)
            },
            'qdrant_metrics': self.qdrant.get_performance_metrics(),
            'neo4j_metrics': self.neo4j.get_performance_metrics(),
        }

    async def health_check(self) -> Dict[str, bool]:
        """Comprehensive system health check"""
        results = {}
        
        # Check Qdrant
        try:
            test_results = await self.qdrant.hybrid_search_optimized("test query", limit=1)
            results['qdrant'] = len(test_results) >= 0
        except:
            results['qdrant'] = False
        
        # Check Neo4j
        try:
            results['neo4j'] = await self.neo4j.health_check()
        except:
            results['neo4j'] = False
        
        # Check embedding models
        try:
            test_embedding = self.qdrant.models['model_512'].embed("test")
            results['embeddings'] = len(test_embedding) > 0
        except:
            results['embeddings'] = False
            
        return results

    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
        if hasattr(self, 'neo4j'):
            self.neo4j.close()
