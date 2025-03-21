from transformers import AutoModel
from transformers import AutoTokenizer
from dotenv import load_dotenv
from ModelLLM.AModelLLM import IModelLLM
load_dotenv()

class ModelLateInteraction(IModelLLM):
    def load_model(self):
        model = AutoModel.from_pretrained(self.name)
        tokenizer = AutoTokenizer.from_pretrained(self.name)
        print("load model embedding late interaction success")
        return model, tokenizer

    def embed(self, model_embedding, tokenizer, text_pre_processed):
        query_tokens = tokenizer(text_pre_processed, return_tensors='pt', truncation=True, padding=True)
        query_embedding = model_embedding(**query_tokens).last_hidden_state.detach().numpy()[0]
        return query_embedding[: 10]

    def get_dimension(self):
        return 123