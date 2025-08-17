import re

from markdown_it.common.entities import entities

from LLM.Cohere import CohereChatBot
from LLM.GPT import GPT
from LLM.Gemini import Gemini
import LLM.prompt as prompt
from LLM.Llama import Llama
from dotenv import load_dotenv
from knowledge_graph.create_entities_relationship_kb import pre_processing

load_dotenv()
import json
import os
import torch
from langchain_core.prompts import PromptTemplate


class Chat:
    def __init__(self, t, qdrant, neo4j, pre_processing, document_id):
        self.t = t
        self.question = ''
        self.pre_processing = pre_processing
        self.references_final = ""
        self.extract = ""
        self.feedback = ""
        self.answer_final = ""
        self.entities = []
        self.relations = []
        self.document_id = document_id

        # 1. khởi tạo gemini và chat
        model_name_15_flash = os.getenv('MODEL_15_FLASH')
        model_name_20_flash = os.getenv('MODEL_20_FLASH')
        model_name_25_flash = os.getenv('MODEL_25_FLASH')

        api_key_agent = os.getenv('API_KEY_AGENT')
        api_key_generator = os.getenv('API_KEY_GENERATOR')
        api_key_valid = os.getenv('API_KEY_VALID')
        api_key_commentor = os.getenv('API_KEY_COMMENTOR')


        self.gemini_agent = Gemini(model_name_25_flash, api_key_agent)
        self.gemini_generator = Gemini(model_name_20_flash, api_key_generator)
        self.gemini_valid = Gemini(model_name_15_flash, api_key_valid)
        self.gemini_commentor = Gemini(model_name_15_flash, api_key_commentor)

        self.qdrant = qdrant
        self.neo = neo4j

        api_key_01 = os.getenv("API_KEY_NVIDIA_01")
        api_key_02 = os.getenv("API_KEY_NVIDIA_02")
        api_key_03 = os.getenv("API_KEY_NVIDIA_03")
        api_key_04 = os.getenv("API_KEY_NVIDIA_04")

        model_llama_405b = os.getenv("MODEL_LLAMA_405B")

        self.llama3_1_commentor = Llama(api_key_01, model_llama_405b)
        self.llama3_1_generator = Llama(api_key_02, model_llama_405b)
        self.llama3_1_graph = Llama(api_key_03, model_llama_405b)
        self.llama3_1_summary = Llama(api_key_04, model_llama_405b)

        self.cohere_agent = CohereChatBot()
        self.cohere_generator = CohereChatBot()
        self.cohere_valid = CohereChatBot()
        self.cohere_commentor = CohereChatBot()


        self.gpt_agent = GPT("gpt-5-mini")
        self.gpt_generator = GPT("gpt-5-nano")
        self.gpt_valid = GPT("gpt-5-nano")
        self.gpt_commentor = GPT("gpt-5-mini")
        self.gpt_summary = GPT("gpt-5-nano")
        self.gpt_graph = GPT("gpt-5-nano")

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

    def answer_s2s_stsv(self):
        self.document_id = 'so_tay_sinh_vien_2024'
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
                references = self.retrieval_bank_stsv(action)
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

    def answer_prime(self):
        self.extract = ""
        self.answer_final = ""
        self.feedback = ""
        self.references_final = ""

        print(f'question: {self.question}')
        for t in range(self.t):
            print(f"Step {t}, initial feedback: {self.feedback}")
            self.references_final = ""

            relationship, action = self.agent_prime()  # knowledge graph or text documents

            print(f'Relationship: {relationship}')
            print(f'Action: {action}')

            self.references_final = self.retrieval_bank_prime(action, relationship)

            self.answer_final = f"{self.generator_prime()}"
            print(f"Answer: {self.answer_final}")

            validator = self.valid_prime()
            print(f"valid: {validator}")

            if "yes" in validator:
                self.entities.clear()
                self.relations.clear()
                return self.summary_answer_prime()

            self.feedback = self.commentor_prime()
            self.entities.clear()
            self.relations.clear()

        return self.summary_answer_prime()

    def answer_mag(self):
        self.extract = ""
        self.answer_final = ""
        self.feedback = ""
        self.references_final = ""

        print(f'question: {self.question}')
        for t in range(self.t):
            print(f"Step {t}, initial feedback: {self.feedback}")
            self.references_final = ""

            relationship, action = self.agent_mag()  # knowledge graph or text documents

            print(f'Relationship: {relationship}')
            print(f'Action: {action}')

            self.references_final = self.retrieval_bank_mag(action, relationship)

            self.answer_final = f"{self.generator_prime()}"
            print(f"Answer: {self.answer_final}")

            validator = self.valid_prime()
            print(f"valid: {validator}")

            if "yes" in validator:
                self.entities.clear()
                self.relations.clear()
                return self.summary_answer_prime()

            self.feedback = self.commentor_prime()
            self.entities.clear()
            self.relations.clear()

        return self.summary_answer_prime()

    def agent_prime(self):
        agent = self.first_decision_prime() if not self.feedback else self.reflection_prime()
        print(f"Agent: {agent}")
        agent = pre_processing.string_to_json(agent)


        return agent["relationship"], agent["action"]

    def agent_mag(self):
        agent = self.first_decision_mag() if not self.feedback else self.reflection_prime()
        print(f"Agent: {agent}")
        agent = pre_processing.string_to_json(agent)


        return agent["relationship"], agent["action"]

    def first_decision_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.first_decision_prime()
        )

        formatted_prompt = prompt_template.format(question=self.question)
        # return self.gemini_agent.generator(formatted_prompt).lower()
        # self.llama3_1_graph.set_prompt(formatted_prompt)
        # return self.llama3_1_graph.generator().lower()
        return self.cohere_agent.chat(formatted_prompt).lower()

    def first_decision_mag(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.first_decision_mag()
        )

        formatted_prompt = prompt_template.format(question=self.question)
        return self.cohere_agent.chat(formatted_prompt).lower()

    def reflection_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "feedback"],
            template=prompt.self_reflection_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, feedback=self.feedback)
        return self.cohere_agent.chat(formatted_prompt).lower()

    def summary_answer(self):
        prompt_template = PromptTemplate(
            input_variables=["question", 'answer'],
            template=prompt.summary_answer()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=self.answer_final)
        return self.gpt_summary.ask(formatted_prompt)

    def summary_answer_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", 'answer'],
            template=prompt.summary_answer_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=self.answer_final)
        return self.gpt_summary.ask(formatted_prompt)

    def agent(self):
        agent = self.first_decision() if not self.feedback else self.reflection()
        return pre_processing.string_to_json(agent)

    def retrieval_bank_stsv(self, action):
        return self.retrieval_graph_stsv() if 'graph' in action else self.retrieval_text()

    def retrieval_bank(self, action):
        return self.retrieval_graph() if 'graph' in action else self.retrieval_text()

    def retrieval_bank_prime(self, action, relationship):
        return self.retrieval_graph_prime(relationship) if 'knowledge graph' in action else self.retrieval_text_prime(relationship)

    def retrieval_bank_mag(self, action, relationship):
        return self.retrieval_graph_prime(relationship)

    def retrieval_graph_prime(self, relationship):
        res = ""
        for relation in relationship:
            head_type = relation["head_type"]
            head_name = str(relation["head"]).replace("'", "").replace('"', "")

            query = f"""
            MATCH p=(a)-[r]-(b)
            WHERE a.name CONTAINS '{head_name}'
            RETURN p
            LIMIT 20
            """.strip()

            print('query:', query)
            e, r, triplets = self.neo.run_cypher(query)

            self.entities.extend(e)
            self.relations.extend(r)
            res += str(triplets)

        return res

    def retrieval_graph(self):
        # llm dự đoán câu hỏi thuộc phần nào để thu hẹp nội dung cần truy xuất
        prompt_template = PromptTemplate(
            input_variables=["question", "document_id", "parts_of_document"],
            template=prompt.predict_question_belong_to()
        )
        formatted_prompt = prompt_template.format(question=self.question, document_id=self.document_id,
                                                  parts_of_document=self.neo.get_part_of_document(self.document_id))
        res = self.gpt_graph.ask(formatted_prompt)
        res = self.pre_processing.string_to_json(res)

        query = f"""
        MATCH (document:Document {{name: '{self.document_id}'}})-[*]->(predict:Document {{name: '{res['name']}'}})
        MATCH p=(predict)-[r*1..{res['level']}]->(e)
        RETURN p
        """
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
        return texts

    def retrieval_graph_stsv(self):
        # llm dự đoán câu hỏi thuộc phần nào để thu hẹp nội dung cần truy xuất
        prompt_template = PromptTemplate(
            input_variables=["question", "document_id"],
            template=prompt.predict_question_belong_to_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, document_id=self.document_id)
        res = self.gpt_graph.ask(formatted_prompt)
        res = self.pre_processing.string_to_json(res)

        query = f"""
        MATCH (document:Document {{name: '{self.document_id}'}})-[*]->(predict:{res["part"]} {{name: '{res['name']}'}})
        MATCH p=(predict)-[r*1..{res['level']}]->(e)
        RETURN p
        """
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

        # x = self.neo.encode(texts)
        #
        # # Chuyển x lên cùng device
        # if isinstance(x, torch.Tensor):
        #     x = x.to(device)
        # else:
        #     x = torch.tensor(x).to(device)
        #
        # data = Data(x=x, edge_index=edge_index)
        #
        # # Chuyển model lên device
        # model = GCN(input_dim=x.shape[1], hidden_dim=x.shape[1], output_dim=x.shape[1]).to(device)
        #
        # output = model(data)  # output: [num_nodes, 16]
        # results = self.neo.retrieve_similar_nodes(self.question, output, texts, math.ceil(x.shape[0] * 0.5))
        # texts = ''
        # for res in results:
        #     texts += res + " "
        return texts

    def retrieval_text(self):
        self.qdrant.set_collection_name(self.document_id)
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

    def retrieval_text_prime(self, relationship):
        self.qdrant.set_collection_name(self.document_id)
        entities_topic  = ""
        for relation in relationship:
            entities_topic += relation["head"]

        documents = self.qdrant.query_from_db_prime(entities_topic)

        try:
            re_ranking_query_text = self.qdrant.re_ranking(entities_topic, documents)
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
        return self.gpt_agent.ask(formatted_prompt).lower()

    def reflection(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "feedback", "answer"],
            template=prompt.reflection_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, feedback=self.feedback,
                                                  answer=self.answer_final)
        return self.gpt_agent.ask(formatted_prompt).lower()

    def generator(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "references"],
            template=prompt.generator()
        )

        formatted_prompt = prompt_template.format(question=self.question, references=self.references_final)
        return self.gpt_generator.ask(formatted_prompt)


    def generator_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "document"],
            template=prompt.generator_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, document=self.references_final)
        return self.gpt_generator.ask(formatted_prompt)

    def valid(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "answer"],
            template=prompt.valid_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=self.answer_final)

        # return self.gemini_valid.generator(formatted_prompt).lower()
        return self.gpt_valid.ask(formatted_prompt).lower()

    def valid_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "document", "answer"],
            template=prompt.validator_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, document=self.references_final, answer=self.answer_final)
        return self.gpt_valid.ask(formatted_prompt).lower()

    def commentor(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "entities", "references"],
            template=prompt.commentor_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, entities=self.extract,
                                                  references=self.references_final)
        # return self.gemini_commentor.generator(formatted_prompt)
        return self.gpt_commentor.ask(formatted_prompt)

    def commentor_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "entities", "relations"],
            template=prompt.commentor_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, entities=self.entities,
                                                  relations=self.relations)

        # return self.gemini_commentor.generator(formatted_prompt)
        # self.llama3_1_commentor.set_prompt(formatted_prompt)
        # return self.llama3_1_commentor.generator()
        # return self.cohere_commentor.chat(formatted_prompt)

        return self.gpt_commentor.ask(formatted_prompt)
    def set_question(self, question):
        self.question = question

    def set_document_id(self, document_id):
        self.document_id = document_id
