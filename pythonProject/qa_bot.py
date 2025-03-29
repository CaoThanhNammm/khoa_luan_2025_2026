from Chat import Chat
from LLM.Gemini import Gemini
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    # 1. khởi tạo gemini và chat
    model_name = os.getenv('MODEL')
    api_key = os.getenv('API_KEY')
    gemini = Gemini(model_name, api_key)
    t = 5
    chat = Chat(t, gemini)
    # 2. câu hỏi
    question = 'hãy cho tôi biết về thời gian các tiết học'
    # 3. trả lời
    chat.answer(question)

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