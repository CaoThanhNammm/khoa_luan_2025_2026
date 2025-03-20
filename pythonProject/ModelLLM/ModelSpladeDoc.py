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

class ModelSpladeDoc(IModelLLM):
    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.name)
        model = AutoModelForMaskedLM.from_pretrained(self.name)
        print("load model embedding splade success")
        return model, tokenizer

    def embed(self, model_embedding, tokenizer, text_pre_processed):
        tokens = tokenizer(text_pre_processed, return_tensors="pt")
        output = model_embedding(**tokens)
        logits, attention_mask = output.logits, tokens.attention_mask
        relu_log = torch.log(1 + torch.relu(logits))
        weighted_log = relu_log * attention_mask.unsqueeze(-1)
        max_val, _ = torch.max(weighted_log, dim=1)
        vec = max_val.squeeze()

        return vec, tokens

    def get_dimension(self):
        return 1024