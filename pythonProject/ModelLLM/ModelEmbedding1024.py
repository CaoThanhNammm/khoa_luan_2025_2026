from ModelLLM.AModelLLM import IModelLLM
from transformers import AutoModel
import torch
from transformers import AutoTokenizer
from dotenv import load_dotenv
load_dotenv()

class ModelEmbedding1024(IModelLLM):
    def load_model(self):
        phobert = AutoModel.from_pretrained(self.name)
        tokenizer = AutoTokenizer.from_pretrained(self.name)
        print("load model embedding 1024 success")
        return phobert, tokenizer

    def embed(self, model_embedding, tokenizer, text, max_length=256):
        # Tokenize đoạn văn
        inputs = tokenizer(
            text,
            max_length=max_length,
            padding=True,
            truncation=True,
            return_tensors="pt"  # Trả về PyTorch tensors
        )

        # Đưa model vào chế độ evaluation
        model_embedding.eval()

        # Không tính gradient để tiết kiệm bộ nhớ và tăng tốc
        with torch.no_grad():
            # Lấy output từ model
            outputs = model_embedding(**inputs)

            # Lấy hidden states từ layer cuối cùng
            last_hidden_states = outputs.last_hidden_state

            # Tính mean pooling trên tất cả các token để có được sentence embedding
            # Loại bỏ dimension batch (squeeze) và lấy mean theo dimension time steps
            embedding = torch.mean(last_hidden_states, dim=1).squeeze()

        return embedding

    def get_dimension(self):
        return 1024