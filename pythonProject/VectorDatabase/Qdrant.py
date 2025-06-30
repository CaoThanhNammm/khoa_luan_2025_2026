from qdrant_client.models import PointStruct
from dotenv import load_dotenv
load_dotenv()
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain_core.documents import Document
from qdrant_client import models
from qdrant_client import QdrantClient
import os


class Qdrant:
    def __init__(self, host, api, model_1024, model_768, model_512, model_late_interaction, collection_name, pre_processing):
        self.client = QdrantClient(
            url=host,
            api_key=api,
        )
        self.collection_name = collection_name
        self.model_1024 = model_1024
        self.model_768 = model_768
        self.model_512 = model_512
        self.model_late_interaction = model_late_interaction
        self.pre_processing = pre_processing

    def create_collection(self, collection_name, size, distance):
        if self.client.collection_exists(collection_name=collection_name):
            return

        hnsw_config = {
            "m": 16,  # Số kết nối tối đa cho mỗi nút trong đồ thị (mặc định: 16)
            "ef_construct": 1000,  # Yếu tố xây dựng, ảnh hưởng đến chất lượng index (mặc định: 100)
            "full_scan_threshold": 10000  # Ngưỡng để chuyển sang quét toàn bộ nếu tập dữ liệu nhỏ
        }

        # Tạo collection với cấu hình vectors và HNSW
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config={
                'matryoshka-1024dim': models.VectorParams(
                    size=size,
                    distance=models.Distance[distance.upper()],
                    datatype=models.Datatype.FLOAT32
                ),
                'matryoshka-768dim': models.VectorParams(
                    size=768,
                    distance=models.Distance[distance.upper()],
                    datatype=models.Datatype.FLOAT32
                ),
                'matryoshka-512dim': models.VectorParams(
                    size=512,
                    distance=models.Distance[distance.upper()],
                    datatype=models.Datatype.FLOAT32
                ),
                'late_interaction': models.VectorParams(
                    size=768,
                    distance=models.Distance[distance.upper()],
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM
                    ),
                    datatype=models.Datatype.FLOAT32
                )
            },
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True,
                ),
            ),
            hnsw_config=hnsw_config  # Thêm cấu hình HNSW
        )
        print("create collection success")
        return self.client

    def delete_collection(self, collection_name):
        if self.client.collection_exists(collection_name=collection_name):
            self.client.delete_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' has been deleted.")
        else:
            print(f"Collection '{collection_name}' does not exist.")

    def create_embedding(self, chunks):
        points = []
        batch_size = 20


        for chunk_id, chunk_text in enumerate(chunks, 1):
            chunk_text_pre_processing = self.pre_processing.text_preprocessing_vietnamese(chunk_text)
            print(chunk_text)

            try:
                # Tạo embeddings song song nếu có thể
                embeddings = {
                    'matryoshka-1024dim': self.model_1024.embed(chunk_text_pre_processing),
                    'matryoshka-768dim': self.model_768.embed(chunk_text_pre_processing),
                    'matryoshka-512dim': self.model_512.embed(chunk_text_pre_processing),
                    'late_interaction': self.model_late_interaction.embed(chunk_text_pre_processing)
                }

                # Tạo PointStruct với cách viết gọn hơn
                points.append(
                    PointStruct(
                        id=chunk_id,
                        payload={"text": chunk_text},
                        vector=embeddings
                    )
                )

                print(f"Processed chunk {chunk_id}")

                # Batch processing
                if len(points) >= batch_size:
                    self._upsert_points(points)
                    points.clear()

            except Exception as e:
                print(f"Error processing chunk {chunk_id}: {e}")
                continue

        # Xử lý các points còn lại
        if points:
            self._upsert_points(points)

        print("Embedding creation completed successfully")

    def _upsert_points(self, points):
        """Helper method để upsert points vào VDB"""
        try:
            self.client.upsert(self.collection_name, points)
            print(f"Upserted {len(points)} points to VDB")
        except Exception as e:
            print(f"Error upserting points: {e}")

    def query_from_db(self, text):
      text_embedded_512 = self.model_512.embed(text)
      text_embedded_768 = self.model_768.embed(text)
      text_embedded_1024 = self.model_1024.embed(text)
      embedded_late_interaction = self.model_late_interaction.embed(text).cpu().numpy()

      response =  self.client.query_points(
            collection_name= self.collection_name,
            prefetch=models.Prefetch(
                prefetch=models.Prefetch(
                    prefetch=models.Prefetch(
                        query=text_embedded_512,
                        using="matryoshka-512dim",
                        limit=200,
                    ),
                    query=text_embedded_768,
                    using="matryoshka-768dim",
                    limit=100,
                ),
                query=text_embedded_1024,
                using="matryoshka-1024dim",
                limit=50,
            ),
            query=embedded_late_interaction,
            using="late_interaction",
            limit=25,
        )
      documents = []
      for result in response.points:
        documents.append(result.payload["text"])
      return documents

    def re_ranking(self, query, passages):
        client = NVIDIARerank(
            model="nvidia/llama-3.2-nv-rerankqa-1b-v2",
            api_key=os.getenv('API_KEY_RERANKING'),

            top_n=len(passages)
        )

        response = client.compress_documents(
            query=query,
            documents=[Document(page_content=passage) for passage in passages]
        )
        return response


