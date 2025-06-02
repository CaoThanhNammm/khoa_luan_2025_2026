from Chat import Chat
from LLM.Gemini import Gemini
import os
from dotenv import load_dotenv
load_dotenv()
from PreProcessing.PreProcessing import PreProcessing
import pandas as pd
import time

if __name__ == "__main__":
    qa = pd.read_csv(r'D:\PycharmProjects\pythonProject\eva_hybrid_question\qa_human_hybrid.csv')
    # 1. khởi tạo gemini và chat
    model_name_15_flash = os.getenv('MODEL_15_FLASH')
    model_name_20_flash = os.getenv('MODEL_20_FLASH')
    model_name_25_flash = os.getenv('MODEL_25_FLASH')

    api_key_agent = os.getenv('API_KEY_AGENT')
    api_key_generator = os.getenv('API_KEY_GENERATOR')
    api_key_valid = os.getenv('API_KEY_VALID')
    api_key_commentor = os.getenv('API_KEY_COMMENTOR')

    pre_processing = PreProcessing()
    t = 5

    gemini_agent = Gemini(model_name_15_flash, api_key_agent)
    gemini_generator = Gemini(model_name_20_flash, api_key_generator)
    gemini_valid = Gemini(model_name_15_flash, api_key_valid)
    gemini_commentor = Gemini(model_name_20_flash, api_key_commentor)

    chat = Chat(t, gemini_agent, gemini_generator, gemini_valid, gemini_commentor, pre_processing)

    my_qa = pd.DataFrame(columns=['question', 'answer'])
    file_name = 'my_qa_human_hybrid_updated_01.csv'

    for index, row in qa[30:].iterrows():
        q = row['question']

        time.sleep(60)

        try:
            answer = chat.answer_s2s(q)
            new_row = pd.DataFrame({
                'question': [q],
                'answer': [answer]
            })
            my_qa = pd.concat([my_qa, new_row], ignore_index=True)
            if len(my_qa) % 2 == 0:
                my_qa.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
                print(my_qa)
        except:
            gemini_agent = Gemini(model_name_15_flash, api_key_agent)
            gemini_generator = Gemini(model_name_20_flash, api_key_generator)
            gemini_valid = Gemini(model_name_15_flash, api_key_valid)
            gemini_commentor = Gemini(model_name_15_flash, api_key_commentor)
            chat = Chat(t, gemini_agent, gemini_generator, gemini_valid, gemini_commentor, pre_processing)
            time.sleep(60)

            answer = chat.answer_s2s(q)
            new_row = pd.DataFrame({
                'question': [q],
                'answer': [answer]
            })
            my_qa = pd.concat([my_qa, new_row], ignore_index=True)
            if len(my_qa) % 2 == 0:
                my_qa.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
                print(my_qa)


    my_qa.to_csv(fr"C:\Users\Nam\Desktop\my_qa_human_hybrid_updated_final", encoding='utf-8-sig')




    # 3. trả lời
    # prompt_template = PromptTemplate(
    #     input_variables=["question"],
    #     template=prompt.criteria_complete_question()
    # )
    # formatted_prompt = prompt_template.format(question=question)
    # criteria = gemini.generator(formatted_prompt)
    # criteria = pre_processing.string_to_json(criteria)
    # result = ""
    # for c in criteria['criteria']:
    #     result += f'{c}: {chat.answer(c)} \n'
    # result = re.sub(r'\s+', ' ', result).strip()
    # prompt_template = PromptTemplate(
    #     input_variables=["question", "answer"],
    #     template=prompt.summary_answer()
    # )
    # formatted_prompt = prompt_template.format(question=question, answer=result)
    # answer = gemini.generator(formatted_prompt)



    # print(chat.retrieval_graph(question))
    # print('---------------------------------------')
    # print(chat.retrieval_text(question))
    # """
    #     1. nhận 1 câu hỏi q, khởi tạo f0
    #     2. đưa vào llm với prompt first decision => return vector or graph at
    #     3. if(vector):
    #             truy xuat vao vector
    #         if(graph):
    #             truy xuat vao graph
    #         return ve 1 cau tra loi Xt
    #     4. đưa câu hỏi q và cau tra loi Xt vào llm với prompt generator => return về câu trả lời y^
    #     5. đưa câu hỏi q, câu trả lời y^, Xt vào llm với prompt validator nếu True => return câu trả lời y^
    #     Nếu không tới B6
    #     6. đưa câu hỏi q và hành động at vào llm với prompt commentor => return về ft, gán f0 thành ft
    # """


    # # câu hỏi q, csdl D, số lần lặp T
    # # khởi tạo phản hồi ban đầu
    # f0 = ""
    # # số lần lặp
    # t = 10
    # for i in t:
    #     # xác định hành dộng dựa trên câu hỏi và hành động trước đó
    #     at = Agent(q, f(t-1))
    #     Xt = retrievalbank(q, at, D)
    #     y mu t = generator(q, Xt)
    #     if Cval(q, y mu t, Xt):
    #         return y mu t
    #     else:
    #         f0 = Ccom(q, at)




