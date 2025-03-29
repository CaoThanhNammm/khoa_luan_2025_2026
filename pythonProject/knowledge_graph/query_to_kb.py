import json
from KnowledgeGraphDatabase import Neo4j
from knowledge_graph.create_entities_relationship_kb import pre_processing

def get_path(type, part):
    result = neo.get_path(type, part)
    i = 1

    for record in result:
        print(i)

        path = []
        relationships = record['relationship']
        for rel in relationships:
            # Lấy thông tin từ Relationship
            start_node = rel.start_node
            end_node = rel.end_node
            rel_type = rel.type

            # Lấy thông tin từ start_node
            start_node_labels = list(start_node.labels)[0]
            start_node_name = start_node.get("name")

            # Lấy thông tin từ end_node
            end_node_labels = list(end_node.labels)[0]
            end_node_name = end_node.get("name")

            path.append({
                "source": start_node_name,
                "type_source": start_node_labels,
                "target": end_node_name,
                "type_target": end_node_labels,
                "relation": rel_type,

            })
        i += 1
        print(path)


def get_owned_entities(type, part, relation):
    result = neo.get_owned_entities(type, part, relation)
    i = 1
    for record in result:
        print(i)
        relation = record['relationship']
        # Lấy thông tin từ relation
        start_node = relation.start_node
        end_node = relation.end_node
        rel_type = relation.type

        # Lấy thông tin từ start_node
        start_node_labels = list(start_node.labels)[0]
        start_node_name = start_node.get("name")

        # Lấy thông tin từ end_node
        end_node_labels = list(end_node.labels)[0]
        end_node_name = end_node.get("name")

        connect = {
            "source": start_node_name,
            "type_source": start_node_labels,
            "target": end_node_name,
            "type_target": end_node_labels,
            "relation": rel_type,

        }

        i += 1
        print(connect)

def jaccard_similarity_for_node(str1, str2):
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def jaccard_similarity_for_relation(str1, str2):
    set1 = set(str1.lower().split("_"))
    set2 = set(str2.lower().split("_"))
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def change_node_to_relation(text):
    return text.replace(" ", "_")

if __name__ == "__main__":
    # Thay đổi thông tin kết nối theo cấu hình Neo4j của bạn
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "123456789"

    # Tạo instance của class Neo4j
    neo = Neo4j(uri, user, password)

    # lấy path từ một part
    # ví dụ: lấy path của "các khoa - ngành đào tạo"
    # lấy path của "giá trị cốt lõi"
    type = "part"
    part = "các đơn vị trong trường"
    # get_path(type, part)


    # QUY TRÌNH XỬ LÝ CÂU HỎI
    # 1. dùng llm trích xuất entites và relation
    # 2. dùng llm tạo cypher query
    # 3. dùng cypher truy vấn vào neo4j
    # 4. trả về kết quả

    all_nodes = neo.get_all_nodes()
    all_nodes_and_relationships = neo.get_all_nodes_and_relationships()

    """match (o:organization{name:"trường đại học nông lâm"})-[r:của]->(e:location) return o,r,e"""
    entities_relationship = [
        {
            "entities": [
                {
                    "name": "trường đại_học nông_lâm thành_phố hồ_chí_minh",
                    "type": "organization"
                },
                {
                    "name": "lịch_sử",
                    "type": "concept"
                }
            ],
            "relationships": [
                {
                    "source": "lịch_sử",
                    "relation": "của",
                    "type_source": "concept"
                }
            ]
        }]

    relationship = entities_relationship[0]['relationships']

    for relation in relationship:
        source_text = relation["source"]
        relation_text = relation["relation"]
        rel_search_text = change_node_to_relation(relation_text)

        for connect in all_nodes_and_relationships:
            source = connect['source']
            relation = connect['relation']

            source_score = jaccard_similarity_for_node(source_text, source)
            relation_score = jaccard_similarity_for_relation(rel_search_text, relation)

            if source_score > 0.4 or relation_score > 0.4:
                print({
                    source: source_score,
                    relation: relation_score
                })

    # Đóng kết nối
    neo.close()



# lấy tất cả quan hệ
# MATCH (n)-[r]->(m)
# RETURN n, r, m;
# xóa tất cả quan hệ
# MATCH (n)
# DETACH DELETE n;


