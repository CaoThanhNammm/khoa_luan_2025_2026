from neo4j import GraphDatabase

class Neo4j:
    def __init__(self, uri, user, password):
        """Khởi tạo kết nối tới Neo4j"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Đóng kết nối tới Neo4j"""
        self.driver.close()

    def execute_cypher(self, query):
        """Thực thi một truy vấn Cypher"""
        with self.driver.session() as session:
            session.run(query)

    def add_entities_relation_highest(self):
        """Thêm các entities và relationships cấp cao"""
        cypher_queries = [
            # Episode 1: nlu - định hướng trường đại học nghiên cứu
            """
            MERGE (a:Part {name: 'phần 1: nlu - định hướng trường đại học nghiên cứu'})
            MERGE (b:Section {name: 'quá trình hình thành và phát triển'})
            MERGE (c:Section {name: 'sứ mạng'})
            MERGE (d:Section {name: 'tầm nhìn'})
            MERGE (e:Section {name: 'giá trị cốt lõi'})
            MERGE (f:Section {name: 'mục tiêu chiến lược'})
            MERGE (g:Section {name: 'cơ sở vật chất'})
            MERGE (h:Section {name: 'các đơn vị trong trường'})
            MERGE (i:Section {name: 'các khoa - ngành đào tạo'})
            MERGE (j:Section {name: 'tuần sinh hoạt công dân - sinh viên'})
            MERGE (k:Section {name: 'hoạt động phong trào sinh viên'})
            MERGE (l:Section {name: 'câu lạc bộ (clb) - đội, nhóm'})
            MERGE (m:Section {name: 'cơ sở đào tạo'})
            MERGE (a)-[:BAO_GỒM]->(b)
            MERGE (a)-[:BAO_GỒM]->(c)
            MERGE (a)-[:BAO_GỒM]->(d)
            MERGE (a)-[:BAO_GỒM]->(e)
            MERGE (a)-[:BAO_GỒM]->(f)
            MERGE (a)-[:BAO_GỒM]->(g)
            MERGE (a)-[:BAO_GỒM]->(h)
            MERGE (a)-[:BAO_GỒM]->(i)
            MERGE (a)-[:BAO_GỒM]->(j)
            MERGE (a)-[:BAO_GỒM]->(k)
            MERGE (a)-[:BAO_GỒM]->(l)
            MERGE (a)-[:BAO_GỒM]->(m)
            """,
            # Episode 2: học tập và rèn luyện
            """
            MERGE (n:Part {name: 'phần 2: học tập và rèn luyện'})

            MERGE (o:Section {name: 'quy chế sinh viên'})
            MERGE (o2:Part {name: 'chương 2: quyền và nghĩa vụ của sinh viên'})
            MERGE (o2_4:Article {name: 'điều 4: quyền của sinh viên'})
            MERGE (o2_5:Article {name: 'điều 5: nghĩa vụ của sinh viên'})
            MERGE (o2_6:Article {name: 'điều 6: các hành vi sinh viên không được làm'})

            MERGE (p:Section {name: 'quy chế học vụ'})
            MERGE (p2:Part {name: 'chương 2: lập kế hoạch và tổ chức giảng dạy'})
            MERGE (p2_9:Article {name: 'điều 9: tổ chức đăng ký học tập'})
            MERGE (p2_10:Article {name: 'điều 10: tổ chức lớp học phần'})
            MERGE (p3:Part {name: 'chương 3: đánh giá kết quả học tập và cấp bằng tốt nghiệp'})
            MERGE (p3_12:Article {name: 'điều 12: tổ chức thi kết thúc học phần'})
            MERGE (p3_13:Article {name: 'điều 13: đánh giá và tính điểm học phần'})
            MERGE (p3_14:Article {name: 'điều 14: xét tương đường và công nhận học phần của các cơ sở đào tạo khác'})
            MERGE (p3_15:Article {name: 'điều 15: đánh giá kết quả học tập theo học kỳ, năm học'})
            MERGE (p3_16:Article {name: 'điều 16: thông báo kết quả học tập'})
            MERGE (p3_17:Article {name: 'điều 17: điểm rèn luyện(đrl)'})
            MERGE (p3_18:Article {name: 'điều 18: xử lý kết quả học tập'})
            MERGE (p3_19:Article {name: 'điều 19: khóa luận, tiểu luận, tích lũy tín chỉ tốt nghiệp'})
            MERGE (p3_20:Article {name: 'điều 20: công nhận tốt nghiệp và cấp bằng tốt nghiêp'})
            MERGE (p4:Part {name: 'chương 4: những quy định khác đối với sinh viên'})
            MERGE (p4_21:Article {name: 'điều 21: nghỉ học tạm thời, thôi học'})
            MERGE (p4_24:Article {name: 'điều 24: học cùng lúc hai chương trình'})

            MERGE (q:Section {name: 'quy định về việc đào tạo trực tuyến'})
            MERGE (q0_3:Article {name: 'điều 3: hệ thống đào tạo trực tuyến tại trường đại học nông lâm tp.hcm'})
            MERGE (q0_9:Article {name: 'điều 9: đánh giá kết quả học tập trực tuyến'})
            MERGE (q0_13:Article {name: 'điều 13: quyền và trách nhiệm của sinh viên'})

            MERGE (r:Section {name: 'quy định khen thưởng, kỷ luật sinh viên'})
            MERGE (r2:Part {name: 'chương 2: khen thưởng'})
            MERGE (r2_4:Article {name: 'điều 4: nội dung khen thưởng'})
            MERGE (r2_5:Article {name: 'điều 5: khen thưởng đối với cá nhân và tập thể sinh viên đạt thành tích xứng đánh để biểu dương, khen thưởng'})
            MERGE (r2_6:Article {name: 'điều 6: khen thưởng đối với sinh viên tiêu biểu(svtb) vào cuối mỗi năm học'})
            MERGE (r2_7:Article {name: 'điều 7: khen thưởng đối với sinh viên là thủ khoa, á khoa kỳ tuyển sinh đầu vào'})
            MERGE (r2_8:Article {name: 'điều 8: khen thưởng đối với sinh viên tốt nghiệp'})
            MERGE (r3:Part {name: 'chương 3: kỷ luật'})
            MERGE (r3_11:Article {name: 'điều 11: hình thức kỷ luật và nội dung vi phạm'})
            MERGE (r3_12:Article {name: 'điều 12: trình tự, thủ tục và hồ sơ xét kỷ luật'})
            MERGE (r3_13:Article {name: 'điều 13: chấm dứt hiệu lực của quyết định kỷ luật'})
            MERGE (r3_0:Article {name: 'một số nội dung vi phạm và khung xử lý kỷ luật sinh viên'})

            MERGE (s:Section {name: 'quy chế đánh giá kết quả rèn luyện'})
            MERGE (s0_3:Article {name: 'điều 3: nội dung đánh giá và thang điểm'})
            MERGE (s0_4:Article {name: 'điều 4: đánh giá về ý thức tham gia học tập'})
            MERGE (s0_5:Article {name: 'điều 5: đánh giá về ý thức chấp hành nội quy, quy chế, quy định trong cơ sở giáo dục đại học'})
            MERGE (s0_6:Article {name: 'điều 6: đánh giá về ý thức tham gia các hoạt động chính trị, xã hội, văn hóa, nghệ thuật, thể thao, phòng chống tội phạm và các tệ nạn xã hội'})
            MERGE (s0_7:Article {name: 'điều 7: đánh giá về ý thức công dân trong quản hệ cộng đồng'})
            MERGE (s0_8:Article {name: 'điều 8: Đánh giá về ý thức và kết quả khi tham gia công tác cán bộ lớp, các đoàn thể, tổ chức trong cơ sở giáo dục đại học hoặc người học đạt được thành tích đặc biệt trong học tập, rèn luyện'})
            MERGE (s0_9:Article {name: 'điều 9: phân loại kết quả rèn luyện'})
            MERGE (s0_10:Article {name: 'điều 10: phân loại để đánh giá'})
            MERGE (s0_11:Article {name: 'điều 11: quy trình đánh giá kết quả rèn luyện'})

            MERGE (t:Section {name: 'quy tắc ứng xử văn hóa của người học'})
            MERGE (t0_4:Article {name: 'điều 4: ứng xử với công tác học tập, nghiên cứu khoa học, rèn luyện'})
            MERGE (t0_5:Article {name: 'điều 5: ứng xử đối với giảng viên và nhân viên nhà trường'})
            MERGE (t0_6:Article {name: 'điều 6: ứng xử với bạn bè'})
            MERGE (t0_7:Article {name: 'điều 7: ứng xử với cảnh quan môi trường và tài sản công'})

            MERGE (u:Section {name: 'cố vấn học tập'})
            MERGE (v:Section {name: 'danh hiệu sinh viên 5 tốt'})
            MERGE (v0_1:Article {name: 'đạo đức tốt'})
            MERGE (v0_2:Article {name: 'học tập tốt'})
            MERGE (v0_3:Article {name: 'thể lực tốt'})
            MERGE (v0_4:Article {name: 'tình nguyện tốt'})
            MERGE (v0_5:Article {name: 'hội nhập tốt'})
            MERGE (v0_6:Article {name: 'khái niệm'})

            MERGE (v1:Part {name: 'ngoài ra ưu tiên xét chọn những sinh viên đạt ít nhất 01 trong các các tiêu chuẩn sau'})
            MERGE (v1_1:Article {name: 'ưu tiên 1'})
            MERGE (v1_2:Article {name: 'ưu tiên 2'})
            MERGE (v1_3:Article {name: 'ưu tiên 3'})
            MERGE (v1_4:Article {name: 'ưu tiên 4'})
            MERGE (v1_5:Article {name: 'ưu tiên 5'})
            MERGE (v1_6:Article {name: 'ưu tiên 6'})

            MERGE (w:Section {name: 'danh hiệu sinh viên tiêu biểu'})

            MERGE (n)-[:BAO_GỒM]->(o)
            MERGE (o)-[:BAO_GỒM]->(o2)
            MERGE (o2)-[:BAO_GỒM]->(o2_4)
            MERGE (o2)-[:BAO_GỒM]->(o2_5)
            MERGE (o2)-[:BAO_GỒM]->(o2_6)

            MERGE (n)-[:BAO_GỒM]->(p)
            MERGE (p)-[:BAO_GỒM]->(p2)
            MERGE (p2)-[:BAO_GỒM]->(p2_9)
            MERGE (p2)-[:BAO_GỒM]->(p2_10)
            MERGE (p)-[:BAO_GỒM]->(p3)
            MERGE (p3)-[:BAO_GỒM]->(p3_12)
            MERGE (p3)-[:BAO_GỒM]->(p3_13)
            MERGE (p3)-[:BAO_GỒM]->(p3_14)
            MERGE (p3)-[:BAO_GỒM]->(p3_15)
            MERGE (p3)-[:BAO_GỒM]->(p3_16)
            MERGE (p3)-[:BAO_GỒM]->(p3_17)
            MERGE (p3)-[:BAO_GỒM]->(p3_18)
            MERGE (p3)-[:BAO_GỒM]->(p3_19)
            MERGE (p3)-[:BAO_GỒM]->(p3_20)
            MERGE (p)-[:BAO_GỒM]->(p4)
            MERGE (p4)-[:BAO_GỒM]->(p4_21)
            MERGE (p4)-[:BAO_GỒM]->(p4_24)

            MERGE (n)-[:BAO_GỒM]->(q)
            MERGE (q)-[:BAO_GỒM]->(q0_3)
            MERGE (q)-[:BAO_GỒM]->(q0_9)
            MERGE (q)-[:BAO_GỒM]->(q0_13)

            MERGE (n)-[:BAO_GỒM]->(r)
            MERGE (r)-[:BAO_GỒM]->(r2)
            MERGE (r2)-[:BAO_GỒM]->(r2_4)
            MERGE (r2)-[:BAO_GỒM]->(r2_5)
            MERGE (r2)-[:BAO_GỒM]->(r2_6)
            MERGE (r2)-[:BAO_GỒM]->(r2_7)
            MERGE (r2)-[:BAO_GỒM]->(r2_8)
            MERGE (r)-[:BAO_GỒM]->(r3)
            MERGE (r3)-[:BAO_GỒM]->(r3_11)
            MERGE (r3)-[:BAO_GỒM]->(r3_12)
            MERGE (r3)-[:BAO_GỒM]->(r3_13)
            MERGE (r3)-[:BAO_GỒM]->(r3_0)

            MERGE (n)-[:BAO_GỒM]->(s)
            MERGE (s)-[:BAO_GỒM]->(s0_3)
            MERGE (s)-[:BAO_GỒM]->(s0_4)
            MERGE (s)-[:BAO_GỒM]->(s0_5)
            MERGE (s)-[:BAO_GỒM]->(s0_6)
            MERGE (s)-[:BAO_GỒM]->(s0_7)
            MERGE (s)-[:BAO_GỒM]->(s0_8)
            MERGE (s)-[:BAO_GỒM]->(s0_9)
            MERGE (s)-[:BAO_GỒM]->(s0_10)
            MERGE (s)-[:BAO_GỒM]->(s0_11)

            MERGE (n)-[:BAO_GỒM]->(t)
            MERGE (t)-[:BAO_GỒM]->(t0_4)
            MERGE (t)-[:BAO_GỒM]->(t0_5)
            MERGE (t)-[:BAO_GỒM]->(t0_6)
            MERGE (t)-[:BAO_GỒM]->(t0_7)

            MERGE (n)-[:BAO_GỒM]->(u)
            MERGE (n)-[:BAO_GỒM]->(v)
            MERGE (v)-[:BAO_GỒM]->(v0_1)
            MERGE (v)-[:BAO_GỒM]->(v0_2)
            MERGE (v)-[:BAO_GỒM]->(v0_3)
            MERGE (v)-[:BAO_GỒM]->(v0_4)
            MERGE (v)-[:BAO_GỒM]->(v0_5)
            MERGE (v)-[:BAO_GỒM]->(v0_6)
            MERGE (v)-[:BAO_GỒM]->(v1)
            MERGE (v1)-[:BAO_GỒM]->(v1_1)
            MERGE (v1)-[:BAO_GỒM]->(v1_2)
            MERGE (v1)-[:BAO_GỒM]->(v1_3)
            MERGE (v1)-[:BAO_GỒM]->(v1_4)
            MERGE (v1)-[:BAO_GỒM]->(v1_5)
            MERGE (v1)-[:BAO_GỒM]->(v1_6)

            MERGE (n)-[:BAO_GỒM]->(w)
            """,
            # Episode 3: hỗ trợ và dịch vụ
            """
            MERGE (x:Part {name: 'phần 3: hỗ trợ và dịch vụ'})
            MERGE (y:Section {name: 'quy định phân cấp giải quyết thắc mắc của sinh viên'})
            MERGE (y0_2:Article {name: 'điều 2: hình thức thắc mắc, kiến nghị'})
            MERGE (y0_3:Article {name: 'điều 3: các bước gửi thắc mắc, kiên nghị'})
            MERGE (y0_4:Article {name: 'điều 4: những vấn đề trao đổi trực tiếp hoặc gửi thư qua email'})
            MERGE (y0_5:Article {name: 'điều 5: trách nhiệm của giảng viên và các bộ phận chức năng'})
            MERGE (y0_6:Article {name: 'điều 6: những vấn đề đã trao đổi trực tiêp hoặc gửi thư không được giải quyết thoải đáng'})
            MERGE (y0_7:Article {name: 'điều 7: những vấn đề liên quan đến tổ chức lớp học phần'})
            MERGE (y0_8:Article {name: 'điều 8: những vấn đề liên quan đến điểm bộ phận, điểm thi kết thúc học phần, điểm thi học phần và tổ chức thi'})
            MERGE (y0_9:Article {name: 'điều 9; chuyển thắc mắc, kiến nghị của sinh viên'})
            MERGE (y0_10:Article {name: 'điều 10: những nội dung được nói trực tuyến trên website'})
            MERGE (y0_11:Article {name: 'điều 11: yêu cầu đối với sinh viên tham gia trực tuyến'})

            MERGE (z:Section {name: 'thông tin học bổng tài trợ'})
            MERGE (aa:Section {name: 'vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})
            MERGE (aa0_1:Article {name: 'đối tượng sinh viên được hỗ trợ vay tiền'})
            MERGE (aa0_2:Article {name: 'điều kiện để được hỗ trợ vay tiền sinh viên'})
            MERGE (aa0_3:Article {name: 'mức tiền và lãi suất hỗ trợ vay tiền sinh viên'})
            MERGE (aa0_4:Article {name: 'phương thức cho vay tiền sinh viên'})
            MERGE (aa0_5:Article {name: 'thông tin về vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})

            MERGE (bb:Section {name: 'quy trình xác nhận hồ sơ sinh viên'})
            MERGE (bb0_1:Article {name: 'các loại giấy tờ được xác nhận'})
            MERGE (bb0_2:Article {name: 'kênh đăng ký'})
            MERGE (bb0_3:Article {name: 'đăng ký'})
            MERGE (bb0_4:Article {name: 'quy trình'})

            MERGE (cc:Section {name: 'hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên'})
            MERGE (dd:Section {name: 'thông tin về bảo hiểm y tế'})

            MERGE (ee:Section {name: 'hướng dẫn sử dụng các kênh thanh toán học phí, bhyt, lệ phí xét tốt nghiệp'})
            MERGE (ee0_1:Article {name: 'thanh toán tại quầy giao dịch của bidv'})
            MERGE (ee0_2:Article {name: 'thanh toán qua kênh bidv smart banking'})
            MERGE (ee0_3:Article {name: 'thanh toán qua kênh bidv online'})
            MERGE (ee0_4:Article {name: 'thanh toán qua atm của bidv'})
            MERGE (ee0_5:Article {name: 'thanh toán qua website sinh viên'})
            MERGE (ee0_6:Article {name: 'hướng dẫn cài đặt sinh trắc học'})

            MERGE (ff:Section {name: 'tham vấn tâm lý học đường'})
            MERGE (gg:Section {name: 'trung tâm dịch vụ sinh viên'})

            MERGE (mm:Section {name: 'thông tin học bổng khuyến khích học tập'})
            MERGE (mm0_1:Article {name: 'đối tượng'})
            MERGE (mm0_2:Article {name: 'quỹ học bổng khuyến khích học tập'})
            MERGE (mm0_3:Article {name: 'căn cứ để xét học bổng khuyến khích học tập'})
            MERGE (mm0_4:Article {name: 'mức học bổng khuyến khích học tập'})
            MERGE (mm0_5:Article {name: 'quy trình xét học bổng'})

            MERGE (x)-[:BAO_GỒM]->(y)
            MERGE (y)-[:BAO_GỒM]->(y0_2)
            MERGE (y)-[:BAO_GỒM]->(y0_3)
            MERGE (y)-[:BAO_GỒM]->(y0_4)
            MERGE (y)-[:BAO_GỒM]->(y0_5)
            MERGE (y)-[:BAO_GỒM]->(y0_6)
            MERGE (y)-[:BAO_GỒM]->(y0_7)
            MERGE (y)-[:BAO_GỒM]->(y0_8)
            MERGE (y)-[:BAO_GỒM]->(y0_9)
            MERGE (y)-[:BAO_GỒM]->(y0_10)
            MERGE (y)-[:BAO_GỒM]->(y0_11)

            MERGE (x)-[:BAO_GỒM]->(z)
            MERGE (x)-[:BAO_GỒM]->(aa)
            MERGE (aa)-[:BAO_GỒM]->(aa0_1)
            MERGE (aa)-[:BAO_GỒM]->(aa0_2)
            MERGE (aa)-[:BAO_GỒM]->(aa0_3)
            MERGE (aa)-[:BAO_GỒM]->(aa0_4)
            MERGE (aa)-[:BAO_GỒM]->(aa0_5)

            MERGE (x)-[:BAO_GỒM]->(bb)
            MERGE (bb)-[:BAO_GỒM]->(bb0_1)
            MERGE (bb)-[:BAO_GỒM]->(bb0_2)
            MERGE (bb)-[:BAO_GỒM]->(bb0_3)
            MERGE (bb)-[:BAO_GỒM]->(bb0_4)

            MERGE (x)-[:BAO_GỒM]->(cc)
            MERGE (x)-[:BAO_GỒM]->(dd)
            MERGE (x)-[:BAO_GỒM]->(ee)
            MERGE (ee)-[:BAO_GỒM]->(ee0_1)
            MERGE (ee)-[:BAO_GỒM]->(ee0_2)
            MERGE (ee)-[:BAO_GỒM]->(ee0_3)
            MERGE (ee)-[:BAO_GỒM]->(ee0_4)
            MERGE (ee)-[:BAO_GỒM]->(ee0_5)
            MERGE (ee)-[:BAO_GỒM]->(ee0_6)

            MERGE (x)-[:BAO_GỒM]->(ff)
            MERGE (x)-[:BAO_GỒM]->(gg)
            MERGE (x)-[:BAO_GỒM]->(mm)
            MERGE (mm)-[:BAO_GỒM]->(mm0_1)
            MERGE (mm)-[:BAO_GỒM]->(mm0_2)
            MERGE (mm)-[:BAO_GỒM]->(mm0_3)
            MERGE (mm)-[:BAO_GỒM]->(mm0_4)
            MERGE (mm)-[:BAO_GỒM]->(mm0_5)
            """
        ]
        for query in cypher_queries:
            self.execute_cypher(query)

    def get_owned_entities(self, type, source, relation):
        query = f"""
            MATCH (o:{type} {{name: "{source}"}})-[r:{relation}]->(e)
            RETURN o AS source, r AS relationship, e AS target
        """

        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]



    def get_path(self, cypher_query):
        with self.driver.session() as session:
            result = session.run(cypher_query)
            return [record for record in result]


    def create_documents(self, records):
        documents = []

        for record in records:
            relations = record["relation"]

            for rel in relations:
                source_node = rel.start_node
                target_node = rel.end_node
                relation_type = rel.type

                # Lấy thuộc tính của nguồn và đích
                source_properties = dict(source_node)
                target_properties = dict(target_node)

                # Chuyển thuộc tính thành chuỗi
                source_str = str(source_properties) if source_properties else "{}"
                target_str = str(target_properties) if target_properties else "{}"

                # Tạo triplet dạng chuỗi
                triplet = f"{source_str} -> {relation_type} -> {target_str}"
                documents.append(triplet)

        return documents

    def import_relationships(self, content, Part, type_Part):
        relationships = content["relationships"]
        with self.driver.session() as session:
            for rel in relationships:
                source = rel["source"]
                target = rel["target"]
                relation = rel["relation"].upper()  # IN HOA
                print(f'{source} {relation} {target}')
                type_source = self._capitalize_label(rel["type_source"])
                type_target = self._capitalize_label(rel["type_target"])
                type_Part_cap = self._capitalize_label(type_Part)

                session.execute_write(
                    self._create_relation_with_Part,
                    source, type_source,
                    target, type_target,
                    relation,
                    Part, type_Part_cap
                )

    @staticmethod
    def _capitalize_label(label):
        # Chuyển thành PascalCase: "university_branch" -> "UniversityBranch"
        return ''.join(word.capitalize() for word in label.split('_'))

    @staticmethod
    def _create_relation_with_Part(tx, source, type_source, target, type_target, relation, Part, type_Part):
        query = f"""
           MERGE (src:{type_source} {{name: $source_name}})
           SET src += $source_props

           MERGE (tgt:{type_target} {{name: $target_name}})
           SET tgt += $target_props

           MERGE (Part:{type_Part} {{name: $Part}})
           MERGE (src)-[:{relation}]->(tgt)
           MERGE (Part)-[:BAO_GỒM]->(src)
           """
        tx.run(query,
               source_name=source["name"],
               source_props=source,
               target_name=target["name"],
               target_props=target,
               Part=Part
               )

