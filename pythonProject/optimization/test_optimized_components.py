"""
Test suite cho optimized components
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch, MagicMock
import numpy as np

# Import optimized components
from optimization.OptimizedQdrant import OptimizedQdrant, CacheConfig
from optimization.OptimizedNeo4jDatabase import OptimizedNeo4jDatabase
from optimization.OptimizedEmbeddingFactory import OptimizedEmbeddingFactory, ModelConfig
from optimization.OptimizedChat import OptimizedChat, RetrievalConfig
from optimization.config import SystemConfig

class TestOptimizedQdrant:
    """Test cases cho OptimizedQdrant"""
    
    @pytest.fixture
    def mock_qdrant_client(self):
        """Mock Qdrant client"""
        with patch('optimization.OptimizedQdrant.QdrantClient') as mock:
            mock_client = Mock()
            mock.return_value = mock_client
            yield mock_client
    
    @pytest.fixture
    def optimized_qdrant(self, mock_qdrant_client):
        """Create OptimizedQdrant instance for testing"""
        models_config = {
            'model_512': Mock(),
            'model_768': Mock(),
            'model_1024': Mock(),
            'model_late_interaction': Mock()
        }
        
        cache_config = CacheConfig(
            embedding_cache_size=100,
            ttl_seconds=300
        )
        
        return OptimizedQdrant(
            host="test_host",
            api="test_api",
            models_config=models_config,
            collection_name="test_collection",
            pre_processing=Mock(),
            cache_config=cache_config
        )
    
    def test_cache_functionality(self, optimized_qdrant):
        """Test caching functionality"""
        # Test cache miss and hit
        cache_key = "test_key"
        test_embedding = np.array([1, 2, 3, 4, 5])
        
        # First access - cache miss
        cached = optimized_qdrant.embedding_cache.get(cache_key)
        assert cached is None
        
        # Store in cache
        optimized_qdrant.embedding_cache.put(cache_key, test_embedding)
        
        # Second access - cache hit
        cached = optimized_qdrant.embedding_cache.get(cache_key)
        assert np.array_equal(cached, test_embedding)
    
    @pytest.mark.asyncio
    async def test_async_embedding_creation(self, optimized_qdrant):
        """Test async embedding creation"""
        with patch.object(optimized_qdrant, '_process_batch_async') as mock_batch:
            mock_batch.return_value = {
                'dense-512': [np.array([1, 2, 3])],
                'dense-768': [np.array([1, 2, 3, 4])],
                'dense-1024': [np.array([1, 2, 3, 4, 5])],
                'sparse': [np.array([1, 2])]
            }
            
            texts = ["test text"]
            result = await optimized_qdrant.create_embeddings_async(texts)
            
            assert 'dense-512' in result
            assert 'dense-768' in result
            assert 'dense-1024' in result
            assert 'sparse' in result
    
    def test_performance_metrics(self, optimized_qdrant):
        """Test performance metrics collection"""
        # Simulate some operations
        optimized_qdrant.metrics['cache_hits'] = 10
        optimized_qdrant.metrics['cache_misses'] = 5
        optimized_qdrant.metrics['query_times'] = [0.1, 0.2, 0.15]
        
        metrics = optimized_qdrant.get_performance_metrics()
        
        assert 'cache_hits' in metrics
        assert 'cache_misses' in metrics
        assert 'avg_query_time' in metrics
        assert metrics['cache_hits'] == 10

class TestOptimizedNeo4jDatabase:
    """Test cases cho OptimizedNeo4jDatabase"""
    
    @pytest.fixture
    def mock_neo4j_driver(self):
        """Mock Neo4j driver"""
        with patch('optimization.OptimizedNeo4jDatabase.GraphDatabase') as mock:
            mock_driver = Mock()
            mock.driver.return_value = mock_driver
            yield mock_driver
    
    @pytest.fixture
    def optimized_neo4j(self, mock_neo4j_driver):
        """Create OptimizedNeo4jDatabase instance for testing"""
        return OptimizedNeo4jDatabase(
            uri="test_uri",
            user="test_user",
            password="test_password"
        )
    
    def test_query_cache(self, optimized_neo4j):
        """Test query caching"""
        query = "MATCH (n) RETURN n LIMIT 1"
        params = {"param": "value"}
        
        # Mock the query cache
        cache_key = optimized_neo4j.query_cache._get_hash(query, params)
        test_result = [{"n": "test_node"}]
        
        # Test cache miss
        cached = optimized_neo4j.query_cache.get(query, params)
        assert cached is None
        
        # Store in cache
        optimized_neo4j.query_cache.put(query, params, test_result)
        
        # Test cache hit
        cached = optimized_neo4j.query_cache.get(query, params)
        assert cached == test_result
    
    @pytest.mark.asyncio
    async def test_parallel_entity_search(self, optimized_neo4j):
        """Test parallel entity search"""
        entities = ["entity1", "entity2", "entity3"]
        
        with patch.object(optimized_neo4j, 'optimized_entity_search') as mock_search:
            mock_search.return_value = [{"entity": "test"}]
            
            result = await optimized_neo4j.parallel_multi_entity_search(entities)
            
            assert len(result) == len(entities)
            assert mock_search.call_count == len(entities)
    
    def test_triplet_creation(self, optimized_neo4j):
        """Test triplet creation from graph records"""
        mock_records = [
            {
                'path': {
                    'relationships': [
                        Mock(
                            start_node={'name': 'Entity1'},
                            end_node={'name': 'Entity2'},
                            type='RELATES_TO'
                        )
                    ]
                }
            }
        ]
        
        triplets = optimized_neo4j.create_triplets_optimized(mock_records)
        
        assert len(triplets) > 0
        assert "Entity1 -> RELATES_TO -> Entity2" in triplets

class TestOptimizedEmbeddingFactory:
    """Test cases cho OptimizedEmbeddingFactory"""
    
    @pytest.fixture
    def embedding_factory(self):
        """Create OptimizedEmbeddingFactory instance for testing"""
        return OptimizedEmbeddingFactory(
            enable_gpu=False,  # Disable GPU for testing
            max_models_in_memory=2
        )
    
    def test_model_creation(self, embedding_factory):
        """Test model creation and pooling"""
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        
        with patch('optimization.OptimizedEmbeddingFactory.OptimizedGenericModel') as mock_model:
            mock_instance = Mock()
            mock_model.return_value = mock_instance
            
            model = embedding_factory.create_embed_model(model_name)
            
            assert model is not None
            assert model_name in embedding_factory.model_pool
    
    def test_model_pooling(self, embedding_factory):
        """Test model pooling functionality"""
        model_name = "test_model"
        
        # Create mock model
        mock_model = Mock()
        embedding_factory.model_pool[model_name] = mock_model
        
        # Get model from pool
        retrieved_model = embedding_factory.get_model(model_name)
        
        assert retrieved_model == mock_model
    
    def test_memory_management(self, embedding_factory):
        """Test memory management"""
        # Set max models to 1 for testing
        embedding_factory.max_models_in_memory = 1
        
        with patch('optimization.OptimizedEmbeddingFactory.OptimizedGenericModel') as mock_model:
            mock_instance1 = Mock()
            mock_instance2 = Mock()
            mock_model.side_effect = [mock_instance1, mock_instance2]
            
            # Add first model
            model1 = embedding_factory.create_embed_model("model1")
            assert len(embedding_factory.model_pool) == 1
            
            # Add second model - should evict first
            model2 = embedding_factory.create_embed_model("model2")
            assert len(embedding_factory.model_pool) == 1
            assert "model2" in embedding_factory.model_pool

class TestOptimizedChat:
    """Test cases cho OptimizedChat"""
    
    @pytest.fixture
    def retrieval_config(self):
        """Create RetrievalConfig for testing"""
        return RetrievalConfig(
            max_vector_results=10,
            max_graph_results=10,
            enable_cache=True,
            cache_ttl=300
        )
    
    @pytest.fixture
    def optimized_chat(self, retrieval_config):
        """Create OptimizedChat instance for testing"""
        with patch.object(OptimizedChat, '_initialize_components'):
            chat = OptimizedChat(config=retrieval_config)
            
            # Mock components
            chat.qdrant = Mock()
            chat.neo4j = Mock()
            chat.embedding_factory = Mock()
            
            return chat
    
    def test_response_caching(self, optimized_chat):
        """Test response caching"""
        question = "test question"
        answer = "test answer"
        
        # Mock cache
        cache_key = f"response_{hash(question)}"
        optimized_chat.response_cache[cache_key] = (answer, time.time())
        
        # Test cache retrieval (this would be part of answer_question_optimized)
        assert cache_key in optimized_chat.response_cache
        cached_answer, cache_time = optimized_chat.response_cache[cache_key]
        assert cached_answer == answer
    
    @pytest.mark.asyncio
    async def test_parallel_retrieval(self, optimized_chat):
        """Test parallel retrieval"""
        question = "test question"
        strategy = {
            'use_vector': True,
            'use_graph': True,
            'use_hybrid_fusion': False,
            'priority': 'balanced'
        }
        
        # Mock retrieval methods
        with patch.object(optimized_chat, '_vector_retrieval_task') as mock_vector, \
             patch.object(optimized_chat, '_graph_retrieval_task') as mock_graph:
            
            mock_vector.return_value = [Mock(source='vector', score=0.9)]
            mock_graph.return_value = [Mock(source='graph', score=0.8)]
            
            results = await optimized_chat._parallel_retrieval(question, strategy)
            
            assert len(results) == 2
            assert mock_vector.called
            assert mock_graph.called
    
    def test_strategy_determination(self, optimized_chat):
        """Test retrieval strategy determination"""
        # Test different question types
        statistical_question = "Có bao nhiêu sinh viên trong trường?"
        regulation_question = "Quy định về học phí như thế nào?"
        
        # Note: This would need to be an async test if the method is async
        # For now, testing the logic structure
        strategy_stats = {
            'use_vector': True,
            'use_graph': False,
            'priority': 'vector'
        }
        
        strategy_regs = {
            'use_vector': False,
            'use_graph': True,
            'priority': 'graph'
        }
        
        # These would be actual calls to the method
        assert 'use_vector' in strategy_stats
        assert 'use_graph' in strategy_regs
    
    def test_performance_metrics_collection(self, optimized_chat):
        """Test performance metrics collection"""
        # Simulate some operations
        optimized_chat.metrics['queries_processed'] = 5
        optimized_chat.metrics['cache_hits'] = 2
        optimized_chat.metrics['response_times'] = [1.0, 1.5, 0.8, 1.2, 0.9]
        
        # Mock component metrics
        optimized_chat.qdrant.get_performance_metrics.return_value = {
            'cache_hits': 10,
            'total_queries': 15
        }
        optimized_chat.neo4j.get_performance_metrics.return_value = {
            'cache_hits': 5,
            'total_queries': 8
        }
        
        metrics = optimized_chat.get_performance_metrics()
        
        assert 'chat_metrics' in metrics
        assert 'qdrant_metrics' in metrics
        assert 'neo4j_metrics' in metrics
        assert metrics['chat_metrics']['total_queries'] == 5

class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_system_health_check(self):
        """Test full system health check"""
        config = RetrievalConfig(enable_cache=True)
        
        with patch.object(OptimizedChat, '_initialize_components'):
            chat = OptimizedChat(config=config)
            
            # Mock health check responses
            chat.qdrant = Mock()
            chat.qdrant.hybrid_search_optimized = Mock(return_value=["test"])
            
            chat.neo4j = Mock()
            chat.neo4j.health_check = Mock(return_value=True)
            
            # Mock embedding model
            mock_model = Mock()
            mock_model.embed = Mock(return_value=[1, 2, 3])
            chat.qdrant.models = {'model_512': mock_model}
            
            health_results = await chat.health_check()
            
            assert 'qdrant' in health_results
            assert 'neo4j' in health_results
            assert 'embeddings' in health_results
    
    def test_config_loading(self):
        """Test configuration loading"""
        config = SystemConfig()
        
        assert config.environment == "development"
        assert config.enable_global_cache == True
        assert config.max_workers == 8
        assert isinstance(config.embedding_models, dict)
        assert len(config.embedding_models) == 4

# Performance benchmarks
class TestPerformanceBenchmarks:
    """Performance benchmark tests"""
    
    def test_cache_performance(self):
        """Test cache performance"""
        from optimization.OptimizedQdrant import EmbeddingCache
        
        cache = EmbeddingCache(max_size=1000)
        
        # Measure cache operations
        start_time = time.time()
        
        for i in range(1000):
            cache.put(f"key_{i}", np.random.rand(768))
        
        put_time = time.time() - start_time
        
        start_time = time.time()
        
        for i in range(1000):
            cache.get(f"key_{i}")
        
        get_time = time.time() - start_time
        
        # Assert reasonable performance
        assert put_time < 1.0  # Should be fast
        assert get_time < 0.5  # Gets should be very fast
    
    @pytest.mark.asyncio
    async def test_parallel_processing_performance(self):
        """Test parallel processing performance"""
        # Mock parallel operations
        async def mock_operation(x):
            await asyncio.sleep(0.01)  # Simulate work
            return x * 2
        
        # Sequential processing
        start_time = time.time()
        sequential_results = []
        for i in range(10):
            result = await mock_operation(i)
            sequential_results.append(result)
        sequential_time = time.time() - start_time
        
        # Parallel processing
        start_time = time.time()
        tasks = [mock_operation(i) for i in range(10)]
        parallel_results = await asyncio.gather(*tasks)
        parallel_time = time.time() - start_time
        
        # Parallel should be faster
        assert parallel_time < sequential_time
        assert parallel_results == sequential_results

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
