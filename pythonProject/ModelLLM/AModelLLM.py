from abc import ABC, abstractmethod

class IModelLLM(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def embed(self, model_embedding, tokenizer, text):
        pass

    @abstractmethod
    def get_dimension(self):
        pass

