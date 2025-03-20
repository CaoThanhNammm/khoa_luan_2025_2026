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
            MERGE (a:episode {name: 'phần 1: nlu - định hướng trường đại học nghiên cứu'}) 
            MERGE (b:part {name: 'quá trình hình thành và phát triển'}) 
            MERGE (c:part {name: 'sứ mạng'}) 
            MERGE (d:part {name: 'tầm nhìn'}) 
            MERGE (e:part {name: 'giá trị cốt lõi'}) 
            MERGE (f:part {name: 'mục tiêu chiến lược'}) 
            MERGE (g:part {name: 'cơ sở vật chất'}) 
            MERGE (h:part {name: 'các đơn vị trong trường'}) 
            MERGE (i:part {name: 'các khoa - ngành đào tạo'}) 
            MERGE (j:part {name: 'tuần sinh hoạt công dân - sinh viên'}) 
            MERGE (k:part {name: 'hoạt động phong trào sinh viên'}) 
            MERGE (l:part {name: 'câu lạc bộ (clb) - đội, nhóm'}) 
            MERGE (m:part {name: 'cơ sở đào tạo'})
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
            MERGE (n:episode {name: 'phần 2: học tập và rèn luyện'}) 
            MERGE (o:part {name: 'quy chế sinh viên'}) 
            MERGE (p:part {name: 'quy chế học vụ'}) 
            MERGE (q:part {name: 'quy định về việc đào tạo trực tuyến'}) 
            MERGE (r:part {name: 'quy định khen thưởng, kỷ luật sinh viên'}) 
            MERGE (s:part {name: 'quy chế đánh giá kết quả rèn luyện'}) 
            MERGE (t:part {name: 'quy tắc ứng xử văn hóa của người học'}) 
            MERGE (u:part {name: 'cố vấn học tập'}) 
            MERGE (v:part {name: 'danh hiệu sinh viên 5 tốt'}) 
            MERGE (w:part {name: 'danh hiệu sinh viên tiêu biểu'})
            MERGE (n)-[:BAO_GỒM]->(o)
            MERGE (n)-[:BAO_GỒM]->(p)
            MERGE (n)-[:BAO_GỒM]->(q)
            MERGE (n)-[:BAO_GỒM]->(r)
            MERGE (n)-[:BAO_GỒM]->(s)
            MERGE (n)-[:BAO_GỒM]->(t)
            MERGE (n)-[:BAO_GỒM]->(u)
            MERGE (n)-[:BAO_GỒM]->(v)
            MERGE (n)-[:BAO_GỒM]->(w)
            """,
            # Episode 3: hỗ trợ và dịch vụ
            """
            MERGE (x:episode {name: 'phần 3: hỗ trợ và dịch vụ'}) 
            MERGE (y:part {name: 'quy định phân cấp giải quyết thắc mắc của sinh viên'}) 
            MERGE (z:part {name: 'thông tin học bổng'}) 
            MERGE (aa:part {name: 'vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'}) 
            MERGE (bb:part {name: 'quy trình xác nhận hồ sơ sinh viên'}) 
            MERGE (cc:part {name: 'hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên'}) 
            MERGE (dd:part {name: 'thông tin về bảo hiểm y tế'}) 
            MERGE (ee:part {name: 'hướng dẫn sử dụng các kênh thanh toán học phí, bhyt, lệ phí xét tốt nghiệp'}) 
            MERGE (ff:part {name: 'tham vấn tâm lý học đường'}) 
            MERGE (gg:part {name: 'trung tâm dịch vụ sinh viên'})
            MERGE (mm:part {name: 'thông tin học bổng khuyến khích học tập'})
            MERGE (x)-[:BAO_GỒM]->(y)
            MERGE (x)-[:BAO_GỒM]->(z)
            MERGE (x)-[:BAO_GỒM]->(aa)
            MERGE (x)-[:BAO_GỒM]->(bb)
            MERGE (x)-[:BAO_GỒM]->(cc)
            MERGE (x)-[:BAO_GỒM]->(dd)
            MERGE (x)-[:BAO_GỒM]->(ee)
            MERGE (x)-[:BAO_GỒM]->(ff)
            MERGE (x)-[:BAO_GỒM]->(gg)
            MERGE (x)-[:BAO_GỒM]->(mm)
            """
        ]
        for query in cypher_queries:
            self.execute_cypher(query)

    def add_entities(self, entities):
        def _add_entities(tx, entities):
            for entity in entities:
                print(entity)
                name = entity["name"]
                entity_type = entity["type"]
                query = f"MERGE (e:{entity_type} {{name: $name}})"
                tx.run(query, name=name)

        with self.driver.session() as session:
            session.execute_write(_add_entities, entities)

    def add_relationships(self, relationships, part=None):
        """Thêm các relationships vào Neo4j"""

        def _add_relationships(tx, relationships, part):
            for rel in relationships:
                source = rel["source"]
                target = rel["target"]
                relation = rel["relation"]
                type_source = rel["type_source"]
                type_target = rel["type_target"]

                # Sử dụng APOC để merge mối quan hệ với nhãn động, tránh tạo quan hệ trùng lặp
                query = """
                    MATCH (source:%s {name: $source})
                    MATCH (target:%s {name: $target})
                    CALL apoc.merge.relationship(source, $relation, {}, {}, target)
                    YIELD rel
                    RETURN rel
                """ % (type_source, type_target)
                tx.run(query, source=source, target=target, relation=relation)

                # Nếu part được cung cấp, tạo mối quan hệ BAO_GỒM từ part đến source
                if part:
                    part_query = """
                        MATCH (p:part {name: $part})
                        MATCH (s)
                        WHERE $type_source IN labels(s) AND s.name = $source
                        MERGE (p)-[:BAO_GỒM]->(s)
                    """
                    tx.run(part_query, part=part, source=source, type_source=type_source)

        with self.driver.session() as session:
            session.execute_write(_add_relationships, relationships, part)

    def get_path(self, type, part):
        """Lấy danh sách các phần từ một episode cụ thể"""
        query = f"""
                MATCH (n:{type} {{name: "{part}"}})-[r*]->(m)
                RETURN n AS source, r AS relation, m AS target
            """

        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

    def get_owned_entities(self, type, source, relation):
        query = f"""
            MATCH (o:{type} {{name: "{source}"}})-[r:{relation}]->(e)
            RETURN o AS source, r AS relationship, e AS target
        """

        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

    # Hàm chạy câu lệnh Cypher
    def run_cypher_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                return query

    # Lấy tất cả node
    def get_all_nodes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN n, labels(n) AS labels")
            nodes = [{"name": record["n"].get("name", ""), "type": record["labels"][0]}
                        for record in result]
            return nodes

    # Lấy tất cả node và relationship
    def get_all_nodes_and_relationships(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n)-[r]->(m) RETURN n, type(r) AS rel_type, m")
            data = [{"source": record["n"].get("name", ""),
                        "relation": record["rel_type"],
                        "target": record["m"].get("name", "")}
                    for record in result]
            return data