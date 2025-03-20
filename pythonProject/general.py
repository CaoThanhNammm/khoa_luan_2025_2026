import json
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from transformers import AutoModel
from qdrant_client import QdrantClient, models
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer
import py_vncorenlp
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as generativeai
import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, NLTKTextSplitter, SpacyTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader, PyPDFLoader, UnstructuredPDFLoader, PyPDFium2Loader, PDFMinerLoader
from google import genai


def encode(content):
    client = genai.Client(api_key=os.getenv("API_KEY"))

    result = client.models.embed_content(
        model="text-embedding-004",
        contents=content)

    return result.embeddings[0].values

def load_model(model, system_instruction):
    generativeai.configure(api_key=os.getenv("API_KEY"))
    model = generativeai.GenerativeModel(
        model_name=model,
        system_instruction=system_instruction)

    print("load model success")
    return model

def load_vncorenlp():
    return py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=r'C:\Users\Nam\Desktop\vncorenlp')

def string_to_json(text):
    removed_special = text.replace("```", "").replace("json", "")
    removed_special = removed_special.strip()
    return json.loads(removed_special)

def text_preprocessing_vietnamese(text, vncorenlp):
    # 1. Chuyển thành chữ thường
    text = text.lower()

    # 2. Loại bỏ dấu câu
    text = re.sub(r'[^\w\s]', '', text)

    # 4. Xóa khoảng trắng thừa
    text = text.strip()

    # 5. Tách từ (Tokenization)
    output = vncorenlp.word_segment(text)
    result_string = ' '.join(output)
    return result_string


# kết nối đến db
def load_db(url):
    client = QdrantClient(url=url)
    print('load database success')
    return client

# ------------------------------------------------------------------------------------------- #

def compute_vector(text, model, tokenizer):
    tokens = tokenizer(text, return_tensors="pt")
    output = model(**tokens)
    logits, attention_mask = output.logits, tokens.attention_mask
    relu_log = torch.log(1 + torch.relu(logits))
    weighted_log = relu_log * attention_mask.unsqueeze(-1)
    max_val, _ = torch.max(weighted_log, dim=1)
    vec = max_val.squeeze()

    return vec, tokens

def extract_and_map_sparse_vector(vector, tokenizer):
    # Extract indices and values of non-zero elements in the vector
    cols = vector.nonzero().squeeze().cpu().tolist()
    weights = vector[cols].cpu().tolist()

    # Map indices to tokens and create a dictionary
    idx2token = {idx: token for token, idx in tokenizer.get_vocab().items()}
    token_weight_dict = {idx2token[idx]: round(weight, 2) for idx, weight in zip(cols, weights)}

    # Sort the dictionary by weights in descending order
    sorted_token_weight_dict = {k: v for k, v in sorted(token_weight_dict.items(), key=lambda item: item[1], reverse=True)}

    return sorted_token_weight_dict