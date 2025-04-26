from dotenv import load_dotenv
import google.generativeai as generativeai
from google import genai
import os
load_dotenv()
from sentence_transformers import SentenceTransformer

class Gemini:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key

        self.client = genai.Client(api_key=self.api_key)
        self.model_encode = SentenceTransformer('intfloat/multilingual-e5-large')
        # chat = client.create(model=self.model_name)
        # self.chat = chat
        print("load model success")


    def encode(self, text):
        return self.model_encode.encode(text)

    def generator(self, text):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[text]
        )
        return response.text.strip()