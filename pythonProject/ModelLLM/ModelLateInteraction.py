from transformers import AutoModel
from transformers import AutoTokenizer
from dotenv import load_dotenv
load_dotenv()

class ModelLateInteraction:
    def __init__(self, name):
        self.name = name
        model_embedding, tokenizer = self.load_model()

        self.model_embedding = model_embedding
        self.tokenizer = tokenizer

    def load_model(self):
        model = AutoModel.from_pretrained(self.name)
        tokenizer = AutoTokenizer.from_pretrained(self.name)
        print("load model embedding late interaction success")
        return model, tokenizer

    def embed(self, text):
        query_tokens = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        query_embedding = self.model_embedding(**query_tokens).last_hidden_state.detach().numpy()[0]
        return query_embedding[: 10]