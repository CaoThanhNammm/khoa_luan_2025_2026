#!/usr/bin/env python3
"""
Fallback model configuration for the optimization system
"""

from optimization.config import SystemConfig

def get_fallback_config():
    """Get fallback configuration with simpler models"""
    fallback_config = SystemConfig()
    
    # Use simpler models that don't require trust_remote_code
    fallback_config.embedding_models = {
        'model_512': "sentence-transformers/distiluse-base-multilingual-cased-v2",
        'model_768': "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        'model_1024': "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        'model_late_interaction': "sentence-transformers/msmarco-distilbert-base-v4"
    }
    
    return fallback_config

def is_model_available(model_name):
    """Check if a model is available without downloading"""
    try:
        from huggingface_hub import model_info
        info = model_info(model_name)
        return True
    except Exception:
        return False
