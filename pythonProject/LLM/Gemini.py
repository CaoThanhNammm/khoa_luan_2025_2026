from dotenv import load_dotenv
import google.generativeai as generativeai
from google import genai
import os
load_dotenv()

class Gemini:
    def __init__(self, model_name, api_key):
        self.model = None
        self.model_name = model_name
        self.api_key = api_key


    def load_model(self):
        generativeai.configure(api_key=self.api_key)
        model = generativeai.GenerativeModel(
            model_name=self.model_name)
        self.model = model
        print("load model success")

    def encode(self, text):
        client = genai.Client(api_key=self.api_key)

        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text)

        return result.embeddings[0].values

    def generator(self, text):
        response = self.model.generate_content(text)
        return response.text
