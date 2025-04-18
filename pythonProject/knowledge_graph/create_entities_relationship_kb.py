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
      "name": "giấy tờ",
      "type": "document"
    },
    {
      "name": "Vay vốn ngân hàng chính sách xã hội",
      "type": "document_type"
    },
    {
      "name": "ngân hàng chính sách xã hội",
      "type": "organization"
    },
    {
      "name": "Tạm hoãn nghĩa vụ quân sự",
      "type": "document_type"
    },
    {
      "name": "Đi xe buýt",
      "type": "document_type"
    },
    {
      "name": "Bổ sung hồ sơ nhận trợ cấp",
      "type": "document_type"
    },
    {
      "name": "Bổ sung hồ sơ làm lại thẻ sinh viên",
      "type": "document_type"
    },
    {
      "name": "thẻ sinh viên",
      "type": "student_card"
    },
    {
      "name": "Bổ sung hồ sơ thuế cho người thân",
      "type": "document_type"
    },
    {
      "name": "thuế",
      "type": "tax_document"
    },
    {
      "name": "người thân",
      "type": "relative"
    },
    {
      "name": "Bổ sung hồ sơ ký túc xá Đại học Quốc gia TP.HCM",
      "type": "document_type"
    },
    {
      "name": "ký túc xá",
      "type": "dormitory_document"
    },
    {
      "name": "Đại học Quốc gia TP.HCM",
      "type": "university"
    },
    {
      "name": "Bổ sung hồ sơ thi học kỳ, thi acces",
      "type": "document_type"
    },
    {
      "name": "thi học kỳ",
      "type": "exam_document"
    },
    {
      "name": "thi acces",
      "type": "exam_document"
    },
    {
      "name": "Bổ sung hồ sơ lý lịch cá nhân",
      "type": "document_type"
    },
    {
      "name": "lý lịch cá nhân",
      "type": "personal_profile"
    },
    {
      "name": "Bổ sung hồ sơ nhận học bổng",
      "type": "document_type"
    },
    {
      "name": "học bổng",
      "type": "scholarship_document"
    },
    {
      "name": "Bổ sung hồ sơ giảm trừ gia cảnh",
      "type": "document_type"
    },
    {
      "name": "giảm trừ gia cảnh",
      "type": "family_deduction_document"
    },
    {
      "name": "Bổ sung hồ sơ đi làm, đi thực tập",
      "type": "document_type"
    },
    {
      "name": "đi làm",
      "type": "work_document"
    },
    {
      "name": "đi thực tập",
      "type": "internship_document"
    }
  ],
  "relationships": [
    {
      "source": "Vay vốn ngân hàng chính sách xã hội",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "ngân hàng chính sách xã hội",
      "target": "Vay vốn ngân hàng chính sách xã hội",
      "relation": "của",
      "type_source": "organization",
      "type_target": "document_type"
    },
    {
      "source": "Tạm hoãn nghĩa vụ quân sự",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "Đi xe buýt",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "Bổ sung hồ sơ nhận trợ cấp",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "Bổ sung hồ sơ làm lại thẻ sinh viên",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "thẻ sinh viên",
      "target": "Bổ sung hồ sơ làm lại thẻ sinh viên",
      "relation": "của",
      "type_source": "student_card",
      "type_target": "document_type"
    },
    {
      "source": "Bổ sung hồ sơ thuế cho người thân",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "thuế",
      "target": "Bổ sung hồ sơ thuế cho người thân",
      "relation": "của",
      "type_source": "tax_document",
      "type_target": "document_type"
    },
    {
      "source": "người thân",
      "target": "Bổ sung hồ sơ thuế cho người thân",
      "relation": "cho",
      "type_source": "relative",
      "type_target": "document_type"
    },
    {
      "source": "Bổ sung hồ sơ ký túc xá Đại học Quốc gia TP.HCM",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "ký túc xá",
      "target": "Bổ sung hồ sơ ký túc xá Đại học Quốc gia TP.HCM",
      "relation": "của",
      "type_source": "dormitory_document",
      "type_target": "document_type"
    },
    {
      "source": "Đại học Quốc gia TP.HCM",
      "target": "Bổ sung hồ sơ ký túc xá Đại học Quốc gia TP.HCM",
      "relation": "của",
      "type_source": "university",
      "type_target": "document_type"
    },
    {
      "source": "Bổ sung hồ sơ thi học kỳ, thi acces",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "thi học kỳ",
      "target": "Bổ sung hồ sơ thi học kỳ, thi acces",
      "relation": "của",
      "type_source": "exam_document",
      "type_target": "document_type"
    },
    {
      "source": "thi acces",
      "target": "Bổ sung hồ sơ thi học kỳ, thi acces",
      "relation": "của",
      "type_source": "exam_document",
      "type_target": "document_type"
    },
    {
      "source": "Bổ sung hồ sơ lý lịch cá nhân",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "lý lịch cá nhân",
      "target": "Bổ sung hồ sơ lý lịch cá nhân",
      "relation": "của",
      "type_source": "personal_profile",
      "type_target": "document_type"
    },
    {
      "source": "Bổ sung hồ sơ nhận học bổng",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "học bổng",
      "target": "Bổ sung hồ sơ nhận học bổng",
      "relation": "của",
      "type_source": "scholarship_document",
      "type_target": "document_type"
    },
    {
      "source": "Bổ sung hồ sơ giảm trừ gia cảnh",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "giảm trừ gia cảnh",
      "target": "Bổ sung hồ sơ giảm trừ gia cảnh",
      "relation": "của",
      "type_source": "family_deduction_document",
      "type_target": "document_type"
    },
    {
      "source": "Bổ sung hồ sơ đi làm, đi thực tập",
      "target": "giấy tờ",
      "relation": "là_loại",
      "type_source": "document_type",
      "type_target": "document"
    },
    {
      "source": "đi làm",
      "target": "Bổ sung hồ sơ đi làm, đi thực tập",
      "relation": "của",
      "type_source": "work_document",
      "type_target": "document_type"
    },
    {
      "source": "đi thực tập",
      "target": "Bổ sung hồ sơ đi làm, đi thực tập",
      "relation": "của",
      "type_source": "internship_document",
      "type_target": "document_type"
    }
  ]
}
"""
    ]
    part = "các loại giấy tờ được xác nhận"

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



