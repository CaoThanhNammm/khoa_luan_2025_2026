from langchain.text_splitter import SpacyTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from qdrant_client.models import PointStruct

load_dotenv()
from dotenv import load_dotenv

load_dotenv()
import general
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain_core.documents import Document
from qdrant_client import models
import os
from dotenv import load_dotenv
load_dotenv()


class VectorDatabase:
    def __init__(self, host, port, model_1024, model_768, model_512, model_late_interaction, model_splade_doc, collection_name):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.model_1024 = model_1024
        self.model_768 = model_768
        self.model_512 = model_512
        self.model_late_interaction = model_late_interaction
        self.model_splade_doc = model_splade_doc

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
            sparse_vectors_config={
                "sparse": models.SparseVectorParams()
            },
            hnsw_config=hnsw_config  # Thêm cấu hình HNSW
        )
        print("create collection success")
        return self.client

    def read_chunks(self, data_path, chunk_size=700, chunk_overlap=140):
        # Khai báo loader để quét toàn bộ thư mục data
        loader = DirectoryLoader(data_path, glob="*.pdf", use_multithreading=True,
                                 loader_cls=PyMuPDFLoader)  # type: ignore
        documents = loader.load()

        # Chỉ lấy từ trang 4 trở đi vì trang đầu thường là bìa sách và mục lục
        documents = documents[4:len(documents) - 2]

        # Sử dụng TextSplitter để chia nhỏ văn bản
        text_splitter = SpacyTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)

        print("Read chunk success")
        return chunks

    def create_embedding(self, chunks):
        model_embed_1024, tokenizer_1024 = self.model_1024.load_model()
        model_embed_768, tokenizer_768 = self.model_768.load_model()
        model_embed_512 = self.model_512.load_model()
        model_embed_late_interaction, tokenizer_late_interaction = self.model_late_interaction.load_model()
        model_splade_doc, tokenizer_splade_doc = self.model_splade_doc.load_model()

        vncorenlp = general.load_vncorenlp()
        points = []
        id = 1

        for chunk in range(len(chunks)):
            try:
                metadata = chunks[chunk].metadata
                content = chunks[chunk].page_content

                text_pre_processing = general.text_preprocessing_vietnamese(content, vncorenlp)

                embedded_text_1024 = self.model_1024.embed(model_embed_1024, tokenizer_1024, text_pre_processing)
                embedded_text_768 = self.model_768.embed(model_embed_768, tokenizer_768, text_pre_processing)
                embedded_text_512 = self.model_512.embed(model_embed_512, None, text_pre_processing)

                doc_vec, doc_tokens = general.compute_vector(text_pre_processing, model=model_splade_doc,
                                                             tokenizer=tokenizer_splade_doc)
                sorted_tokens_doc = general.extract_and_map_sparse_vector(doc_vec, tokenizer_splade_doc)

                embedded_late_interaction = self.model_late_interaction.embed(model_embed_late_interaction,
                                                                                   tokenizer_late_interaction,
                                                                                   text_pre_processing)

                indices = tokenizer_splade_doc.convert_tokens_to_ids(sorted_tokens_doc)
                values = list(sorted_tokens_doc.values())

                points.append(
                    PointStruct(
                        id=id,
                        payload={"text": content, "metadata": metadata},
                        vector={
                            'matryoshka-1024dim': embedded_text_1024,
                            'matryoshka-768dim': embedded_text_768,
                            'matryoshka-512dim': embedded_text_512,
                            'sparse': models.SparseVector(indices=indices, values=values),
                            'late_interaction': embedded_late_interaction
                        }
                    )
                )
                print(id)
                if len(points) == 20:
                    print('Thêm vào VDB')
                    self.client.upsert(self.collection_name, points)
                    points.clear()

                id += 1
            except Exception as e:
                print(e)
                continue

        if points:  # Thêm các points còn lại nếu có
            self.client.upsert(self.collection_name, points)

        print("create embedding success")


    def query_from_db(self, text_embedded_1024, text_embedded_768, text_embedded_512, embedded_late_interaction):
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
                    limit=50,
                ),
                query=text_embedded_1024,
                using="matryoshka-1024dim",
                limit=25,
            ),
            query=embedded_late_interaction,
            using="late_interaction",
            limit=10,
        ).points

    def re_ranking(query, query_text_json):
        client = NVIDIARerank(
            model="nvidia/nv-rerankqa-mistral-4b-v3",
            api_key=os.getenv("API_KEY_RERANKING"),
        )

        response = client.compress_documents(
            query=query,
            documents=[Document(page_content=passage) for passage in query_text_json]
        )

        return response
