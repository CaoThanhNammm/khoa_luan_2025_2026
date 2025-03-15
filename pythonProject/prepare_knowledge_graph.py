import time
from neo4j import GraphDatabase
from dotenv import load_dotenv

import prompt

load_dotenv()
import general
import os

def create_entities(tx, entities):
    # Loại bỏ duplicates trong danh sách entities trước khi gửi vào Neo4j
    unique_entities = [dict(t) for t in {tuple(d.items()) for d in entities}]
    query = """
    UNWIND $entities AS entity
    MERGE (n:Entity {name: entity.name, type: entity.type})
    """
    tx.run(query, entities=unique_entities)

def create_relationships(tx, relationships):
    # Loại bỏ duplicates trong danh sách relationships
    unique_relationships = [dict(t) for t in {tuple(d.items()) for d in relationships}]
    query = """
    UNWIND $rels AS rel
    MATCH (a:Entity {name: rel.source})
    MATCH (b:Entity {name: rel.target})
    MERGE (a)-[r:RELATION {type: rel.relation}]->(b)
    """
    tx.run(query, rels=unique_relationships)


# Hàm tạo node và relationship
def create_nodes_and_relationships(driver, data):
    with driver.session() as session:
        # Tạo các node với UNWIND
        entities_query = """
        UNWIND $entities AS entity
        MERGE (n:Entity {name: entity.name, type: entity.type})
        """
        session.run(entities_query, parameters={"entities": data['entities']})

        # Tạo các relationship với UNWIND sử dụng apoc để động tên mối quan hệ
        relationships_query = """
        UNWIND $rels AS rel
        MATCH (a:Entity {name: rel.source})
        MATCH (b:Entity {name: rel.target})
        CALL apoc.create.relationship(a, rel.relation, {}, b) YIELD rel as r
        SET r.created_at = timestamp()
        """
        session.run(relationships_query, parameters={"rels": data['relationships']})

model_name = os.getenv("model")
data_path = os.getenv("data_path")

driver = general.connect_to_graph_db()
model = general.load_model(model_name, prompt.prompt_extract_entities_relationship())
chunks = general.read_chunks(data_path)

documents = []
# chưa tiền xử lý dữ liệu sử dụng hàm text_vietnamese_processed bên lớp general

for i in range(0, 27):
    start = i*10+i
    end = start + 10
    time.sleep(120)
    for chunk in range(start, end+1):
        try:
            content = chunks[chunk].page_content
            response = model.generate_content(content)
            extract = general.extract_relations_from_model_output(response.text)

            print(extract)
            if len(extract) != 0:
                create_nodes_and_relationships(driver, extract)
            print(chunk, ' thành công')
        except Exception as e:
            print(chunk, ' thất bại ', e)

driver.close()

# lấy tất cả quan hệ
# MATCH (n)-[r]->(m)
# RETURN n, r, m;
# xóa tất cả quan hệ
# MATCH (n)
# DETACH DELETE n;
