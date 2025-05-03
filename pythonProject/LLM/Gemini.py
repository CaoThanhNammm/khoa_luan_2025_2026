from dotenv import load_dotenv
from google import genai
load_dotenv()
from sentence_transformers import SentenceTransformer

class Gemini:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key

        client = genai.Client(api_key=self.api_key)
        self.model_encode = SentenceTransformer('intfloat/multilingual-e5-large')
        self.chat = client.chats.create(model=self.model_name)
        print("load model success")

    def encode(self, text):
        return self.model_encode.encode(text)

    def generator(self, text):
        response = self.chat.send_message(text)

        return response.text.strip()