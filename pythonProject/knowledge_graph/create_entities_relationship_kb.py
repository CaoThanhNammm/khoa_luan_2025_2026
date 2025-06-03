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
    print(len(relationships))
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
      "name": "học sinh/sinh viên",
      "type": "person"
    },
    {
      "name": "giờ học",
      "type": "time"
    },
    {
      "name": "giờ thực tập",
      "type": "time"
    },
    {
      "name": "điểm rèn luyện",
      "type": "score_type"
    },
    {
      "name": "thầy",
      "type": "person"
    },
    {
      "name": "cô giáo",
      "type": "person"
    },
    {
      "name": "CBVC nhà trường",
      "type": "person"
    },
    {
      "name": "khiển trách",
      "type": "punishment"
    },
    {
      "name": "buộc thôi học",
      "type": "punishment"
    },
    {
      "name": "thi",
      "type": "activity"
    },
    {
      "name": "kiểm tra",
      "type": "activity"
    },
    {
      "name": "tiểu luận",
      "type": "academic_work"
    },
    {
      "name": "đồ án",
      "type": "academic_work"
    },
    {
      "name": "khóa luận tốt nghiệp",
      "type": "academic_work"
    },
    {
      "name": "đình chỉ có thời hạn",
      "type": "punishment"
    },
    {
      "name": "cơ quan chức năng",
      "type": "organization"
    },
    {
      "name": "phòng thi",
      "type": "location"
    },
    {
      "name": "bậc Trung bình",
      "type": "rating"
    },
    {
      "name": "học phí",
      "type": "fee"
    },
    {
      "name": "bảo hiểm y tế",
      "type": "fee"
    },
    {
      "name": "KTX",
      "type": "location"
    },
    {
      "name": "tài sản",
      "type": "property"
    },
    {
      "name": "rượu",
      "type": "substance"
    },
    {
      "name": "bia",
      "type": "substance"
    },
    {
      "name": "thuốc lá",
      "type": "substance"
    },
    {
      "name": "phòng họp",
      "type": "location"
    },
    {
      "name": "phòng thí nghiệm",
      "type": "location"
    },
    {
      "name": "cảnh cáo",
      "type": "punishment"
    },
    {
      "name": "đánh bạc",
      "type": "violation"
    },
    {
      "name": "sản phẩm văn hóa đồi trụy",
      "type": "prohibited_item"
    },
    {
      "name": "hoạt động mê tín dị đoan",
      "type": "prohibited_activity"
    },
    {
      "name": "hoạt động tôn giáo trái phép",
      "type": "prohibited_activity"
    },
    {
      "name": "ma túy",
      "type": "prohibited_substance"
    },
    {
      "name": "mại dâm",
      "type": "prohibited_activity"
    },
    {
      "name": "vũ khí",
      "type": "prohibited_item"
    },
    {
      "name": "chất nổ",
      "type": "prohibited_item"
    },
    {
      "name": "hàng cấm",
      "type": "prohibited_item"
    },
    {
      "name": "phần tử xấu",
      "type": "person"
    },
    {
      "name": "truyền đơn",
      "type": "document"
    },
    {
      "name": "áp phích",
      "type": "document"
    },
    {
      "name": "biểu tình",
      "type": "prohibited_activity"
    },
    {
      "name": "tụ tập đông người",
      "type": "prohibited_activity"
    },
    {
      "name": "khiếu kiện",
      "type": "activity"
    },
    {
      "name": "mạng Internet",
      "type": "platform"
    },
    {
      "name": "Đảng",
      "type": "organization"
    },
    {
      "name": "Nhà nước",
      "type": "organization"
    },
    {
      "name": "an ninh quốc gia",
      "type": "concept"
    },
    {
      "name": "an toàn giao thông",
      "type": "regulation"
    },
    {
      "name": "hồ sơ",
      "type": "document"
    },
    {
      "name": "văn bằng",
      "type": "document"
    },
    {
      "name": "chứng chỉ",
      "type": "document"
    },
    {
      "name": "nhà trường",
      "type": "organization"
    }
  ],
  "relationships": [
    {
      "source": "học sinh/sinh viên",
      "target": "giờ học",
      "type_source": "person",
      "type_target": "time",
      "relation": "đến_muộn"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "giờ thực tập",
      "type_source": "person",
      "type_target": "time",
      "relation": "đến_muộn"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "điểm rèn luyện",
      "type_source": "person",
      "type_target": "score_type",
      "relation": "bị_trừ"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "thầy",
      "type_source": "person",
      "type_target": "person",
      "relation": "vô_lễ_với"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "cô giáo",
      "type_source": "person",
      "type_target": "person",
      "relation": "vô_lễ_với"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "CBVC nhà trường",
      "type_source": "person",
      "type_target": "person",
      "relation": "vô_lễ_với"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "khiển trách",
      "type_source": "person",
      "type_target": "punishment",
      "relation": "bị_xử_lý"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "buộc thôi học",
      "type_source": "person",
      "type_target": "punishment",
      "relation": "bị_xử_lý"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "thi",
      "type_source": "person",
      "type_target": "activity",
      "relation": "thực_hiện"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "kiểm tra",
      "type_source": "person",
      "type_target": "activity",
      "relation": "thực_hiện"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "tiểu luận",
      "type_source": "person",
      "type_target": "academic_work",
      "relation": "làm"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "đồ án",
      "type_source": "person",
      "type_target": "academic_work",
      "relation": "làm"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "khóa luận tốt nghiệp",
      "type_source": "person",
      "type_target": "academic_work",
      "relation": "làm"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "đình chỉ có thời hạn",
      "type_source": "person",
      "type_target": "punishment",
      "relation": "bị_xử_lý"
    },
    {
      "source": "cơ quan chức năng",
      "target": "học sinh/sinh viên",
      "type_source": "organization",
      "type_target": "person",
      "relation": "xử_lý"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "phòng thi",
      "type_source": "person",
      "type_target": "location",
      "relation": "mang_tài_liệu_vào"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "bậc Trung bình",
      "type_source": "person",
      "type_target": "rating",
      "relation": "bị_hạ_điểm_xuống"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "học phí",
      "type_source": "person",
      "type_target": "fee",
      "relation": "chậm_nộp"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "bảo hiểm y tế",
      "type_source": "person",
      "type_target": "fee",
      "relation": "chậm_nộp"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "KTX",
      "type_source": "person",
      "type_target": "location",
      "relation": "ở_trong"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "tài sản",
      "type_source": "person",
      "type_target": "property",
      "relation": "làm_hư_hỏng"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "cảnh cáo",
      "type_source": "person",
      "type_target": "punishment",
      "relation": "bị_xử_lý"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "rượu",
      "type_source": "person",
      "type_target": "substance",
      "relation": "sử_dụng"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "bia",
      "type_source": "person",
      "type_target": "substance",
      "relation": "sử_dụng"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "thuốc lá",
      "type_source": "person",
      "type_target": "substance",
      "relation": "hút"
    },
    {
      "source": "thuốc lá",
      "target": "giờ học",
      "type_source": "substance",
      "type_target": "time",
      "relation": "bị_cấm_trong"
    },
    {
      "source": "thuốc lá",
      "target": "phòng họp",
      "type_source": "substance",
      "type_target": "location",
      "relation": "bị_cấm_trong"
    },
    {
      "source": "thuốc lá",
      "target": "phòng thí nghiệm",
      "type_source": "substance",
      "type_target": "location",
      "relation": "bị_cấm_trong"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "đánh bạc",
      "type_source": "person",
      "type_target": "violation",
      "relation": "thực_hiện"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "sản phẩm văn hóa đồi trụy",
      "type_source": "person",
      "type_target": "prohibited_item",
      "relation": "tàng_trữ"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "hoạt động mê tín dị đoan",
      "type_source": "person",
      "type_target": "prohibited_activity",
      "relation": "tham_gia"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "hoạt động tôn giáo trái phép",
      "type_source": "person",
      "type_target": "prohibited_activity",
      "relation": "tham_gia"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "ma túy",
      "type_source": "person",
      "type_target": "prohibited_substance",
      "relation": "buôn_bán"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "ma túy",
      "type_source": "person",
      "type_target": "prohibited_substance",
      "relation": "sử_dụng"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "mại dâm",
      "type_source": "person",
      "type_target": "prohibited_activity",
      "relation": "môi_giới"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "vũ khí",
      "type_source": "person",
      "type_target": "prohibited_item",
      "relation": "buôn_bán"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "chất nổ",
      "type_source": "person",
      "type_target": "prohibited_item",
      "relation": "buôn_bán"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "hàng cấm",
      "type_source": "person",
      "type_target": "prohibited_item",
      "relation": "buôn_bán"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "phần tử xấu",
      "type_source": "person",
      "type_target": "person",
      "relation": "đưa_vào"
    },
    {
      "source": "phần tử xấu",
      "target": "KTX",
      "type_source": "person",
      "type_target": "location",
      "relation": "được_đưa_vào"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "truyền đơn",
      "type_source": "person",
      "type_target": "document",
      "relation": "viết"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "áp phích",
      "type_source": "person",
      "type_target": "document",
      "relation": "viết"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "biểu tình",
      "type_source": "person",
      "type_target": "prohibited_activity",
      "relation": "tham_gia"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "tụ tập đông người",
      "type_source": "person",
      "type_target": "prohibited_activity",
      "relation": "tham_gia"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "khiếu kiện",
      "type_source": "person",
      "type_target": "activity",
      "relation": "thực_hiện"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "mạng Internet",
      "type_source": "person",
      "type_target": "platform",
      "relation": "sử_dụng"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "Đảng",
      "type_source": "person",
      "type_target": "organization",
      "relation": "chống_phá"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "Nhà nước",
      "type_source": "person",
      "type_target": "organization",
      "relation": "chống_phá" 
    },
    {
      "source": "học sinh/sinh viên",
      "target": "an ninh quốc gia",
      "type_source": "person",
      "type_target": "concept",
      "relation": "xâm_phạm"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "an toàn giao thông",
      "type_source": "person",
      "type_target": "regulation",
      "relation": "vi_phạm"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "hồ sơ",
      "type_source": "person",
      "type_target": "document",
      "relation": "sử_dụng"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "văn bằng",
      "type_source": "person",
      "type_target": "document",
      "relation": "sử_dụng"
    },
    {
      "source": "học sinh/sinh viên",
      "target": "chứng chỉ",
      "type_source": "person",
      "type_target": "document",
      "relation": "sử_dụng"
    },
    {
      "source": "nhà trường",
      "target": "học sinh/sinh viên",
      "type_source": "organization",
      "type_target": "person",
      "relation": "xem_xét"
    }
  ]
}"""
    ]

    part = "một số nội dung vi phạm và khung xử lý kỷ luật sinh viên"

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



