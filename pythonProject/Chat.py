from LLM.Gemini import Gemini
import LLM.prompt as prompt
from ModelLLM.EmbeddingFactory import EmbeddingFactory
from VectorDatabase.Qdrant import Qdrant
from dotenv import load_dotenv
from knowledge_graph.GCN import GCN
from knowledge_graph.create_entities_relationship_kb import pre_processing
load_dotenv()
from knowledge_graph.KnowledgeGraphDatabase import Neo4j
import os
import torch
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import PromptTemplate
import math
from torch_geometric.data import Data


class Chat:
    def __init__(self, t, question, pre_processing):
        self.t = t
        self.question = question
        self.pre_processing = pre_processing
        self.references_final = ""
        self.extract = ""
        self.feedback = ""
        self.answer_final = ""

        # 1. khởi tạo gemini và chat
        model_name_15_flash = os.getenv('MODEL_15_FLASH')
        model_name_20_flash = os.getenv('MODEL_20_FLASH')
        model_name_25_flash = os.getenv('MODEL_25_FLASH')

        # api_key_agent = os.getenv('API_KEY_AGENT')
        # api_key_generator = os.getenv('API_KEY_GENERATOR')
        # api_key_valid = os.getenv('API_KEY_VALID')
        # api_key_commentor = os.getenv('API_KEY_COMMENTOR')

        api_key_generator = "AIzaSyDJOnB0i3Kr4FOk_4mINN9wETWLlV7jdRc"
        api_key_commentor = "AIzaSyBHEUQT-1f1NbZji3LsvYyVBiNxNPShzFg"
        # api_key_generator = "AIzaSyBpbQbmZek3VC98sGoKJV0hSWiBNbuaKRY" # pha
        api_key_valid = "AIzaSyBHEUQT-1f1NbZji3LsvYyVBiNxNPShzFg"
        api_key_agent = "AIzaSyDJOnB0i3Kr4FOk_4mINN9wETWLlV7jdRc"
        # api_key_generator = "AIzaSyC9JFA36xRYLaS9TAbOfrefpHkPFZEbiRU" # pha

        self.gemini_agent = Gemini(model_name_25_flash, api_key_agent)
        self.gemini_generator = Gemini(model_name_20_flash, api_key_generator)
        self.gemini_valid = Gemini(model_name_15_flash, api_key_valid)
        self.gemini_commentor = Gemini(model_name_15_flash, api_key_commentor)

        self._initialize_embedding_models()
        # host = os.getenv('HOST_QDRANT')
        # api = os.getenv("API_KEY_QDRANT")
        host = "https://0d9e031b-a61d-479b-8a5e-1b1aeeba93a0.us-west-1-0.aws.cloud.qdrant.io:6333"
        api = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.kVTMd_unNC9-pK_NsxehcjvoHSVzeHT7OmmmCdgppis"

        self.qdrant = Qdrant(
            host,
            api,
            self.model_1024,
            self.model_768,
            self.model_512,
            self.model_late_interaction,
            self.collection_name,
            pre_processing
        )

        # uri = os.getenv("URI_NEO")
        # user = os.getenv("USER")
        # password = os.getenv("PASSWORD")

        uri = "neo4j+s://4e1a09c4.databases.neo4j.io"
        user = "neo4j"
        password = "0hEim02sJ0LOqIArIDcQ0StvSntXIMc2qZyaDVAM37k"

        self.neo = Neo4j(uri, user, password)

        print('Initialize Chat success')

    def answer_by_context(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.answer_by_context()
        )
        formatted_prompt = prompt_template.format(question=self.question)

        return self.gemini_agent.generator(formatted_prompt)

    def answer_s2s(self):
        self.references_final = ""
        self.extract = ""
        self.feedback = ""
        self.answer_final = ""

        print(f'question: {self.question}')
        for t in range(self.t):
            print(f"Step {t}, initial feedback: {self.feedback}")
            self.references_final = ""

            self.extract = self.agent()
            print(f'extract: {self.extract}')

            for attr in self.extract:
                action = self.extract[attr]
                print(f'attr: {attr}')
                print(f'action: {action}')
                references = self.retrieval_bank(action)
                print(f"Available references: {references}")
                self.references_final += str(references)

            self.answer_final += f"Step {t}: {self.generator()}"
            print(f"Answer: {self.answer_final}")
            validator = self.valid()
            print(f"valid: {validator}")

            if "yes" in validator:
                return self.summary_answer()

            self.feedback = self.commentor()

        return self.summary_answer()

    def summary_answer(self):
        prompt_template = PromptTemplate(
            input_variables=["question", 'answer'],
            template=prompt.summary_answer()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=self.answer_final)
        return self.gemini_agent.generator(formatted_prompt)

    def separate_question(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.separate_question()
        )
        formatted_prompt = prompt_template.format(question=self.question)
        answer = self.gemini_agent.generator(formatted_prompt)
        answer_json = pre_processing.string_to_json(answer)
        return answer_json

    def agent(self):
        agent = self.first_decision() if not self.feedback else self.reflection()
        return pre_processing.string_to_json(agent)

    def retrieval_bank(self, action):
        return self.retrieval_graph() if 'graph' in action else self.retrieval_text()

    def retrieval_graph(self):
        # llm dự đoán câu hỏi thuộc phần nào để thu hẹp nội dung cần truy xuất
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.predict_question_belong_to()
        )
        formatted_prompt = prompt_template.format(question=self.question)
        query = self.gemini_agent.generator(formatted_prompt)
        query = query.replace("```", "").replace("cypher", "")
        print('query:', query)
        nodes, edges = self.neo.fetch_subgraph(query)

        # Tạo mapping node_id_to_idx trước
        node_id_list = list(nodes.keys())
        node_id_to_idx = {nid: i for i, nid in enumerate(node_id_list)}

        # Xác định thiết bị (GPU nếu có, ngược lại CPU)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Tạo edge_index và chuyển lên device
        edge_index = torch.tensor([
            [node_id_to_idx[edge["source"]] for edge in edges],
            [node_id_to_idx[edge["target"]] for edge in edges]
        ], dtype=torch.long).to(device)

        texts = [" ".join([f"{key} {value}" for key, value in dict(nodes[nid].items())['properties'].items()]) for nid
                 in node_id_list]

        x = self.neo.encode(texts)

        # Chuyển x lên cùng device
        if isinstance(x, torch.Tensor):
            x = x.to(device)
        else:
            x = torch.tensor(x).to(device)

        data = Data(x=x, edge_index=edge_index)

        # Chuyển model lên device
        model = GCN(input_dim=x.shape[1], hidden_dim=x.shape[1], output_dim=x.shape[1]).to(device)

        output = model(data)  # output: [num_nodes, 16]
        results = self.neo.retrieve_similar_nodes(self.question, output, texts, math.ceil(x.shape[0] * 0.5))

        return results

    def retrieval_text(self):
        documents = self.qdrant.query_from_db(self.question)

        try:
            re_ranking_query_text = self.qdrant.re_ranking(self.question, documents)

            reference = ""
            for i in range(len(re_ranking_query_text)):
                logit = re_ranking_query_text[i].metadata['relevance_score']
                text = re_ranking_query_text[i].page_content
                if logit > 0:
                    reference += f'{text}\n'

            return reference
        except:
            return documents

    def first_decision(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.first_decision_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question)

        return self.gemini_agent.generator(formatted_prompt).lower()

    def reflection(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "feedback", "answer"],
            template=prompt.reflection_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, feedback=self.feedback,
                                                  answer=self.answer_final)

        return self.gemini_agent.generator(formatted_prompt).lower()

    def generator(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "references"],
            template=prompt.generator_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, references=self.references_final)
        return self.gemini_generator.generator(formatted_prompt)

    def valid(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "answer"],
            template=prompt.valid_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=self.answer_final)
        return self.gemini_valid.generator(formatted_prompt).lower()

    def commentor(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "entities", "references"],
            template=prompt.commentor_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, entities=self.extract,
                                                  references=self.references_final)
        return self.gemini_commentor.generator(formatted_prompt)

    @staticmethod
    def _get_env():
        return (
            # os.getenv("MODEL_EMBEDDING_512"),
            "sentence-transformers/distiluse-base-multilingual-cased-v2",
            # os.getenv("MODEL_EMBEDDING_768"),
            "Alibaba-NLP/gte-multilingual-base",
            # os.getenv("MODEL_EMBEDDING_1024"),
            "intfloat/multilingual-e5-large-instruct",
            # os.getenv("MODEL_LATE_INTERACTION"),
            "colbert-ir/colbertv2.0",
            # os.getenv("NAME_COLLECTION")
            "Số tay sinh viên"
        )

    def _initialize_embedding_models(self):
        """Initialize all embedding models and their components"""
        # Get environment variables
        (self.model_embedding_512_name,
         self.model_embedding_768_name,
         self.model_embedding_1024_name,
         self.model_late_interaction_name,
         self.collection_name) = self._get_env()

        # Create embedding models using factory
        factory = EmbeddingFactory()
        self.model_512 = factory.create_embed_model(self.model_embedding_512_name)
        self.model_768 = factory.create_embed_model(self.model_embedding_768_name)
        self.model_1024 = factory.create_embed_model(self.model_embedding_1024_name)
        self.model_late_interaction = factory.create_embed_model(self.model_late_interaction_name)

    def set_question(self, question):
        self.question = question





