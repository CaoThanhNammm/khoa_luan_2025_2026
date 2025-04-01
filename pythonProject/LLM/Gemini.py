from dotenv import load_dotenv
import google.generativeai as generativeai
from google import genai
import os
load_dotenv()

class Gemini:
    def __init__(self, model_name, api_key):
        self.chat = None
        self.model_name = model_name
        self.api_key = api_key

    def load_model(self):
        client = genai.Client(api_key=self.api_key)
        chat = client.chats.create(model=self.model_name)

        self.chat = chat
        print("load model success")

    def encode(self, text):
        client = genai.Client(api_key=self.api_key)

        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text)

        return result.embeddings[0].values


    def generator(self, text):
        response = self.chat.send_message(text)
        return response.text

    def get_history(self):
        for message in self.chat.get_history():
            print(f'role - {message.role}', end=": ")
            print(message.parts[0].text)
