from LLM import prompt
from ModelLLM.EmbeddingFactory import EmbeddingFactory
from VectorDatabase.Qdrant import Qdrant
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import PromptTemplate
import os
from knowledge_graph.KnowledgeGraphDatabase import Neo4j


class Chat:
    def __init__(self, t, gemini, pre_processing):
        self.gemini = gemini
        self.t = t

        self._initialize_embedding_models()

        self.qdrant = Qdrant(
            "localhost",
            6333,
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

    def answer(self, question):
        question_pre_processing = self.pre_processing.text_preprocessing_vietnamese(question.strip())
        feedback = ""
        potential_answer = ""
        print(f"Question nhỏ: {question}")
        for i in range(self.t):
            print(f"Step {i}, initial feedback: {feedback}")

            action = self.agent(question, feedback)
            print(f"Action: {action}")

            references = self.retrieval_bank(question_pre_processing, action)
            print(f"Available references: {references}")

            potential_answer = self.generator(question_pre_processing, references)
            print(f"Answer: {potential_answer}")

            validator = self.valid(question, potential_answer)
            print(f"valid: {validator}")
            if "yes" in validator:
                print(f"Final answer: {potential_answer}")
                return potential_answer

            feedback = self.commentor(question, potential_answer, references, action)
            print(f"Continuing feedback: {feedback}")
            print("-" * 2000)
        return potential_answer

    def agent(self, question, feedback):
        return self.first_decision(question) if not feedback else self.reflection(question, feedback)

    def retrieval_bank(self, question, action):
        return self.retrieval_graph(question) if 'graph' in action else self.retrieval_text(question)

    def retrieval_graph(self, question):
        # llm dự đoán câu hỏi thuộc phần nào để thu hẹp nội dung cần truy xuất
        query = self.gemini.generator(prompt.predict_question_belong_to(question))
        query = query.replace("```", "").replace("cypher", "")

        print('query:', query)
        path = self.neo.get_path(query)
        references_node = self.neo.get_relationship(path)

        results = ""
        for r in references_node:
            results += r + '\n'

        return results

    def retrieval_text(self, question):
        embeddings = self.embed_question(question)
        results = self.qdrant.query_from_db(*embeddings)
        json_query_text = []
        for result in results:
            json_query_text.append(result.payload["text"])

        re_ranking_query_text = self.qdrant.re_ranking(question, json_query_text)
        reference = ""
        for i in range(len(re_ranking_query_text)):
            logit = re_ranking_query_text[i].metadata['relevance_score']
            text = re_ranking_query_text[i].page_content
            print(f"{logit}: {text}")
            reference += f'{text}\n'

        return reference

    def embed_question(self, question):
        return (
            self.model_512.embed(self.model_embed_512, None, question),
            self.model_768.embed(self.model_embed_768, self.tokenizer_768, question),
            self.model_1024.embed(self.model_embed_1024, self.tokenizer_1024, question),
            self.model_late_interaction.embed(self.model_embed_late_interaction, self.tokenizer_late_interaction,
                                              question)
        )

    def first_decision(self, question):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.first_decision_stsv()
        )
        formatted_prompt = prompt_template.format(question=question)

        return self.gemini.generator(formatted_prompt).lower()


    def reflection(self, question, feedback):
        prompt_template = PromptTemplate(
            input_variables=["question", "feedback"],
            template=prompt.reflection_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, feedback=feedback)

        return self.gemini.generator(formatted_prompt).lower()

    def generator(self, question, references):
        prompt_template = PromptTemplate(
            input_variables=["question", "references"],
            template=prompt.generator_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, references=references)

        return self.gemini.generator(formatted_prompt)

    def valid(self, question, answer):
        prompt_template = PromptTemplate(
            input_variables=["question", "answer"],
            template=prompt.valid_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, answer=answer)

        return self.gemini.generator(formatted_prompt).lower()

    def commentor(self, question, answer, references, current_module):
        prompt_template = PromptTemplate(
            input_variables=["question", "answer", "references", "current_module"],
            template=prompt.commentor_stsv()
        )
        formatted_prompt = prompt_template.format(question=question, answer=answer, references=references, current_module=current_module)

        return self.gemini.generator(formatted_prompt)

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

        # Load embedding models
        self.model_embed_512 = self.model_512.load_model()
        self.model_embed_768, self.tokenizer_768 = self.model_768.load_model()
        self.model_embed_1024, self.tokenizer_1024 = self.model_1024.load_model()
        self.model_embed_late_interaction, self.tokenizer_late_interaction = self.model_late_interaction.load_model()


    def set_gemini(self, gemini):
        self.gemini = gemini






