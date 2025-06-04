"""
Configuration file cho hệ thống RAG/GRAG tối ưu hóa
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class SystemConfig:
    """Cấu hình tổng thể cho hệ thống"""
    
    # Environment
    environment: str = "development"  # development, production
    debug: bool = True
    
    # Qdrant Configuration
    qdrant_url: str = "https://0d9e031b-a61d-479b-8a5e-1b1aeeba93a0.us-west-1-0.aws.cloud.qdrant.io:6333"
    qdrant_api_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.kVTMd_unNC9-pK_NsxehcjvoHSVzeHT7OmmmCdgppis"
    qdrant_collection: str = "Số tay sinh viên"
    
    # Neo4j Configuration
    neo4j_uri: str = "neo4j+s://4e1a09c4.databases.neo4j.io"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "0hEim02sJ0LOqIArIDcQ0StvSntXIMc2qZyaDVAM37k"
    neo4j_max_pool_size: int = 50
    neo4j_connection_timeout: int = 60
    
    # Cache Configuration
    enable_global_cache: bool = True
    cache_ttl_seconds: int = 1800  # 30 minutes
    embedding_cache_size: int = 10000
    query_cache_size: int = 1000
    response_cache_size: int = 500
    
    # Performance Configuration
    max_workers: int = 8
    max_batch_size: int = 32
    enable_gpu: bool = True
    max_models_in_memory: int = 4
    
    # Retrieval Configuration
    max_vector_results: int = 25
    max_graph_results: int = 20
    rerank_threshold: float = 0.1
    fusion_weights: Dict[str, float] = None
    max_iterations: int = 2
    
    # Embedding Models Configuration
    embedding_models: Dict[str, str] = None
    
    def __post_init__(self):
        if self.fusion_weights is None:
            self.fusion_weights = {
                'vector': 0.6,
                'graph': 0.4
            }
        
        if self.embedding_models is None:
            self.embedding_models = {
                'model_512': "sentence-transformers/distiluse-base-multilingual-cased-v2",
                'model_768': "Alibaba-NLP/gte-multilingual-base", 
                'model_1024': "intfloat/multilingual-e5-large-instruct",
                'model_late_interaction': "colbert-ir/colbertv2.0"
            }

@dataclass
class OptimizationConfig:
    """Cấu hình cho các tối ưu hóa"""
    
    # Qdrant Optimizations
    qdrant_hnsw_m: int = 32
    qdrant_hnsw_ef_construct: int = 400
    qdrant_enable_quantization: bool = True
    qdrant_enable_async: bool = True
    qdrant_batch_size: int = 32
    
    # Neo4j Optimizations
    neo4j_enable_indexing: bool = True
    neo4j_enable_query_cache: bool = True
    neo4j_parallel_queries: bool = True
    neo4j_max_query_depth: int = 3
    
    # Embedding Optimizations
    embedding_enable_fp16: bool = True
    embedding_enable_batch_processing: bool = True
    embedding_adaptive_batch_size: bool = True
    embedding_memory_optimization: bool = True
    
    # Chat Optimizations
    chat_parallel_retrieval: bool = True
    chat_enable_fusion: bool = True
    chat_adaptive_strategy: bool = True
    chat_multi_iteration: bool = True

# Global configuration instance
config = SystemConfig()
optimization_config = OptimizationConfig()

def load_config_from_env():
    """Load configuration từ environment variables"""
    global config
    
    # Override from environment if exists
    config.qdrant_url = os.getenv('QDRANT_URL', config.qdrant_url)
    config.qdrant_api_key = os.getenv('QDRANT_API_KEY', config.qdrant_api_key)
    config.neo4j_uri = os.getenv('NEO4J_URI', config.neo4j_uri)
    config.neo4j_user = os.getenv('NEO4J_USER', config.neo4j_user)
    config.neo4j_password = os.getenv('NEO4J_PASSWORD', config.neo4j_password)
    
    config.enable_global_cache = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    config.enable_gpu = os.getenv('ENABLE_GPU', 'true').lower() == 'true'
    config.debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    # Performance settings
    config.max_workers = int(os.getenv('MAX_WORKERS', config.max_workers))
    config.max_batch_size = int(os.getenv('MAX_BATCH_SIZE', config.max_batch_size))

def get_config() -> SystemConfig:
    """Get current configuration"""
    return config

def get_optimization_config() -> OptimizationConfig:
    """Get optimization configuration"""
    return optimization_config
