import os
from dotenv import load_dotenv
from ModelLLM.EmbeddingFactory import EmbeddingFactory
from VectorDatabase.Qdrant import Qdrant
load_dotenv()

if __name__ == "__main__":
    # 1. sử dụng factory để khởi tạo các clas model embed
    model_embedding_1024_name = os.getenv("MODEL_EMBEDDING_1024")
    model_embedding_768_name = os.getenv("MODEL_EMBEDDING_768")
    model_embedding_512_name = os.getenv("MODEL_EMBEDDING_512")
    model_late_interaction_name = os.getenv("MODEL_LATE_INTERACTION")

    factory = EmbeddingFactory()
    model_1024 = factory.create_embedding_model(model_embedding_1024_name)
    model_768 = factory.create_embedding_model(model_embedding_768_name)
    model_512 = factory.create_embedding_model(model_embedding_512_name)
    model_late_interaction = factory.create_embedding_model(model_late_interaction_name)

    # 3. Khởi tạo client Qdrant
    collection_name = os.getenv("NAME_COLLECTION")
    size = os.getenv("SIZE")
    distance = os.getenv("DISTANCE")
    qdrant = Qdrant("localhost", 6333, model_1024, model_768, model_512, model_late_interaction, collection_name)

    # 4. tạo collection, nếu có rồi thì không tạo nữa
    qdrant.create_collection(collection_name, size, distance)

    # 5. lấy ra chunks trong tất cả các doc
    data_path = os.getenv("DATA_PATH")
    chunks = qdrant.read_chunks(data_path)

    # 6. tiền xử lý dữ liệu

    # 7. tạo embedding
    qdrant.create_embedding(chunks)





















