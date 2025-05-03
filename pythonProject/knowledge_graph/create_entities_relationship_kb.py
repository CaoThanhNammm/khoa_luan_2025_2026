import os
from PreProcessing.PreProcessing import PreProcessing
from knowledge_graph.KnowledgeGraphDatabase import Neo4j

pre_processing = PreProcessing()
from dotenv import load_dotenv
load_dotenv()
import json

def add_entities_relationship(json_string, type_part, part):
    json_string = list(map(lambda s: s.lower(), json_string))
    print(json_string)
    json = []
    # đổi từ string sang json
    for s in json_string:
        print(s)
        json.append(pre_processing.string_to_json(s))

    entities = []
    relationships = []

    for j in json:
        entities.extend(j['entities'])
        relationships.extend(j['relationships'])

    # change_to_json = json.loads(json_string)
    #
    # entities = change_to_json['entities']
    # relationships = change_to_json['relationships']

    print(entities)
    neo.add_entities(entities)

    neo.add_relationships(relationships, type_part, part)
    print("thêm hoàn tất")


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


if __name__ == "__main__":
    # Thay đổi thông tin kết nối theo cấu hình Neo4j của bạn
    uri = os.getenv("URI_NEO")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    # Tạo instance của class Neo4j
    neo = Neo4j(uri, user, password)

    # 1. Thêm các entities và relationships cấp cao
    neo.add_entities_relation_highest()

    # 2. thêm entities và relationship vào neo4j
    type_part = "article"

    json_string = []

    part = []
    json_string = [
        """{
  "entities": [
    {
      "name": "Kênh đăng ký",
      "type": "registration_channel"
    },
    {
      "name": "Đăng ký trực tuyến",
      "type": "registration_method"
    },
    {
      "name": "https://nlsonline.hcmuaf.edu.vn/gxn/dangnhap.php",
      "type": "website"
    }
  ],
  "relationships": [
    {
      "source": "Đăng ký trực tuyến",
      "target": "https://nlsonline.hcmuaf.edu.vn/gxn/dangnhap.php",
      "relation": "tại_địa_chỉ",
      "type_source": "registration_method",
      "type_target": "website"
    }
  ]
}
"""
    ]
    part = "kênh đăng ký"

    add_entities_relationship(json_string, type_part, part)
    # for i in range(len(json_string)):
    #     add_entities_relationship(json_string[i], type_part, part[i])

    # Đóng kết nối
    neo.close()


# lấy tất cả quan hệ
# MATCH (n)-[r]->(m)
# RETURN n, r, m;
# xóa tất cả quan hệ
# MATCH (n)
# DETACH DELETE n;

# bac 2
# MATCH (first:part {name: 'phần 3: hỗ trợ và dịch vụ'})-[:bao_gồm]->(second:section {name: 'trung tâm dịch vụ sinh viên'})-[r*1..3]->(e)
# RETURN r as relation, e as target

# bac 3
# MATCH (first:part {name: 'phần 3: hỗ trợ và dịch vụ'})-[:bao_gồm]->(second:section {name: 'vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})-[:bao_gồm]->(four:article {name: 'thông tin về vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})-[r*1..3]->(e)
# RETURN r as relation, e as target

# bac 4
# MATCH (first:part {name: 'phần 3: hỗ trợ và dịch vụ'})-[:bao_gồm]->(second:section {name: 'quy định phân cấp giải quyết thắc mắc của sinh viên'})-[:bao_gồm]->(third:part {name: 'ngoài ra ưu tiên xét chọn những sinh viên đạt ít nhất 01 trong các các tiêu chuẩn sau'})-[:bao_gồm]->(four:article {name: 'ưu tiên 6'})-[r*1..3]->(e)
# RETURN r as relation, e as target


# xoa tat ca cac node tu node co san
# MATCH (a:article {name: 'phương thức cho vay tiền sinh viên'})-[r]->(b)
# DETACH DELETE b



