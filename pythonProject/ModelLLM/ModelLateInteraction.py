import json
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from transformers import AutoModel
from qdrant_client import QdrantClient, models
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer
import py_vncorenlp
from dotenv import load_dotenv

from ModelLLM.AModelLLM import IModelLLM

load_dotenv()
import google.generativeai as generativeai
import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, NLTKTextSplitter, SpacyTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader, PyPDFLoader, UnstructuredPDFLoader, PyPDFium2Loader, PDFMinerLoader
from google import genai

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