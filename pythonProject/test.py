# from LLM.Gemini import Gemini
# from dotenv import load_dotenv
# load_dotenv()
# import os
# from ModelLLM.EmbeddingFactory import EmbeddingFactory
# import numpy as np
#
# # Hàm tính cosine similarity
# def cosine_similarity(vec1, vec2):
#     # Chuyển đổi về numpy array nếu chưa phải
#     vec1 = np.array(vec1)
#     vec2 = np.array(vec2)
#
#     # Tính dot product
#     dot_product = np.dot(vec1, vec2)
#
#     # Tính norm (độ dài vector)
#     norm_vec1 = np.linalg.norm(vec1)
#     norm_vec2 = np.linalg.norm(vec2)
#
#     # Tính cosine similarity
#     if norm_vec1 == 0 or norm_vec2 == 0:
#         return 0.0
#     return dot_product / (norm_vec1 * norm_vec2)
#
# model_embedding_1024_name = os.getenv("MODEL_EMBEDDING_1024")
# factory = EmbeddingFactory()
# model_1024 = factory.create_embedding_model(model_embedding_1024_name)
# model_embed_1024, tokenizer_1024 = model_1024.load_model()
#
# text_1 = "tôi là vui"
# text_2 = "tôi có niềm vui"
#
# text_1_embed = model_1024.embed(model_embed_1024, tokenizer_1024, text_1)
# text_2_embed = model_1024.embed(model_embed_1024, tokenizer_1024, text_2)
# similarity = cosine_similarity(text_1_embed, text_2_embed)
#
# print(f"{text_1}: {text_1_embed}")
# print(f"{text_2}: {text_2_embed}")
# print(f"size vector tôi là vui: {len(text_1_embed)}")
# print(f"size vector tôi có niềm vui: {len(text_2_embed)}")
#
# print(f"Cosine similarity: {similarity}")
#


f = 'ASDS'
if f:
    print('a')
else:
    print('b')
