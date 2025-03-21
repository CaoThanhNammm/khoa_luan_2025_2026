from dotenv import load_dotenv
load_dotenv()
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as generativeai
from google import genai

class Gemini:
    def __init__(self, api_key):
        self.api_key = api_key

    def load_model(self, model_name, system_instruction):
        generativeai.configure(api_key=self.api_key)
        model = generativeai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction)

        print("load model success")
        return model

    def encode(self, text):
        client = genai.Client(api_key=self.api_key)

        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text)

        return result.embeddings[0].values
