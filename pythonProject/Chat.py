from sentence_transformers import CrossEncoder
from LLM import prompt
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
        host = os.getenv('HOST_QDRANT')
        api = os.getenv("API_KEY_QDRANT")

        self.qdrant = Qdrant(
            host,
            api,
            self.model_1024,
            self.model_768,
            self.model_512,
            self.model_late_interaction,
            self.collection_name
        )

        uri = os.getenv("URI_NEO")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        self.neo = Neo4j(uri, user, password)
        self.pre_processing = pre_processing
        self.reranker_model = CrossEncoder('DiTy/cross-encoder-russian-msmarco', max_length=512)


    def answer(self, question):
        # sử dụng ngữ cảnh của các câu trả lời trước đó để trả lời
        # first_answer = self.answer_by_context(question)
        # validator = self.valid(question, first_answer)
        # print(f"valid: {validator}")
        # if "yes" in validator:
        #     print(f"Final answer: {first_answer}")
        #     return first_answer

        # nếu không có câu trả thì mới truy xuất
        feedback = ""
        # new_question_pre_processing = self.pre_processing.text_preprocessing_vietnamese(question.strip())

        for i in range(self.t):
            print(f"Step {i}, initial feedback: {feedback}")

            entities, relationship, action = self.agent(question, feedback)
            print(f"Action: {action}")
            print(f'entities {entities}')
            print(f'relationship {relationship}')
            if len(relationship) != 0:
                new_question = self.join_relations(relationship)
            else:
                new_question = question

            print(f'New question: {new_question}')
            new_question_pre_processing = self.pre_processing.text_preprocessing_vietnamese(new_question.strip())

            references = self.retrieval_bank(new_question_pre_processing, action)
            print(f"Available references: {references}")

            potential_answer = self.generator(question, references)
            print(f"Answer: {potential_answer}")

            validator = self.valid(question, potential_answer)
            print(f"valid: {validator}")

            if "yes" in validator:
                return potential_answer

            feedback = self.commentor(question, entities, relationship, action, references)
            print("-" * 2000)

        return "không có thông tin"


    def answer_grag(self, question):
        references = self.retrieval_graph(question)

        potential_answer = self.generator(question, references)
        print(f"Answer: {potential_answer}")
        print("-" * 2000)

        return potential_answer

    def answer_by_context(self, question):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.answer_by_context()
        )
        formatted_prompt = prompt_template.format(question=question)

        return self.gemini_agent.generator(formatted_prompt)

    def answer_s2s(self, question):
        separate_question = self.separate_question(question)
        answer_final = ''
        for attr in separate_question:
            question_child = separate_question[attr]
            print(f'question child: {question_child}')
            answer_child = self.answer(question_child)
            answer_final += f'{question_child}: {answer_child}'


        return self.summary_answer(question, answer_final)

    def answer_parent(self, question):
        # Tách câu hỏi thành các câu hỏi con
        separate_question = self.separate_question(question)
        answer_child_list = []

        # Hàm phụ để gọi answer_child với một câu hỏi con
        def process_child_question(attr_question_pair):
            attr, question_child = attr_question_pair
            print(f'question_child: {question_child}')
            answer = self.answer(question_child)
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
        print(f'question {question}')
        agent = self.first_decision(question) if not feedback else self.reflection(question, feedback)
        agent = pre_processing.string_to_json(agent)

        entities_relationship = agent['extracted']

        action = agent['retriever']
        relationship = entities_relationship['relations']
        entities = entities_relationship['entities']

        return entities, relationship, action.lower()

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

        scores = self.reranker_model.rank(question, documents)
        res = []
        for item in scores:
            corpus_id = item['corpus_id']
            score = item['score']
            name = documents[corpus_id] if corpus_id < len(documents) else "Không tìm thấy tài liệu"
            res.append(f"score: {score}, name: {name}")

        return res


    def retrieval_text(self, question):
        embeddings = self.embed_question(question)
        documents = self.qdrant.query_from_db(*embeddings)
        print(f'documents {documents}')
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


    def embed_question(self, question):
        return (
            self.model_512.embed(question),
            self.model_768.embed(question),
            self.model_1024.embed(question),
            self.model_late_interaction.embed(question)
        )

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
            template=prompt.reflection_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, feedback=feedback)

        return self.gemini_agent.generator(formatted_prompt).lower()

    def generator(self, question, references):
        prompt_template = PromptTemplate(
            input_variables=["question", "references"],
            template=prompt.generator_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, references=references)

        return self.gemini_generator.generator(formatted_prompt)

    def valid(self, question, answer):
        prompt_template = PromptTemplate(
            input_variables=["question", "answer"],
            template=prompt.valid_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, answer=answer)

        return self.gemini_valid.generator(formatted_prompt).lower()

    def commentor(self, question, entities, relationship, action, references):
        prompt_template = PromptTemplate(
            input_variables=["question", "entities", "relationship", "action", "references"],
            template=prompt.commentor_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, entities=entities, relationship=relationship, action=action, references=references)

        return self.gemini_commentor.generator(formatted_prompt)


    @staticmethod
    def _get_env():
        return (
            os.getenv("MODEL_EMBEDDING_512"),
            os.getenv("MODEL_EMBEDDING_768"),
            os.getenv("MODEL_EMBEDDING_1024"),
            os.getenv("MODEL_LATE_INTERACTION"),
            os.getenv("NAME_COLLECTION")
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


    def join_relations(self, relations):
        if not relations:
            return ""

        # Bắt đầu với source của quan hệ đầu tiên
        result = [relations[0]["source"]]

        # Duyệt qua từng quan hệ để thêm relation và target
        for rel in relations:
            result.append(rel["relation"])
            result.append(rel["target"])

        # Nối các thành phần thành chuỗi, loại bỏ các phần tử rỗng
        return " ".join(item for item in result if item)





