"""
Tối ưu hóa Factory pattern cho Embedding Models
Cải tiến:
1. Lazy loading models
2. Model pooling và reuse
3. Memory management
4. Batch processing optimization
5. GPU utilization optimization
"""

import torch
import asyncio
import threading
from typing import Dict, List, Optional, Any, Union
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import gc
import psutil
import time
import logging
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class ModelConfig:
    """Cấu hình model"""
    name: str
    device: str = "auto"
    max_batch_size: int = 32
    cache_size: int = 1000
    enable_gpu: bool = True

class ModelPool:
    """Pool để quản lý và tái sử dụng models"""
    
    def __init__(self, max_models: int = 4):
        self.models = {}
        self.model_usage = {}
        self.max_models = max_models
        self.lock = threading.RLock()
        
    def get_model(self, model_name: str, model_class, *args, **kwargs):
        """Lấy model từ pool hoặc tạo mới"""
        with self.lock:
            if model_name not in self.models:
                if len(self.models) >= self.max_models:
                    # Evict least used model
                    least_used = min(self.model_usage.keys(), 
                                   key=lambda k: self.model_usage[k])
                    del self.models[least_used]
                    del self.model_usage[least_used]
                    gc.collect()
                
                self.models[model_name] = model_class(*args, **kwargs)
                self.model_usage[model_name] = 0
            
            self.model_usage[model_name] += 1
            return self.models[model_name]

class OptimizedEmbeddingFactory:
    """Factory tối ưu hóa cho embedding models"""
    
    def __init__(self, enable_gpu: bool = True, max_models_in_memory: int = 4):
        self.enable_gpu = enable_gpu
        self.device = self._get_optimal_device()
        self.model_pool = ModelPool(max_models_in_memory)
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Performance monitoring
        self.metrics = {
            'model_loads': 0,
            'embeddings_generated': 0,
            'total_time': 0,
            'gpu_usage': []
        }
        
        self.logger = logging.getLogger(__name__)
        
    def _get_optimal_device(self) -> str:
        """Xác định device tối ưu"""
        if not self.enable_gpu:
            return "cpu"
            
        if torch.cuda.is_available():
            # Chọn GPU có memory nhiều nhất
            gpu_count = torch.cuda.device_count()
            best_gpu = 0
            max_memory = 0
            
            for i in range(gpu_count):
                memory = torch.cuda.get_device_properties(i).total_memory
                if memory > max_memory:
                    max_memory = memory
                    best_gpu = i
                    
            return f"cuda:{best_gpu}"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    @lru_cache(maxsize=128)
    def create_embed_model(self, model_name: str, config: Optional[ModelConfig] = None):
        """Tạo embedding model với caching"""
        start_time = time.time()
        
        if config is None:
            config = ModelConfig(name=model_name, device=self.device)
        
        # Xác định loại model và tạo
        if "multilingual-e5" in model_name:
            model = self.model_pool.get_model(
                model_name, 
                OptimizedE5Model, 
                model_name, 
                config
            )
        elif "gte-multilingual" in model_name:
            model = self.model_pool.get_model(
                model_name,
                OptimizedGTEModel,
                model_name,
                config
            )
        elif "distiluse-base" in model_name:
            model = self.model_pool.get_model(
                model_name,
                OptimizedDistilUseModel,
                model_name,
                config
            )
        elif "colbert" in model_name:
            model = self.model_pool.get_model(
                model_name,
                OptimizedColBERTModel,
                model_name,
                config
            )
        else:
            model = self.model_pool.get_model(
                model_name,
                OptimizedGenericModel,
                model_name,
                config
            )
        
        self.metrics['model_loads'] += 1
        load_time = time.time() - start_time
        self.logger.info(f"Model {model_name} loaded in {load_time:.2f}s on {config.device}")
        
        return model

