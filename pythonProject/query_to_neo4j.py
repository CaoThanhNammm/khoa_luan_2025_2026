import general
from dotenv import load_dotenv
import requests
load_dotenv()
import prompt
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain_core.documents import Document
import general
import google.generativeai as genai
from qdrant_client import models
import os
from dotenv import load_dotenv
load_dotenv()

driver = general.connect_to_graph_db()

def run_cypher_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]


# Hàm tạo truy vấn kiểm tra theo định dạng MATCH-RETURN
def generate_match_return_query(json_data):
    relationships = json_data["relationships"]
    entities = json_data["entities"]

    check_queries = []

    # Tạo truy vấn MATCH-RETURN cho từng relationship
    for rel in relationships:
        source_type = next(e["type"] for e in entities if e["name"] == rel["source"])
        target_type = next(e["type"] for e in entities if e["name"] == rel["target"])

        query = (
            f"MATCH (s:{source_type} {{name: '{rel['source']}'}})-[r:{rel['relation']}]->(t:{target_type} {{name: '{rel['target']}'}})\n"
            f"RETURN s.name AS source_name, t.name AS target_name, type(r) AS relation_type"
        )
        check_queries.append(query)

    return check_queries

# B1. tải thư viện để tiền xử lý dữ liệu và tên llm
vncorenlp = general.load_vncorenlp()
model_name = os.getenv("model")

# B2. lấy câu hỏi
question = "yêu cầu chuẩn đầu ra tin học không chuyên của ngành Môi trường và Tài nguyên là gì?"
# B3. tiền xử lý dữ liệu
pre_process_question = general.text_preprocessing_vietnamese(question, vncorenlp) + "Hãy trích xuất entities và relationship dựa trên yêu cầu của prompt mà tôi đã đính kèm"
# B3. sử dụng llm để tự động trích xuất entities và relationship
model = general.load_model(model_name, prompt.prompt_extract_entities_relationship())
response = model.generate_content(pre_process_question).text
# B4. tiền xử lý dữ liệu mà llm phản hổi là format json hoàn chỉnh
extract_entities_relationship = general.extract_relations_from_model_output(response) # json

# B5. tạo các câu cypher query để truy xuất dữ liệu từ neo4j
query_cypher = generate_match_return_query(extract_entities_relationship)

# B6. chạy tất cả các query
for j, query in enumerate(query_cypher):
    print(f"Query {j + 1}:")
    print(query)
    result = run_cypher_query(query)

    # In kết quả
    print("\nResult:")
    for record in result:
        print(f"Source: {record['source_name']}, Target: {record['target_name']}, Relation: {record['relation_type']}")

driver.close()











