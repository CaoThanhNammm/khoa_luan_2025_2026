from ModelLLM.AModelLLM import IModelLLM
from transformers import AutoModel
import torch
from transformers import AutoTokenizer
from dotenv import load_dotenv
load_dotenv()

class ModelEmbedding768(IModelLLM):
    def load_model(self):
        phobert = AutoModel.from_pretrained(self.name)
        tokenizer = AutoTokenizer.from_pretrained(self.name)
        print("load model embedding 768 success")
        return phobert, tokenizer

    def embed(self, model_embedding, tokenizer, text_pre_processed):
        input_ids = torch.tensor([tokenizer.encode(text_pre_processed)])

        with torch.no_grad():
            features = model_embedding(input_ids)  # Models outputs are now tuples
            embeddings = features.last_hidden_state

        cls_embedding = embeddings[:, 0, :]
        return cls_embedding.numpy()[0]

    def get_dimension(self):
        return 768