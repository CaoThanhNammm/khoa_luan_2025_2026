from sentence_transformers import CrossEncoder
from LLM import prompt
from LLM.prompt import commentor_stsv, generator_stsv, valid_stsv, reflection_stsv
from ModelLLM.EmbeddingFactory import EmbeddingFactory
from VectorDatabase.Qdrant import Qdrant
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from knowledge_graph.create_entities_relationship_kb import pre_processing
load_dotenv()
import os
from knowledge_graph.KnowledgeGraphDatabase import Neo4j
import numpy as np
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate


class Chat:
    def __init__(self, t, gemini_agent, gemini_generator, gemini_valid, gemini_commentor, pre_processing):
        self.gemini_agent = gemini_agent
        self.gemini_generator = gemini_generator
        self.gemini_valid = gemini_valid
        self.gemini_commentor = gemini_commentor
        self.t = t

        self._initialize_embedding_models()
        # host = user_secrets.get_secret('HOST_QDRANT')
        # api = user_secrets.get_secret("API_KEY_QDRANT")
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

        # uri = user_secrets.get_secret("URI_NEO")
        # user = user_secrets.get_secret("USER")
        # password = user_secrets.get_secret("PASSWORD")

        uri = "neo4j+s://4e1a09c4.databases.neo4j.io"
        user = "neo4j"
        password = "0hEim02sJ0LOqIArIDcQ0StvSntXIMc2qZyaDVAM37k"

        self.neo = Neo4j(uri, user, password)
        self.pre_processing = pre_processing
        print('Initialize Chat success')

    def answer_by_context(self, question):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.answer_by_context()
        )
        formatted_prompt = prompt_template.format(question=question)

        return self.gemini_agent.generator(formatted_prompt)

    def answer_s2s(self, question):
        feedback = ''
        answer_final = ''
        print(f'question: {question}')
        for t in range(self.t):
            print(f"Step {t}, initial feedback: {feedback}")
            references_final = ''

            agent = self.agent(question, feedback)
            print(f'agent: {agent}')

            for attr in agent:
                action = agent[attr]
                print(f'attr: {attr}')
                print(f'action: {action}')
                references = self.retrieval_bank(attr, action)
                print(f"Available references: {references}")
                references_final += str(references)

            answer_final = self.generator(question, references_final)
            print(f"Answer: {answer_final}")
            validator = self.valid(question, answer_final)
            print(f"valid: {validator}")

            if "yes" in validator:
                return answer_final

            feedback = self.commentor(question, str(agent), references_final)

        return self.summary_answer(question, answer_final)

    def answer_parent(self, question):
        # Tách câu hỏi thành các câu hỏi con
        separate_question = self.separate_question(question)
        answer_child_list = []

        # Hàm phụ để gọi answer_child với một câu hỏi con
        def process_child_question(attr_question_pair):
            attr, question_child = attr_question_pair
            print(f'question_child: {question_child}')
            answer = self.answer_s2s(question_child)
            return (attr, f"{question}: {answer}")

        # Chạy song song các câu hỏi con
        with ThreadPoolExecutor() as executor:
            # Tạo danh sách các cặp (attr, question_child)
            question_pairs = [(attr, separate_question[attr]) for attr in separate_question]
            # Gửi các câu hỏi con để xử lý song song
            results = executor.map(process_child_question, question_pairs)
            # Thu thập kết quả
            answer_child_list = list(results)

        # Sắp xếp kết quả theo attr để đảm bảo thứ tự (nếu cần)
        answer_child_list.sort(key=lambda x: x[0])  # Sắp xếp theo attr
        # Tổng hợp các câu trả lời con thành chuỗi
        answer_child = "\n".join(result[1] for result in answer_child_list)

        # Tổng hợp câu trả lời cuối cùng
        return self.summary_answer(question, answer_child)

    def summary_answer(self, question, answer):
        prompt_template = PromptTemplate(
            input_variables=["question", 'answer'],
            template=prompt.summary_answer()
        )
        formatted_prompt = prompt_template.format(question=question, answer=answer)
        return self.gemini_agent.generator(formatted_prompt)

    def separate_question(self, question):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.separate_question()
        )
        formatted_prompt = prompt_template.format(question=question)
        answer = self.gemini_agent.generator(formatted_prompt)
        answer_json = pre_processing.string_to_json(answer)
        return answer_json

    def agent(self, question, feedback):
        agent = self.first_decision(question) if not feedback else self.reflection(question, feedback)
        return pre_processing.string_to_json(agent)

    def retrieval_bank(self, question, action):
        return self.retrieval_graph(question) if 'graph' in action else self.retrieval_text(question)

    def retrieval_graph(self, question):
        # llm dự đoán câu hỏi thuộc phần nào để thu hẹp nội dung cần truy xuất
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.predict_question_belong_to()
        )
        formatted_prompt = prompt_template.format(question=question)
        query = self.gemini_agent.generator(formatted_prompt)
        query = query.replace("```", "").replace("cypher", "")
        print('query:', query)
        path = self.neo.get_path(query)

        documents = self.neo.create_documents(path)

        # scores = self.neo.re_ranking(question, documents)

        # res = []
        # for item in scores:
        #     corpus_id = item['corpus_id']
        #     score = item['score']

        #     name = documents[corpus_id] if corpus_id < len(documents) else "Không tìm thấy tài liệu"
        #     if score > 0.5:
        #         res.append(f"score: {score}, name: {name}")

        return documents

    def retrieval_text(self, question):
        documents = self.qdrant.query_from_db(question)

        try:
            re_ranking_query_text = self.qdrant.re_ranking(question, documents)

            reference = ""
            for i in range(len(re_ranking_query_text)):
                logit = re_ranking_query_text[i].metadata['relevance_score']
                text = re_ranking_query_text[i].page_content
                if logit > 0:
                    reference += f'{text}\n'

            return reference
        except:
            return documents

    def first_decision(self, question):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.first_decision_stsv()
        )
        formatted_prompt = prompt_template.format(question=question)

        return self.gemini_agent.generator(formatted_prompt).lower()

    def reflection(self, question, feedback):
        prompt_template = PromptTemplate(
            input_variables=["question", "feedback"],
            template=reflection_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, feedback=feedback)

        return self.gemini_agent.generator(formatted_prompt).lower()

    def generator(self, question, references):
        prompt_template = PromptTemplate(
            input_variables=["question", "references"],
            template=generator_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, references=references)
        return self.gemini_generator.generator(formatted_prompt)

    def valid(self, question, answer):
        prompt_template = PromptTemplate(
            input_variables=["question", "answer"],
            template=valid_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, answer=answer)
        return self.gemini_valid.generator(formatted_prompt).lower()

    def commentor(self, question, entities, references):
        prompt_template = PromptTemplate(
            input_variables=["question", "entities", "references"],
            template=commentor_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, entities=entities, references=references)
        return self.gemini_commentor.generator(formatted_prompt)

    @staticmethod
    def _get_env():
        return (
            # user_secrets.get_secret("MODEL_EMBEDDING_512"),
            "sentence-transformers/distiluse-base-multilingual-cased-v2",
            # user_secrets.get_secret("MODEL_EMBEDDING_768"),
            "Alibaba-NLP/gte-multilingual-base",
            # user_secrets.get_secret("MODEL_EMBEDDING_1024"),
            "intfloat/multilingual-e5-large-instruct",
            # user_secrets.get_secret("MODEL_LATE_INTERACTION"),
            "colbert-ir/colbertv2.0",
            # user_secrets.get_secret("NAME_COLLECTION")
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





