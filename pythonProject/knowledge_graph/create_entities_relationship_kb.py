import general
from KnowledgeGraphDatabase import Neo4j

def add_entities_relationship(json_string, part):
    json_string = list(map(lambda s: s.lower(), json_string))
    json = []
    # đổi từ string sang json
    for s in json_string:
        json.append(general.string_to_json(s))

    entities = []
    relationships = []

    for j in json:
        entities.extend(j['entities'])
        relationships.extend(j['relationships'])
    print(entities)
    neo.add_entities(entities)

    neo.add_relationships(relationships, part)
    print("thêm hoàn tất")

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

def jaccard_similarity(str1, str2):
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

if __name__ == "__main__":
    # Thay đổi thông tin kết nối theo cấu hình Neo4j của bạn
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "123456789"

    # Tạo instance của class Neo4j
    neo = Neo4j(uri, user, password)

    # 1. Thêm các entities và relationships cấp cao
    # neo.add_entities_relation_highest()

    # 2. thêm entities và relationship vào neo4j
    json_string = [
    """{
  "entities": [
    {"name": "Trường Đại học Nông Lâm TP.HCM", "type": "organization"},
    {"name": "giảng dạy trực tuyến", "type": "teaching_method"},
    {"name": "giảng dạy online – offline", "type": "teaching_method"},
    {"name": "30%", "type": "percentage"},
    {"name": "chương trình đào tạo", "type": "event"},
    {"name": "dịch bệnh", "type": "event"},
    {"name": "thiên tai", "type": "event"},
    {"name": "Hiệu trưởng", "type": "person"},
    {"name": "Hệ thống Đào tạo trực tuyến", "type": "system"},
    {"name": "Trường Đại học Nông Lâm Thành phố Hồ Chí Minh", "type": "organization"},
    {"name": "e-Learning – NLU", "type": "system"},
    {"name": "cổng đào tạo trực tuyến", "type": "platform"},
    {"name": "hệ thống quản lý học tập", "type": "platform"},
    {"name": "học liệu điện tử", "type": "document"},
    {"name": "diễn đàn trao đổi", "type": "platform"},
    {"name": "thảo luận trực tuyến", "type": "event"},
    {"name": "hệ thống kiểm tra, đánh giá sinh viên", "type": "system"},
    {"name": "giảng viên", "type": "person"},
    {"name": "Edmodo", "type": "platform"},
    {"name": "Zoom", "type": "platform"},
    {"name": "Google meet", "type": "platform"},
    {"name": "Microsoft team", "type": "platform"},
    {"name": "Skype", "type": "platform"},
    {"name": "máy tính", "type": "device"},
    {"name": "thiết bị di động thông minh", "type": "device"},
    {"name": "học phần", "type": "event"},
    {"name": "sinh viên", "type": "person"},
    {"name": "chuẩn đầu ra", "type": "criteria"},
    {"name": "thang điểm 10", "type": "data"},
    {"name": "đề cương chi tiết", "type": "document"},
    {"name": "50%", "type": "percentage"},
    {"name": "Khoa", "type": "organization"},
    {"name": "Bộ môn", "type": "organization"},
    {"name": "thi cuối kỳ", "type": "event"},
    {"name": "Trưởng Khoa", "type": "person"},
    {"name": "ngân hàng câu hỏi", "type": "document"},
    {"name": "đề thi", "type": "document"},
    {"name": "đáp án", "type": "document"},
    {"name": "hướng dẫn chấm thi", "type": "document"},
    {"name": "thực hành", "type": "teaching_method"},
    {"name": "thực tập", "type": "teaching_method"},
    {"name": "thi tay nghề", "type": "event"},
    {"name": "nghiệp vụ", "type": "event"},
    {"name": "thao tác kỹ thuật", "type": "event"},
    {"name": "thiên tai", "type": "event"},
    {"name": "dịch bệnh", "type": "event"},
    {"name": "đồ án", "type": "assignment"},
    {"name": "tiểu luận", "type": "assignment"},
    {"name": "khóa luận", "type": "assignment"},
    {"name": "hội đồng chuyên môn", "type": "organization"},
    {"name": "3 thành viên", "type": "data"},
    {"name": "tài khoản", "type": "account"},
    {"name": "lớp học", "type": "event"},
    {"name": "diễn đàn thảo luận", "type": "platform"},
    {"name": "tài liệu học tập", "type": "document"},
    {"name": "hồ sơ cá nhân", "type": "document"},
    {"name": "hình đại diện", "type": "image"},
    {"name": "chữ ký", "type": "document"},
    {"name": "đường link lớp học", "type": "link"},
    {"name": "nhiệm vụ", "type": "task"},
    {"name": "giảng viên", "type": "person"},
    {"name": "05 - 10 phút", "type": "time"},
    {"name": "email", "type": "email_address"},
    {"name": "micro", "type": "device"},
    {"name": "camera", "type": "device"},
    {"name": "Raise hand", "type": "feature"},
    {"name": "Lower hand", "type": "feature"},
    {"name": "màn hình cá nhân", "type": "device"}
  ],
  "relationships": [
    {"source": "Trường Đại học Nông Lâm TP.HCM", "target": "giảng dạy trực tuyến", "relation": "TĂNG_CƯỜNG", "type_source": "organization", "type_target": "teaching_method"},
    {"source": "Trường Đại học Nông Lâm TP.HCM", "target": "giảng dạy online – offline", "relation": "ÁP_DỤNG", "type_source": "organization", "type_target": "teaching_method"},
    {"source": "giảng dạy online", "target": "30%", "relation": "KHÔNG_VƯỢT_QUÁ", "type_source": "teaching_method", "type_target": "percentage"},
    {"source": "giảng dạy online", "target": "số giờ tín chỉ", "relation": "CỦA", "type_source": "teaching_method", "type_target": "data"},
    {"source": "giảng dạy online", "target": "chương trình đào tạo", "relation": "CỦA", "type_source": "teaching_method", "type_target": "event"},
    {"source": "dịch bệnh", "target": "Hiệu trưởng", "relation": "CHỈ_ĐẠO", "type_source": "event", "type_target": "person"},
    {"source": "thiên tai", "target": "Hiệu trưởng", "relation": "CHỈ_ĐẠO", "type_source": "event", "type_target": "person"},
    {"source": "trường hợp đặc biệt", "target": "Hiệu trưởng", "relation": "CHỈ_ĐẠO", "type_source": "concept", "type_target": "person"},
    {"source": "Hiệu trưởng", "target": "văn bản", "relation": "CÓ", "type_source": "person", "type_target": "document"},
    {"source": "Trường Đại học Nông Lâm Thành phố Hồ Chí Minh", "target": "Hệ thống Đào tạo trực tuyến", "relation": "TẠI", "type_source": "organization", "type_target": "system"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "e-Learning – NLU", "relation": "LÀ", "type_source": "system", "type_target": "system"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "trang thiết bị", "relation": "BAO_GỒM", "type_source": "system", "type_target": "device"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "cơ sở hạ tầng kỹ thuật", "relation": "BAO_GỒM", "type_source": "system", "type_target": "infrastructure"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "cơ sở dữ liệu", "relation": "BAO_GỒM", "type_source": "system", "type_target": "data"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "nguồn nhân lực", "relation": "BAO_GỒM", "type_source": "system", "type_target": "resource"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "tài nguyên hỗ trợ", "relation": "BAO_GỒM", "type_source": "system", "type_target": "resource"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "giảng dạy", "relation": "PHỤC_VỤ", "type_source": "system", "type_target": "activity"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "học tập", "relation": "PHỤC_VỤ", "type_source": "system", "type_target": "activity"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "cổng đào tạo trực tuyến", "relation": "BAO_GỒM", "type_source": "system", "type_target": "platform"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "hệ thống quản lý học tập", "relation": "BAO_GỒM", "type_source": "system", "type_target": "platform"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "học liệu điện tử", "relation": "BAO_GỒM", "type_source": "system", "type_target": "document"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "diễn đàn trao đổi", "relation": "BAO_GỒM", "type_source": "system", "type_target": "platform"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "thảo luận trực tuyến", "relation": "BAO_GỒM", "type_source": "system", "type_target": "event"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "hệ thống kiểm tra, đánh giá sinh viên", "relation": "BAO_GỒM", "type_source": "system", "type_target": "system"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "giảng viên", "relation": "BAO_GỒM", "type_source": "system", "type_target": "person"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "quản trị hệ thống", "relation": "BAO_GỒM", "type_source": "system", "type_target": "activity"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "Edmodo", "relation": "PHÁT_TRIỂN_TRÊN", "type_source": "system", "type_target": "platform"},
    {"source": "Hệ thống Đào tạo trực tuyến", "target": "quy định pháp luật", "relation": "ĐẢM_BẢO", "type_source": "system", "type_target": "regulation"},
    {"source": "giảng dạy", "target": "Zoom", "relation": "TRÊN", "type_source": "activity", "type_target": "platform"},
    {"source": "giảng dạy", "target": "Google meet", "relation": "TRÊN", "type_source": "activity", "type_target": "platform"},
    {"source": "giảng dạy", "target": "Microsoft team", "relation": "TRÊN", "type_source": "activity", "type_target": "platform"},
    {"source": "giảng dạy", "target": "Skype", "relation": "TRÊN", "type_source": "activity", "type_target": "platform"},
    {"source": "giảng viên", "target": "công cụ", "relation": "CHỌN", "type_source": "person", "type_target": "tool"},
    {"source": "giảng viên", "target": "lớp học", "relation": "ĐĂNG_KÝ", "type_source": "person", "type_target": "event"},
    {"source": "giảng viên", "target": "sinh viên", "relation": "THÔNG_BÁO", "type_source": "person", "type_target": "person"},
    {"source": "kiểm tra", "target": "đánh giá", "relation": "KẾT_HỢP", "type_source": "activity", "type_target": "activity"},
    {"source": "đánh giá trực tuyến", "target": "nghiêm túc", "relation": "PHẢI", "type_source": "activity", "type_target": "concept"},
    {"source": "đánh giá trực tuyến", "target": "đầy đủ", "relation": "PHẢI", "type_source": "activity", "type_target": "concept"},
    {"source": "đánh giá trực tuyến", "target": "mức độ chuyên cần", "relation": "ĐÁNH_GIÁ", "type_source": "activity", "type_target": "data"},
    {"source": "đánh giá trực tuyến", "target": "năng lực", "relation": "ĐÁNH_GIÁ", "type_source": "activity", "type_target": "concept"},
    {"source": "đánh giá trực tuyến", "target": "chuẩn đầu ra", "relation": "ĐÁNH_GIÁ", "type_source": "activity", "type_target": "criteria"},
    {"source": "học phần", "target": "điểm đánh giá", "relation": "TÍNH_LÀ_THÀNH_PHẦN", "type_source": "event", "type_target": "data"},
    {"source": "điểm thành phần", "target": "thang điểm 10", "relation": "THEO", "type_source": "data", "type_target": "data"},
    {"source": "điểm thành phần", "target": "đề cương chi tiết", "relation": "ĐƯỢC_QUY_ĐỊNH_TRONG", "type_source": "data", "type_target": "document"},
    {"source": "điểm đánh giá", "target": "50%", "relation": "KHÔNG_QUÁ", "type_source": "data", "type_target": "percentage"},
    {"source": "Khoa", "target": "thi cuối kỳ", "relation": "TỔ_CHỨC", "type_source": "organization", "type_target": "event"},
    {"source": "Bộ môn", "target": "thi cuối kỳ", "relation": "TỔ_CHỨC", "type_source": "organization", "type_target": "event"},
    {"source": "Trưởng Khoa", "target": "thi cuối kỳ", "relation": "ĐỀ_XUẤT", "type_source": "person", "type_target": "event"},
    {"source": "Hiệu trưởng", "target": "thi cuối kỳ", "relation": "QUYẾT_ĐỊNH", "type_source": "person", "type_target": "event"},
    {"source": "thi trực tuyến", "target": "trang thiết bị", "relation": "CẦN", "type_source": "event", "type_target": "device"},
    {"source": "thi trực tuyến", "target": "phần mềm", "relation": "CẦN", "type_source": "event", "type_target": "software"},
    {"source": "thi trực tuyến", "target": "ngân hàng câu hỏi", "relation": "CẦN", "type_source": "event", "type_target": "document"},
    {"source": "Hiệu trưởng", "target": "văn bản", "relation": "BAN_HÀNH", "type_source": "person", "type_target": "document"},
    {"source": "thi cuối kỳ", "target": "thực hành", "relation": "KHÔNG_TỔ_CHỨC", "type_source": "event", "type_target": "teaching_method"},
    {"source": "thi cuối kỳ", "target": "thực tập", "relation": "KHÔNG_TỔ_CHỨC", "type_source": "event", "type_target": "teaching_method"},
    {"source": "Trưởng Khoa", "target": "trường hợp đặc biệt", "relation": "ĐỀ_XUẤT", "type_source": "person", "type_target": "concept"},
    {"source": "Hiệu trưởng", "target": "trường hợp đặc biệt", "relation": "QUYẾT_ĐỊNH", "type_source": "person", "type_target": "concept"},
    {"source": "thiên tai", "target": "bảo vệ", "relation": "TỔ_CHỨC", "type_source": "event", "type_target": "event"},
    {"source": "dịch bệnh", "target": "bảo vệ", "relation": "TỔ_CHỨC", "type_source": "event", "type_target": "event"},
    {"source": "trường hợp bất khả kháng", "target": "bảo vệ", "relation": "TỔ_CHỨC", "type_source": "concept", "type_target": "event"},
    {"source": "Hiệu trưởng", "target": "bảo vệ", "relation": "QUYẾT_ĐỊNH", "type_source": "person", "type_target": "event"},
    {"source": "Trưởng khoa", "target": "bảo vệ", "relation": "ĐỀ_XUẤT", "type_source": "person", "type_target": "event"},
    {"source": "bảo vệ", "target": "hội đồng chuyên môn", "relation": "THÔNG_QUA", "type_source": "event", "type_target": "organization"},
    {"source": "bảo vệ", "target": "thành viên hội đồng", "relation": "ĐƯỢC_ĐỒNG_THUẬN", "type_source": "event", "type_target": "person"},
    {"source": "bảo vệ", "target": "sinh viên", "relation": "ĐƯỢC_ĐỒNG_THUẬN", "type_source": "event", "type_target": "person"},
    {"source": "bảo vệ", "target": "ghi hình", "relation": "ĐƯỢC", "type_source": "event", "type_target": "activity"},
    {"source": "bảo vệ", "target": "ghi âm", "relation": "ĐƯỢC", "type_source": "event", "type_target": "activity"},
    {"source": "sinh viên", "target": "tài khoản", "relation": "ĐƯỢC_CUNG_CẤP", "type_source": "person", "type_target": "account"},
    {"source": "sinh viên", "target": "hướng dẫn", "relation": "ĐƯỢC", "type_source": "person", "type_target": "document"},
    {"source": "sinh viên", "target": "hỗ trợ", "relation": "ĐƯỢC", "type_source": "person", "type_target": "activity"},
    {"source": "sinh viên", "target": "lớp học", "relation": "TRUY_CẬP", "type_source": "person", "type_target": "event"},
    {"source": "sinh viên", "target": "học tập", "relation": "THAM_GIA", "type_source": "person", "type_target": "activity"},
    {"source": "sinh viên", "target": "diễn đàn thảo luận", "relation": "THAM_GIA", "type_source": "person", "type_target": "platform"},
    {"source": "sinh viên", "target": "tài liệu học tập", "relation": "ĐƯỢC_CUNG_CẤP", "type_source": "person", "type_target": "document"},
    {"source": "sinh viên", "target": "thông tin", "relation": "BỔ_SUNG", "type_source": "person", "type_target": "data"},
    {"source": "sinh viên", "target": "hồ sơ cá nhân", "relation": "BỔ_SUNG_VÀO", "type_source": "person", "type_target": "document"},
    {"source": "sinh viên", "target": "hình đại diện", "relation": "SỞ_HỮU", "type_source": "person", "type_target": "image"},
    {"source": "sinh viên", "target": "chữ ký", "relation": "SỞ_HỮU", "type_source": "person", "type_target": "document"},
    {"source": "hình đại diện", "target": "đường dẫn", "relation": "KHÔNG_KÈM", "type_source": "image", "type_target": "link"},
    {"source": "sinh viên", "target": "đường link lớp học", "relation": "GIỮ_BÍ_MẬT", "type_source": "person", "type_target": "link"},
    {"source": "sinh viên", "target": "tài khoản", "relation": "BẢO_VỆ", "type_source": "person", "type_target": "account"},
    {"source": "sinh viên", "target": "thông tin", "relation": "CHỊU_TRÁCH_NHIỆM", "type_source": "person", "type_target": "data"},
    {"source": "sinh viên", "target": "tài khoản", "relation": "CHỊU_TRÁCH_NHIỆM", "type_source": "person", "type_target": "account"},
    {"source": "sinh viên", "target": "nhiệm vụ", "relation": "HOÀN_THÀNH", "type_source": "person", "type_target": "task"},
    {"source": "sinh viên", "target": "lớp", "relation": "ĐĂNG_NHẬP", "type_source": "person", "type_target": "event"},
    {"source": "sinh viên", "target": "05 - 10 phút", "relation": "TRƯỚC", "type_source": "person", "type_target": "time"},
    {"source": "sinh viên", "target": "email", "relation": "BẰNG", "type_source": "person", "type_target": "email_address"},
    {"source": "sinh viên", "target": "micro", "relation": "KIỂM_TRA", "type_source": "person", "type_target": "device"},
    {"source": "sinh viên", "target": "camera", "relation": "KIỂM_TRA", "type_source": "person", "type_target": "device"},
    {"source": "sinh viên", "target": "Raise hand", "relation": "NHẤN", "type_source": "person", "type_target": "feature"},
    {"source": "sinh viên", "target": "micro", "relation": "MỞ", "type_source": "person", "type_target": "device"},
    {"source": "sinh viên", "target": "micro", "relation": "TẮT", "type_source": "person", "type_target": "device"},
    {"source": "sinh viên", "target": "Lower hand", "relation": "BẤM", "type_source": "person", "type_target": "feature"},
    {"source": "sinh viên", "target": "buổi học", "relation": "THAM_GIA", "type_source": "person", "type_target": "event"},
    {"source": "sinh viên", "target": "trang phục", "relation": "MẶC", "type_source": "person", "type_target": "concept"},
    {"source": "sinh viên", "target": "thái độ", "relation": "CÓ", "type_source": "person", "type_target": "concept"},
    {"source": "sinh viên", "target": "không gian học tập", "relation": "ĐẢM_BẢO", "type_source": "person", "type_target": "concept"},
    {"source": "sinh viên", "target": "màn hình cá nhân", "relation": "CHIA_SẺ", "type_source": "person", "type_target": "device"},
    {"source": "giảng viên", "target": "màn hình cá nhân", "relation": "ĐỒNG_Ý", "type_source": "person", "type_target": "device"}
  ]
}"""
    ]
    # part = "quy định về việc đào tạo trực tuyến"
    # add_entities_relationship(json_string, part)

    # lấy path từ một part
    # ví dụ: lấy path của "các khoa - ngành đào tạo"
    # lấy path của "giá trị cốt lõi"
    type = "part"
    part = "các đơn vị trong trường"
    # get_path(type, part)

    query = "trường nông lâm có bao nhiêu phòng ban"
    # 1. dùng llm trích xuất entites và relation
    # 2. dùng llm tạo cypher query
    # 3. dùng cypher truy vấn vào neo4j
    # 4. trả về kết quả
    # get_owned_entities("organization", "trường đại học nông lâm tp.hồ chí minh", "sở_hữu")

    cypher_queries = [
        # Trường Đại học Nông Lâm TP.HCM
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target',

        # Phân hiệu Trường Đại học Nông Lâm TP.HCM tại Ninh Thuận
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target',

        # Phân hiệu Trường Đại học Nông Lâm TP.HCM tại Gia Lai
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:tọa_lạc_tại]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:thuộc]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target',
        'MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target'
    ]
    # print(len(cypher_queries))
    # cypher_string = ""
    # for i, query in enumerate(cypher_queries, 1):
    #     print(i, " ", query)
    #     try:
    #         cypher_string += neo.run_cypher_query(query) +"\n"
    #     except Exception as e:
    #         continue
    # print(cypher_string)

    all_nodes = neo.get_all_nodes()
    all_nodes_and_relationships = neo.get_all_nodes_and_relationships()
    # print(len(all_nodes))
    # print(all_nodes)

    search_source_text = "ngành đào tạo"
    search_rel_text = "chương_trình_đào_tạo_tại"
    search_target_text = "Phân hiệu Ninh thuan"

    for connect in all_nodes_and_relationships:
        source = connect['source']
        relation = connect['relation']
        target = connect['target']

        source_score = jaccard_similarity(search_source_text, source)
        relation_score = jaccard_similarity(search_rel_text, relation)
        target_score = jaccard_similarity(search_target_text, target)

        # if target_score > 0.4:
        #     print(f"{target}: {target_score}, {relation}: {relation_score}, {target}: {target_score}")

        if relation_score > 0.4:
            print(f"{source}: {source_score}, {relation}: {relation_score}, {target}: {target_score}")

    # Đóng kết nối
    neo.close()


# lấy tất cả quan hệ
# MATCH (n)-[r]->(m)
# RETURN n, r, m;
# xóa tất cả quan hệ
# MATCH (n)
# DETACH DELETE n;






