import os
from dotenv import load_dotenv
from ModelLLM.ModelEmbedding1024 import ModelEmbedding1024
from ModelLLM.ModelEmbedding768 import ModelEmbedding768
from ModelLLM.ModelEmbedding512 import ModelEmbedding512
from ModelLLM.ModelLateInteraction import ModelLateInteraction
load_dotenv()

class EmbeddingFactory:
    @staticmethod
    def create_embedding_model(embed_model_name):
        model_embedding_1024_name = os.getenv("model_embedding_1024")
        model_embedding_768_name = os.getenv("model_embedding_768")
        model_embedding_512_name = os.getenv("model_embedding_512")
        model_late_interaction_name = os.getenv("model_late_interaction")

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