class BaseOptimizedModel:
    """Base class cho optimized embedding models"""
    
    def __init__(self, model_name: str, config: ModelConfig):
        self.model_name = model_name
        self.config = config
        self.device = config.device if config.device != "auto" else self._get_device()
        self.model = None
        self.tokenizer = None
        self._load_model()
        
        # Cache và metrics
        self.embedding_cache = {}
        self.batch_cache = {}
        self.metrics = {
            'embeddings_count': 0,
            'cache_hits': 0,
            'batch_processing_time': []
        }
        
    def _get_device(self) -> str:
        """Auto detect device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        return "cpu"
    
    def _load_model(self):
        """Load model - implement in subclasses"""
        raise NotImplementedError
    
    @contextmanager
    def _gpu_memory_context(self):
        """Context manager để quản lý GPU memory"""
        if "cuda" in self.device:
            torch.cuda.empty_cache()
            initial_memory = torch.cuda.memory_allocated()
        
        try:
            yield
        finally:
            if "cuda" in self.device:
                final_memory = torch.cuda.memory_allocated()
                memory_used = final_memory - initial_memory
                self.logger.debug(f"GPU memory used: {memory_used / 1024**2:.2f} MB")
                torch.cuda.empty_cache()

    async def embed_async(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Async embedding generation"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.embed, text)

    def embed_batch_optimized(self, texts: List[str], batch_size: Optional[int] = None) -> List[List[float]]:
        """Optimized batch embedding"""
        if not texts:
            return []
            
        batch_size = batch_size or self.config.max_batch_size
        start_time = time.time()
        
        # Check cache for entire batch
        cache_key = hash(tuple(texts))
        if cache_key in self.batch_cache:
            self.metrics['cache_hits'] += 1
            return self.batch_cache[cache_key]
        
        # Process in batches
        all_embeddings = []
        
        with self._gpu_memory_context():
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_embeddings = self._process_batch(batch)
                all_embeddings.extend(batch_embeddings)
        
        # Cache result
        self.batch_cache[cache_key] = all_embeddings
        if len(self.batch_cache) > 100:  # Limit cache size
            oldest_key = next(iter(self.batch_cache))
            del self.batch_cache[oldest_key]
        
        processing_time = time.time() - start_time
        self.metrics['batch_processing_time'].append(processing_time)
        self.metrics['embeddings_count'] += len(texts)
        
        return all_embeddings

    def _process_batch(self, batch_texts: List[str]) -> List[List[float]]:
        """Process a single batch - implement in subclasses"""
        raise NotImplementedError

    def get_model_info(self) -> Dict[str, Any]:
        """Lấy thông tin model"""
        return {
            'model_name': self.model_name,
            'device': self.device,
            'config': self.config,
            'embeddings_generated': self.metrics['embeddings_count'],
            'cache_hits': self.metrics['cache_hits'],
            'avg_batch_time': (
                sum(self.metrics['batch_processing_time']) / 
                len(self.metrics['batch_processing_time'])
                if self.metrics['batch_processing_time'] else 0
            )
        }

class OptimizedE5Model(BaseOptimizedModel):
    """Optimized E5 embedding model"""
    def _load_model(self):
        from sentence_transformers import SentenceTransformer
        
        self.model = SentenceTransformer(
            self.model_name, 
            device=self.device,
            trust_remote_code=True
        )
        # Optimize model for inference
        self.model.eval()
        if "cuda" in self.device:
            self.model.half()  # Use FP16 for faster inference
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Generate embeddings"""
        is_single_text = isinstance(text, str)
        if is_single_text:
            text = [text]
            
        with self._gpu_memory_context():
            embeddings = self.model.encode(
                text,
                batch_size=self.config.max_batch_size,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
        
        result = embeddings.tolist()
        # Return single embedding vector for single text input
        if is_single_text:
            return result[0]
        return result
    
    def _process_batch(self, batch_texts: List[str]) -> List[List[float]]:
        return self.embed(batch_texts)

class OptimizedGTEModel(BaseOptimizedModel):
    """Optimized GTE embedding model"""
    def _load_model(self):
        from sentence_transformers import SentenceTransformer
        
        self.model = SentenceTransformer(
            self.model_name, 
            device=self.device,
            trust_remote_code=True
        )
        self.model.eval()
        if "cuda" in self.device:
            self.model.half()
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        is_single_text = isinstance(text, str)
        if is_single_text:
            text = [text]
            
        with self._gpu_memory_context():
            embeddings = self.model.encode(
                text,
                batch_size=self.config.max_batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
        
        result = embeddings.tolist()
        # Return single embedding vector for single text input
        if is_single_text:
            return result[0]
        return result
    
    def _process_batch(self, batch_texts: List[str]) -> List[List[float]]:
        return self.embed(batch_texts)

class OptimizedDistilUseModel(BaseOptimizedModel):
    """Optimized DistilUSE embedding model"""
    
    def _load_model(self):
        from sentence_transformers import SentenceTransformer
        
        self.model = SentenceTransformer(
            self.model_name, 
            device=self.device,
            trust_remote_code=True
        )
        self.model.eval()
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        is_single_text = isinstance(text, str)
        if is_single_text:
            text = [text]
            
        with self._gpu_memory_context():
            embeddings = self.model.encode(
                text,
                batch_size=self.config.max_batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
        
        result = embeddings.tolist()
        # Return single embedding vector for single text input
        if is_single_text:
            return result[0]
        return result
    
    def _process_batch(self, batch_texts: List[str]) -> List[List[float]]:
        return self.embed(batch_texts)

class OptimizedColBERTModel(BaseOptimizedModel):
    """Optimized ColBERT late interaction model"""
    
    def _load_model(self):
        # Implement ColBERT loading logic
        from sentence_transformers import SentenceTransformer
        
        self.model = SentenceTransformer(
            self.model_name, 
            device=self.device,
            trust_remote_code=True
        )
        self.model.eval()
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        is_single_text = isinstance(text, str)
        if is_single_text:
            text = [text]
            
        with self._gpu_memory_context():
            # ColBERT specific processing
            embeddings = self.model.encode(
                text,
                batch_size=min(8, self.config.max_batch_size),  # Smaller batch for ColBERT
                show_progress_bar=False,
                convert_to_numpy=True
            )
        
        result = embeddings.tolist()
        # Return single embedding vector for single text input
        if is_single_text:
            return result[0]
        return result
    
    def _process_batch(self, batch_texts: List[str]) -> List[List[float]]:
        return self.embed(batch_texts)

class OptimizedGenericModel(BaseOptimizedModel):
    """Generic optimized embedding model"""
    
    def _load_model(self):
        from sentence_transformers import SentenceTransformer
        
        self.model = SentenceTransformer(
            self.model_name, 
            device=self.device,
            trust_remote_code=True
        )
        self.model.eval()
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        is_single_text = isinstance(text, str)
        if is_single_text:
            text = [text]
            
        with self._gpu_memory_context():
            embeddings = self.model.encode(
                text,
                batch_size=self.config.max_batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
        
        result = embeddings.tolist()
        # Return single embedding vector for single text input
        if is_single_text:
            return result[0]
        return result
    
    def _process_batch(self, batch_texts: List[str]) -> List[List[float]]:
        return self.embed(batch_texts)

class SystemResourceMonitor:
    """Monitor system resources for optimization"""
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Lấy memory usage"""
        memory = psutil.virtual_memory()
        return {
            'total_gb': memory.total / 1024**3,
            'available_gb': memory.available / 1024**3,
            'used_percent': memory.percent
        }
    
    @staticmethod
    def get_gpu_memory() -> Dict[str, Any]:
        """Lấy GPU memory info"""
        if not torch.cuda.is_available():
            return {'available': False}
        
        gpu_info = {}
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            allocated = torch.cuda.memory_allocated(i) / 1024**3
            cached = torch.cuda.memory_reserved(i) / 1024**3
            total = props.total_memory / 1024**3
            
            gpu_info[f'gpu_{i}'] = {
                'name': props.name,
                'total_gb': total,
                'allocated_gb': allocated,
                'cached_gb': cached,
                'free_gb': total - allocated
            }
        
        return gpu_info
    
    @staticmethod
    def recommend_batch_size(model_size_mb: float) -> int:
        """Recommend optimal batch size based on available memory"""
        memory = psutil.virtual_memory()
        available_gb = memory.available / 1024**3
        
        # Conservative estimation
        if available_gb > 16:
            return 64
        elif available_gb > 8:
            return 32
        elif available_gb > 4:
            return 16
        else:
            return 8
