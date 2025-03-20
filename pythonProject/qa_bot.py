from dotenv import load_dotenv

load_dotenv()
import general
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
import os
from dotenv import load_dotenv

from ModelLLM.EmbeddingFactory import EmbeddingFactory
load_dotenv()
from vector_database.VectorDatabase import VectorDatabase

def rewrite_query(model, query):
    system_rewrite = """
    ("system", "Bạn là một trợ lý hữu ích, tạo ra nhiều truy vấn tìm kiếm dựa trên một truy vấn đầu vào duy nhất.
    Thực hiện mở rộng truy vấn. Nếu có nhiều cách phổ biến để diễn đạt một câu hỏi của người dùng hoặc 
    có các từ đồng nghĩa phổ biến cho các từ khóa trong câu hỏi, hãy đảm bảo trả về nhiều phiên bản của truy vấn với các cách diễn đạt khác nhau.
    Nếu có các từ viết tắt hoặc từ bạn không quen thuộc, đừng cố gắng diễn đạt lại chúng.
    Trả về 3 phiên bản khác nhau của câu hỏi.")
    
    ("human", {question})
    """

    prompt = PromptTemplate(input_variables=["question"], template=system_rewrite)
    formatted_prompt = prompt.format(question=query)

    response = model.generate_content(formatted_prompt)

    return response.text

if __name__ == "__main__":
    # 1. sử dụng factory để khởi tạo các clas model embed
    model_embedding_1024_name = os.getenv("model_embedding_1024")
    model_embedding_768_name = os.getenv("model_embedding_768")
    model_embedding_512_name = os.getenv("model_embedding_512")
    model_late_interaction_name = os.getenv("model_late_interaction")
    model_splade_query_name = os.getenv("model_splade_query")

    factory = EmbeddingFactory()
    model_1024 = factory.create_embedding_model(model_embedding_1024_name)
    model_768 = factory.create_embedding_model(model_embedding_768_name)
    model_512 = factory.create_embedding_model(model_embedding_512_name)
    model_late_interaction = factory.create_embedding_model(model_late_interaction_name)
    model_splade_query = factory.create_embedding_model(model_splade_query_name)

    model_embed_1024, tokenizer_1024 = model_1024.load_model()
    model_embed_768, tokenizer_768 = model_768.load_model()
    model_embed_512 = model_512.load_model()
    model_embed_late_interaction, tokenizer_late_interaction = model_late_interaction.load_model()
    model_splade_query, tokenizer_splade_query = model_splade_query.load_model()

    # 3. Khởi tạo client Qdrant
    collection_name = os.getenv("name_collection")
    qdrant = VectorDatabase("localhost", 6333, model_1024, model_768, model_512, model_late_interaction, model_splade_query, collection_name)

    # 5. truy vấn database
    query  = """yêu cầu chuẩn đầu ra tin học không chuyên của ngành Môi trường và Tài nguyên là gì"""

    # 6. Tiền xử lý
    vncorenlp = general.load_vncorenlp()
    text_pre_processed = general.text_preprocessing_vietnamese(query.strip(), vncorenlp)

    # 6. embedding query
    text_embedded_1024 = model_1024.embed(model_embed_1024, tokenizer_1024, text_pre_processed)
    text_embedded_768 = model_768.embed(model_embed_768, tokenizer_768, text_pre_processed)
    text_embedded_512 = model_512.embed(model_embed_512, text_pre_processed)

    # 7. embedding splade query
    doc_vec, doc_tokens = general.compute_vector(text_pre_processed, model=model_splade_query, tokenizer=tokenizer_splade_query)
    sorted_tokens_doc = general.extract_and_map_sparse_vector(doc_vec, tokenizer_splade_query)

    indices = tokenizer_splade_query.convert_tokens_to_ids(sorted_tokens_doc)
    values = list(sorted_tokens_doc.values())

    # 8. embedding late interaction query
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