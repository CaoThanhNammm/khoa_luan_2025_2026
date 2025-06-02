from neo4j import GraphDatabase
import json

NEO4J_URI="neo4j+s://d66e5cf5.databases.neo4j.io"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="q45B_EoJSMdRnTva0JIUArn3IcJjOdfXQOITT7OrU_w"

# Đọc file JSON chứa câu lệnh Cypher
with open(r"C:\Users\Nam\Downloads\neo4j_query_table_data_2025-5-20.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cypher_statements = data[0]["cypherStatements"]

# Kết nối đến Neo4j và chạy các câu lệnh Cypher
def run_cypher_script(cypher_script):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        for statement in cypher_script.split(";\n"):
            stmt = statement.strip()
            if stmt:  # bỏ qua dòng trống
                try:
                    session.run(stmt)
                    print(f"✅ Executed: {stmt[:60]}...")
                except Exception as e:
                    print(f"❌ Error executing: {stmt[:60]}...\n{e}")
    driver.close()

# Thực thi
run_cypher_script(cypher_statements)
