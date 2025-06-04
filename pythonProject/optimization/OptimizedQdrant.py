"""
Tối ưu hóa Vector Database Qdrant để truy xuất nhanh hơn
Cải tiến:
1. Cache embedding vectors
2. Batch processing tối ưu
3. Async/await operations
4. Memory management
5. Index optimization
"""

import asyncio
import pickle
import hashlib
from typing import List, Dict, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct, SearchRequest
from functools import lru_cache
import time
import logging
from dataclasses import dataclass
from contextlib import asynccontextmanager

@dataclass
class CacheConfig:
    """Cấu hình cache"""
    max_size: int = 1000
    ttl_seconds: int = 3600  # 1 hour
    embedding_cache_size: int = 10000

class EmbeddingCache:
    """Cache cho embeddings để tránh tính toán lặp lại"""
    
    def __init__(self, max_size: int = 10000):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
        
    def _get_hash(self, text: str) -> str:
        """Tạo hash cho text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, text: str) -> Optional[np.ndarray]:
        """Lấy embedding từ cache"""
        key = self._get_hash(text)
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None
    
    def set(self, text: str, embedding: np.ndarray):
        """Lưu embedding vào cache"""
        key = self._get_hash(text)
        
        # LRU eviction if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times.keys(), 
                           key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = embedding
        self.access_times[key] = time.time()

class OptimizedQdrant:
    """Qdrant tối ưu hóa với cache, async operations và batch processing"""
    
    def __init__(self, host: str, api: str, models_config: Dict, 
                 collection_name: str, pre_processing, cache_config: CacheConfig = None):
        self.client = QdrantClient(url=host, api_key=api)
        self.collection_name = collection_name
        self.pre_processing = pre_processing
        
        # Models
        self.models = models_config
        
        # Cache configuration
        self.cache_config = cache_config or CacheConfig()
        self.embedding_cache = EmbeddingCache(self.cache_config.embedding_cache_size)
        self.query_cache = {}
        
        # Performance metrics
        self.metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'query_times': [],
            'embedding_times': []
        }
        
        # Thread pool for parallel operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
    def create_optimized_collection(self, collection_name: str, size: int, distance: str):
        """Tạo collection với cấu hình tối ưu"""
        if self.client.collection_exists(collection_name=collection_name):
            return

        # Cấu hình HNSW tối ưu cho hiệu năng
        optimized_hnsw_config = models.HnswConfig(
            m=32,  # Tăng từ 16 để có kết nối tốt hơn
            ef_construct=400,  # Tăng để có index chất lượng cao hơn
            full_scan_threshold=20000,  # Tăng ngưỡng scan toàn bộ
            max_indexing_threads=0,  # Sử dụng tất cả cores
        )

        # Cấu hình quantization để giảm memory usage
        quantization_config = models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True,
            ),
        )

        # Tạo collection với multi-vector configuration
        vectors_config = {
            'dense-512': models.VectorParams(
                size=512,
                distance=models.Distance[distance.upper()],
                hnsw_config=optimized_hnsw_config,
                quantization_config=quantization_config,
            ),
            'dense-768': models.VectorParams(
                size=768,
                distance=models.Distance[distance.upper()],
                hnsw_config=optimized_hnsw_config,
                quantization_config=quantization_config,
            ),
            'dense-1024': models.VectorParams(
                size=size,
                distance=models.Distance[distance.upper()],
                hnsw_config=optimized_hnsw_config,
                quantization_config=quantization_config,
            ),
            'sparse': models.VectorParams(
                size=768,
                distance=models.Distance[distance.upper()],
                multivector_config=models.MultiVectorConfig(
                    comparator=models.MultiVectorComparator.MAX_SIM
                ),
                hnsw_config=optimized_hnsw_config,
            )
        }

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config,
        )
        
        # Tạo payload index để tăng tốc filtering
        self.client.create_payload_index(
            collection_name=collection_name,
            field_name="text",
            field_schema=models.TextIndexParams(
                type="text",
                tokenizer=models.TokenizerType.MULTILINGUAL,
                min_token_len=2,
                max_token_len=20,
            )
        )
        
        self.logger.info(f"Created optimized collection: {collection_name}")

    async def create_embeddings_async(self, texts: List[str]) -> Dict[str, List[np.ndarray]]:
        """Tạo embeddings async với cache"""
        start_time = time.time()
        
        # Chia texts thành batches
        batch_size = 32
        batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]
        
        all_embeddings = {
            'dense-512': [],
            'dense-768': [],
            'dense-1024': [],
            'sparse': []
        }
        
        for batch in batches:
            batch_embeddings = await self._process_batch_async(batch)
            for key in all_embeddings:
                all_embeddings[key].extend(batch_embeddings[key])
        
        elapsed = time.time() - start_time
        self.metrics['embedding_times'].append(elapsed)
        self.logger.info(f"Generated embeddings for {len(texts)} texts in {elapsed:.2f}s")
        
        return all_embeddings

    async def _process_batch_async(self, batch_texts: List[str]) -> Dict[str, List[np.ndarray]]:
        """Xử lý batch texts async"""
        tasks = []
        
        for text in batch_texts:
            # Tiền xử lý text
            processed_text = self.pre_processing.text_preprocessing_vietnamese(text)
            
            # Tạo task cho từng embedding model
            task = self._get_embeddings_for_text(processed_text)
            tasks.append(task)
        
        # Chạy tất cả tasks song song
        results = await asyncio.gather(*tasks)
        
        # Tổng hợp kết quả
        batch_embeddings = {
            'dense-512': [],
            'dense-768': [], 
            'dense-1024': [],
            'sparse': []
        }
        
        for result in results:
            for key in batch_embeddings:
                batch_embeddings[key].append(result[key])
                
        return batch_embeddings

    async def _get_embeddings_for_text(self, text: str) -> Dict[str, np.ndarray]:
        """Lấy embeddings cho 1 text với cache"""
        embeddings = {}
        
        for model_name, embedding_key in [
            ('model_512', 'dense-512'),
            ('model_768', 'dense-768'), 
            ('model_1024', 'dense-1024'),
            ('model_late_interaction', 'sparse')
        ]:
            cache_key = f"{model_name}_{text}"
            cached_embedding = self.embedding_cache.get(cache_key)
            
            if cached_embedding is not None:
                embeddings[embedding_key] = cached_embedding
                self.metrics['cache_hits'] += 1
            else:
                # Tạo embedding mới
                model = self.models[model_name]
                embedding = await asyncio.get_event_loop().run_in_executor(
                    self.executor, model.embed, text
                )
                embeddings[embedding_key] = embedding
                self.embedding_cache.set(cache_key, embedding)
                self.metrics['cache_misses'] += 1
        
        return embeddings

    async def upsert_points_optimized(self, points_data: List[Tuple[int, str]]):
        """Upsert points với tối ưu hóa batch"""
        batch_size = 100
        total_points = len(points_data)
        
        for i in range(0, total_points, batch_size):
            batch = points_data[i:i + batch_size]
            await self._upsert_batch(batch)
            
            # Progress logging
            progress = min(i + batch_size, total_points)
            self.logger.info(f"Upserted {progress}/{total_points} points")

    async def _upsert_batch(self, batch_data: List[Tuple[int, str]]):
        """Upsert một batch points"""
        # Tạo embeddings cho batch
        texts = [item[1] for item in batch_data]
        embeddings = await self.create_embeddings_async(texts)
        
        # Tạo points
        points = []
        for idx, (point_id, text) in enumerate(batch_data):
            point = PointStruct(
                id=point_id,
                vector={
                    'dense-512': embeddings['dense-512'][idx],
                    'dense-768': embeddings['dense-768'][idx],
                    'dense-1024': embeddings['dense-1024'][idx],
                    'sparse': embeddings['sparse'][idx]
                },
                payload={"text": text}
            )
            points.append(point)
        
        # Upsert batch
        await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: self.client.upsert(self.collection_name, points)
        )

    async def hybrid_search_optimized(self, query: str, limit: int = 25) -> List[str]:
        """Tìm kiếm hybrid tối ưu với fusion"""
        start_time = time.time()
        
        # Check cache
        cache_key = f"{query}_{limit}"
        if cache_key in self.query_cache:
            cached_result, cache_time = self.query_cache[cache_key]
            if time.time() - cache_time < self.cache_config.ttl_seconds:
                self.metrics['cache_hits'] += 1
                return cached_result
        
        # Tiền xử lý query
        processed_query = self.pre_processing.text_preprocessing_vietnamese(query)
        
        # Tạo embeddings cho query
        query_embeddings = await self._get_embeddings_for_text(processed_query)
        
        # Tạo search requests song song
        search_requests = [
            SearchRequest(
                vector=models.NamedVector(
                    name='dense-512',
                    vector=query_embeddings['dense-512']
                ),
                limit=limit * 4,  # Lấy nhiều hơn để fusion
                with_payload=True
            ),
            SearchRequest(
                vector=models.NamedVector(
                    name='dense-768', 
                    vector=query_embeddings['dense-768']
                ),
                limit=limit * 3,
                with_payload=True
            ),
            SearchRequest(
                vector=models.NamedVector(
                    name='dense-1024',
                    vector=query_embeddings['dense-1024']
                ),
                limit=limit * 2,
                with_payload=True
            ),
            SearchRequest(
                vector=models.NamedVector(
                    name='sparse',
                    vector=query_embeddings['sparse']
                ),
                limit=limit,
                with_payload=True
            )
        ]
        
        # Thực hiện search song song
        search_tasks = [
            asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda req=req: self.client.search(
                    collection_name=self.collection_name,
                    query_vector=req.vector,
                    limit=req.limit,
                    with_payload=req.with_payload
                )
            ) for req in search_requests
        ]
        
        search_results = await asyncio.gather(*search_tasks)
        
        # Fusion kết quả với Reciprocal Rank Fusion (RRF)
        fused_results = self._reciprocal_rank_fusion(search_results, limit)
        
        # Cache kết quả
        documents = [result.payload["text"] for result in fused_results]
        self.query_cache[cache_key] = (documents, time.time())
        
        # Clean old cache entries
        self._clean_old_cache()
        
        elapsed = time.time() - start_time
        self.metrics['query_times'].append(elapsed)
        self.metrics['cache_misses'] += 1
        
        self.logger.info(f"Hybrid search completed in {elapsed:.2f}s")
        return documents

    def _reciprocal_rank_fusion(self, search_results: List, final_limit: int) -> List:
        """Fusion kết quả với RRF algorithm"""
        k = 60  # RRF parameter
        scores = {}
        
        # Tính RRF score cho mỗi document
        for rank_weight, results in enumerate(search_results, 1):
            weight = 1.0 / rank_weight  # Weight giảm theo thứ tự model
            
            for rank, result in enumerate(results, 1):
                doc_id = result.id
                rrf_score = weight / (k + rank)
                
                if doc_id not in scores:
                    scores[doc_id] = {'score': 0, 'result': result}
                scores[doc_id]['score'] += rrf_score
        
        # Sắp xếp theo score và trả về top results
        sorted_results = sorted(scores.values(), 
                              key=lambda x: x['score'], reverse=True)
        
        return [item['result'] for item in sorted_results[:final_limit]]

    def _clean_old_cache(self):
        """Xóa cache entries cũ"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, cache_time) in self.query_cache.items()
            if current_time - cache_time > self.cache_config.ttl_seconds
        ]
        
        for key in expired_keys:
            del self.query_cache[key]

    async def re_ranking_optimized(self, query: str, passages: List[str]) -> List[str]:
        """Re-ranking tối ưu với async"""
        if not passages:
            return []
            
        # Import dynamic để tránh load unnecessary
        from langchain_nvidia_ai_endpoints import NVIDIARerank
        from langchain_core.documents import Document
        
        reranker = NVIDIARerank(
            model="nvidia/llama-3.2-nv-rerankqa-1b-v2",
            api_key=os.getenv('API_KEY_RERANKING'),
            top_n=min(len(passages), 20)  # Limit để tăng tốc
        )
        
        # Async reranking
        reranked = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: reranker.compress_documents(
                query=query,
                documents=[Document(page_content=passage) for passage in passages]
            )
        )
        
        # Filter theo relevance score
        filtered_results = [
            doc.page_content for doc in reranked 
            if doc.metadata.get('relevance_score', 0) > 0.1
        ]
        
        return filtered_results

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Lấy metrics hiệu năng"""
        cache_total = self.metrics['cache_hits'] + self.metrics['cache_misses']
        cache_hit_rate = (self.metrics['cache_hits'] / cache_total * 100) if cache_total > 0 else 0
        
        avg_query_time = np.mean(self.metrics['query_times']) if self.metrics['query_times'] else 0
        avg_embedding_time = np.mean(self.metrics['embedding_times']) if self.metrics['embedding_times'] else 0
        
        return {
            'cache_hit_rate': f"{cache_hit_rate:.2f}%",
            'total_queries': len(self.metrics['query_times']),
            'avg_query_time': f"{avg_query_time:.3f}s",
            'avg_embedding_time': f"{avg_embedding_time:.3f}s",
            'cache_size': len(self.query_cache),
            'embedding_cache_size': len(self.embedding_cache.cache)
        }

    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
