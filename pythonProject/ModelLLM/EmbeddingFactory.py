import os
from dotenv import load_dotenv
from ModelLLM.ModelEmbedding1024 import ModelEmbedding1024
from ModelLLM.ModelEmbedding768 import ModelEmbedding768
from ModelLLM.ModelEmbedding512 import ModelEmbedding512
from ModelLLM.ModelLateInteraction import ModelLateInteraction
load_dotenv()

class EmbeddingFactory:
    @staticmethod
    def create_embed_model(embed_model_name):
        model_embedding_1024_name = os.getenv("MODEL_EMBEDDING_1024")
        model_embedding_768_name = os.getenv("MODEL_EMBEDDING_768")
        model_embedding_512_name = os.getenv("MODEL_EMBEDDING_512")
        model_late_interaction_name = os.getenv("MODEL_LATE_INTERACTION")

        if embed_model_name == model_embedding_1024_name:
            return ModelEmbedding1024(embed_model_name)
        elif embed_model_name == model_embedding_768_name:
            return ModelEmbedding768(embed_model_name)
        elif embed_model_name == model_embedding_512_name:
            return ModelEmbedding512(embed_model_name)
        elif embed_model_name == model_late_interaction_name:
            return ModelLateInteraction(embed_model_name)
        else:
            raise ValueError(f"Không hỗ trợ")