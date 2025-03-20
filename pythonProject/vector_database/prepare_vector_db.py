import os
from dotenv import load_dotenv

from ModelLLM.EmbeddingFactory import EmbeddingFactory
load_dotenv()
from vector_database.VectorDatabase import VectorDatabase


if __name__ == "__main__":
    # 1. sử dụng factory để khởi tạo các clas model embed
    model_embedding_1024_name = os.getenv("model_embedding_1024")
    model_embedding_768_name = os.getenv("model_embedding_768")
    model_embedding_512_name = os.getenv("model_embedding_512")
    model_late_interaction_name = os.getenv("model_late_interaction")
    model_splade_doc_name = os.getenv("model_splade_doc")

    factory = EmbeddingFactory()
    model_1024 = factory.create_embedding_model(model_embedding_1024_name)
    model_768 = factory.create_embedding_model(model_embedding_768_name)
    model_512 = factory.create_embedding_model(model_embedding_512_name)
    model_late_interaction = factory.create_embedding_model(model_late_interaction_name)
    model_doc = factory.create_embedding_model(model_splade_doc_name)


    # 3. Khởi tạo client Qdrant
    url = os.getenv("url")
    collection_name = os.getenv("name_collection")
    size = os.getenv("size")
    distance = os.getenv("distance")
    qdrant = VectorDatabase("localhost", 6333, model_1024, model_768, model_512, model_late_interaction, model_doc, collection_name)

    # 4. tạo collection, nếu có rồi thì không tạo nữa
    qdrant.create_collection(collection_name, size, distance)

    # 5. lấy ra chunks trong tất cả các doc
    data_path = os.getenv("data_path")
    chunks = qdrant.read_chunks(data_path)

    # 6. tạo embedding
    qdrant.create_embedding(chunks)





















