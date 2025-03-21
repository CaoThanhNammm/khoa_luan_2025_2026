from PreProcessing.PreProcessing import PreProcessing
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from ModelLLM.EmbeddingFactory import EmbeddingFactory
load_dotenv()
from VectorDatabase.Qdrant import Qdrant
import LLM.prompt

def rewrite_query(model, query):
    prompt = PromptTemplate(input_variables=["question"], template=LLM.prompt.rewrite_query)
    formatted_prompt = prompt.format(question=query)

    response = model.generate_content(formatted_prompt)

    return response.text

if __name__ == "__main__":
    # 1. sử dụng factory để khởi tạo các clas model embed
    model_embedding_1024_name = os.getenv("MODEL_EMBEDDING_1024")
    model_embedding_768_name = os.getenv("MODEL_EMBEDDING_768")
    model_embedding_512_name = os.getenv("MODEL_EMBEDDING_512")
    model_late_interaction_name = os.getenv("MODEL_LATE_INTERACTION")

    factory = EmbeddingFactory()
    model_1024 = factory.create_embedding_model(model_embedding_1024_name)
    model_768 = factory.create_embedding_model(model_embedding_768_name)
    model_512 = factory.create_embedding_model(model_embedding_512_name)
    model_late_interaction = factory.create_embedding_model(model_late_interaction_name)

    model_embed_1024, tokenizer_1024 = model_1024.load_model()
    model_embed_768, tokenizer_768 = model_768.load_model()
    model_embed_512 = model_512.load_model()
    model_embed_late_interaction, tokenizer_late_interaction = model_late_interaction.load_model()

    # 3. Khởi tạo client Qdrant
    collection_name = os.getenv("NAME_COLLECTION")
    qdrant = Qdrant("localhost", 6333, model_1024, model_768, model_512, model_late_interaction, collection_name)

    # 5. truy vấn database
    query  = """yêu cầu chuẩn đầu ra tin học không chuyên của ngành Môi trường và Tài nguyên là gì"""

    # 6. Tiền xử lý
    pre_processing = PreProcessing()
    save_dir = r'C:\Users\Nam\Desktop\vncorenlp'
    vncorenlp = pre_processing.load_vncorenlp(save_dir)
    text_pre_processed = pre_processing.text_preprocessing_vietnamese(query.strip(), vncorenlp)

    # 6. embedding query, embedding late interaction query
    text_embedded_1024 = model_1024.embed(model_embed_1024, tokenizer_1024, text_pre_processed)
    text_embedded_768 = model_768.embed(model_embed_768, tokenizer_768, text_pre_processed)
    text_embedded_512 = model_512.embed(model_embed_512, text_pre_processed)
    embedded_late_interaction = model_embed_late_interaction.embed(model_late_interaction, tokenizer_late_interaction, text_pre_processed)

    # 9. query từ database
    results = qdrant.query_from_db(text_embedded_1024, text_embedded_768, text_embedded_512, embedded_late_interaction)
    print(results)


    # json_query_text = []
    # print("\n----------------------------------------------------------------------------------------------------------------------------------------------------------")
    # for result in results:
    #     json_query_text.append(result.payload["text"])
    #     print(result.payload["text"], "\n-----------------------------------------------------------------------------------------------------------")
    #
    #
    # # print("START RE RANKING")
    # # 10. re-ranking
    # re_ranking_query_text = qdrant.re_ranking(query, json_query_text)
    # for i in range(len(re_ranking_query_text)):
    #     logit = re_ranking_query_text[i].metadata['relevance_score']
    #     text = re_ranking_query_text[i].page_content
    #
    #     print(f"{i: } ---- {logit}: {text}\n-----------------------------------------------------------------------------------")