from ModelLLM.AModelLLM import IModelLLM
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()

class ModelEmbedding512(IModelLLM):
    def load_model(self):
        model = SentenceTransformer(self.name)
        print("load model embedding 512 success")
        return model

    def embed(self,  model_embedding, tokenizer, text_pre_processed):
        return model_embedding.encode(text_pre_processed)

    def get_dimension(self):
        return 512