from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from dotenv import load_dotenv
load_dotenv()
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain_core.documents import Document
from qdrant_client import models
import os
import pdfplumber

class Qdrant:
    def __init__(self, host, port, model_1024, model_768, model_512, model_late_interaction, collection_name):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.model_1024 = model_1024
        self.model_768 = model_768
        self.model_512 = model_512
        self.model_late_interaction = model_late_interaction

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

    # đọc tất cả file pdf trong thư mục {data_path}. Mỗi lần đọc 3 trang
    # trả về danh sách các nội dung bao gồm của 3 trang được ghép thành 1
    def read_chunks(self, data_path, footer_height=40):
        all_pages_text = []
        pdf_files = [f for f in os.listdir(data_path) if f.lower().endswith('.pdf')]

        for pdf_file in pdf_files:
            pdf_path = os.path.join(data_path, pdf_file)

            try:
                with pdfplumber.open(pdf_path) as pdf:
                    num_pages = len(pdf.pages)
                    start_page = 10
                    end_page = num_pages - 2

                    # Duyệt qua các trang theo nhóm 3
                    for i in range(start_page, end_page + 1, 3):
                        group_text = []
                        group_pages = []

                        # Lấy tối đa 3 trang liên tiếp
                        for j in range(i, min(i + 3, end_page + 1)):
                            page = pdf.pages[j]
                            page_height = page.height

                            # Chỉ cắt bỏ footer
                            cropped_page = page.within_bbox(
                                (0, 0, page.width, page_height - footer_height)
                            )
                            text = cropped_page.extract_text()
                            if text:
                                group_text.append(text)
                                group_pages.append(j + 1)  # Số trang người dùng thấy (bắt đầu từ 1)

                        if group_text:  # Chỉ thêm nếu có text
                            all_pages_text.append('\n'.join(group_text))
            except Exception as e:
                print(f"Lỗi khi xử lý file {pdf_file}: {str(e)}")

        return all_pages_text

    def create_embedding(self, chunks):
        try:
            model_embed_1024, tokenizer_1024 = self.model_1024.load_model()
            model_embed_768, tokenizer_768 = self.model_768.load_model()
            model_embed_512 = self.model_512.load_model()
            model_embed_late_interaction, tokenizer_late_interaction = self.model_late_interaction.load_model()
        except Exception as e:
            print(f"Error loading models: {e}")
            return

        points = []
        batch_size = 20

        # Sử dụng enumerate thay vì range(len())
        for chunk_id, chunk_text in enumerate(chunks, 1):
            print(chunk_text)
            try:
                # Tạo embeddings song song nếu có thể
                embeddings = {
                    'matryoshka-1024dim': self.model_1024.embed(model_embed_1024, tokenizer_1024, chunk_text),
                    'matryoshka-768dim': self.model_768.embed(model_embed_768, tokenizer_768, chunk_text),
                    'matryoshka-512dim': self.model_512.embed(model_embed_512, None, chunk_text),
                    'late_interaction': self.model_late_interaction.embed(model_embed_late_interaction,
                                                                          tokenizer_late_interaction,
                                                                          chunk_text)
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


    def query_from_db(self, text_embedded_512, text_embedded_768, text_embedded_1024, embedded_late_interaction):
        return self.client.query_points(
            collection_name= self.collection_name,
            prefetch=models.Prefetch(
                prefetch=models.Prefetch(
                    prefetch=models.Prefetch(
                        query=text_embedded_512,
                        using="matryoshka-512dim",
                        limit=100,
                    ),
                    query=text_embedded_768,
                    using="matryoshka-768dim",
                    limit=75,
                ),
                query=text_embedded_1024,
                using="matryoshka-1024dim",
                limit=25,
            ),
            query=embedded_late_interaction,
            using="late_interaction",
            limit=5,
        ).points

    def re_ranking(self, query, passages):
        client = NVIDIARerank(
            model="nvidia/llama-3.2-nv-rerankqa-1b-v2",
            api_key=os.getenv("API_KEY_RERANKING"),
        )

        response = client.compress_documents(
            query=query,
            documents=[Document(page_content=passage) for passage in passages]
        )

        return response
