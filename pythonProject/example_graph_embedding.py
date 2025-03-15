import general
from neo4j import GraphDatabase
import numpy as np
from sentence_transformers import SentenceTransformer


# Kết nối tới Neo4j
driver = general.connect_to_graph_db()
# Hàm tạo 20 node và relationship
def create_graph(tx):
    tx.run("MATCH (n) DETACH DELETE n")
    for i in range(10):
        tx.run("CREATE (p:Person {name: $name})", name=f"Person_{i}")
        tx.run("CREATE (a:Article {title: $title})", title=f"Article_{i}")
    for i in range(10):
        tx.run("""
            MATCH (p:Person {name: $person}), (a:Article {title: $article})
            CREATE (p)-[:WROTE]->(a)
        """, person=f"Person_{i}", article=f"Article_{i}")


# Hàm nhúng node bằng SentenceTransformer (cho Person và Article)
def embed_nodes(tx):
    # Khởi tạo SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Lấy tất cả Person và nhúng
    persons = tx.run("MATCH (p:Person) RETURN p.name AS name")
    person_embeddings = {}
    for record in persons:
        name = record["name"]
        embedding = model.encode(name)  # Tạo embedding từ name
        person_embeddings[name] = embedding
        tx.run("""
            MATCH (p:Person {name: $name})
            SET p.embedding = $embedding
        """, name=name, embedding=embedding.tolist())

    # Lấy tất cả Article và nhúng
    articles = tx.run("MATCH (a:Article) RETURN a.title AS title")
    article_embeddings = {}
    for record in articles:
        title = record["title"]
        embedding = model.encode(title)  # Tạo embedding từ title
        article_embeddings[title] = embedding
        tx.run("""
            MATCH (a:Article {title: $title})
            SET a.embedding = $embedding
        """, title=title, embedding=embedding.tolist())

    # Gộp embedding vào một dictionary chung
    embeddings = {**person_embeddings, **article_embeddings}
    return embeddings


# Hàm truy xuất thông tin dựa trên truy vấn
def retrieve_info(query, embeddings):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query)

    similarities = {}
    for name, emb in embeddings.items():
        similarity = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
        similarities[name] = similarity

    top_matches = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_matches


# Hàm chính
def main():
    with driver.session() as session:
        print("Creating nodes and relationships...")
        session.write_transaction(create_graph)

        print("Embedding nodes with SentenceTransformer...")
        embeddings = session.write_transaction(embed_nodes)

        query = "Who wrote an article 6?"
        print(f"Query: {query}")
        top_matches = retrieve_info(query, embeddings)

        print("Top matching nodes:")
        for name, score in top_matches:
            print(f"Node: {name}, Similarity: {score:.4f}")

    driver.close()


if __name__ == "__main__":
    main()
