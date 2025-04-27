# import pandas as pd
# import asyncio
# import requests
# from typing import Dict
# import google.generativeai as genai
#
# # Cấu hình API key cho Gemini (thay YOUR_API_KEY bằng key thực tế của bạn)
# API_KEY = ""  # Thay bằng API key thực tế từ Google
# genai.configure(api_key=API_KEY)
#
#
# # Định nghĩa tool get_weather sử dụng API thực tế (ở đây tôi giả lập bằng cách gọi Gemini)
# def get_weather(city: str) -> Dict[str, str]:
#     """Lấy báo cáo thời tiết hiện tại cho một thành phố cụ thể bằng Gemini API.
#
#     Args:
#         city (str): Tên thành phố (ví dụ: "New York", "London", "Tokyo").
#
#     Returns:
#         dict: Từ điển chứa thông tin thời tiết.
#               Bao gồm key 'status' ('success' hoặc 'error').
#               Nếu 'success', có thêm key 'report' với chi tiết thời tiết.
#               Nếu 'error', có thêm key 'error_message'.
#     """
#     print(f"--- Tool: get_weather called for city: {city} ---")
#
#     # Tạo prompt gửi đến Gemini API
#     prompt = f"Provide the current weather report for {city}. Return the response in the format: 'The weather in {city} is [description] with a temperature of [temp]°C.' If no data is available, return an error message."
#
#     try:
#         # Gọi Gemini API
#         model = genai.GenerativeModel('gemini-1.5-pro')  # Dùng model Gemini 1.5 Pro, thay đổi nếu cần
#         response = model.generate_content(prompt)
#         weather_report = response.text.strip()
#
#         # Kiểm tra xem response có phải là lỗi không
#         if "error" in weather_report.lower() or "no data" in weather_report.lower():
#             return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}
#         return {"status": "success", "report": weather_report}
#
#     except Exception as e:
#         return {"status": "error", "error_message": f"Error fetching weather for '{city}': {str(e)}"}
#
#
# # Test tool
# print(get_weather("New York"))
# print(get_weather("Paris"))
#
#
# # Định nghĩa Agent
# class Agent:
#     def __init__(self, name: str, model: str, description: str, instruction: str, tools: list):
#         self.name = name
#         self.model = model
#         self.description = description
#         self.instruction = instruction
#         self.tools = tools
#
#     def process_query(self, query: str) -> str:
#         if "weather" in query.lower():
#             for tool in self.tools:
#                 # Tìm thành phố trong query
#                 cities = ["New York", "London", "Tokyo", "Paris"]  # Danh sách có thể mở rộng
#                 city = next((c for c in cities if c.lower() in query.lower()), None)
#                 if city:
#                     result = tool(city)
#                     if result["status"] == "success":
#                         return result["report"]
#                     return result["error_message"]
#         return "Please ask about the weather in a specific city."
#
#
# # Tạo weather agent
# weather_agent = Agent(
#     name="weather_agent_v1",
#     model="gemini-2.0-flash",  # Model Gemini thực tế
#     description="Provides weather information for specific cities using Gemini API.",
#     instruction="You are a helpful weather assistant.",
#     tools=[get_weather]
# )
# print(f"Agent '{weather_agent.name}' created using model '{weather_agent.model}'.")
#
#
# # Định nghĩa Runner
# class Runner:
#     def __init__(self, agent: Agent):
#         self.agent = agent
#
#     async def run_async(self, query: str):
#         response = self.agent.process_query(query)
#         yield response
#
#
# runner = Runner(agent=weather_agent)
# print(f"Runner created for agent '{runner.agent.name}'.")
#
#
# # Hàm gọi agent bất đồng bộ
# async def call_agent_async(query: str):
#     print(f"\n>>> User Query: {query}")
#     async for response in runner.run_async(query):
#         print(f"<<< Agent Response: {response}")
#         break
#
#
# # Chạy conversation
# async def run_conversation():
#     await call_agent_async("What is the weather like in London?")
#     await call_agent_async("How about Paris?")
#     await call_agent_async("Tell me the weather in New York")
#
# # Chạy chương trình
# asyncio.run(run_conversation())


import pandas as pd

from LLM.Gemini import Gemini

# try:
#     qa = pd.read_csv('qa_human.csv')
#     rows = list(qa.itertuples())[809:]
#     for row in rows:
#         print(row.question)
# except FileNotFoundError:
#     print("File 'qa.csv' không tồn tại, bỏ qua phần đọc file.")

# qa_human = pd.read_csv('qa_human.csv')
# my_qa_human = pd.read_csv(r"C:\Users\Nam\Desktop\my_qa_human.csv")
#
# loop_range = min(len(qa_human), len(my_qa_human))
#
# for i in range(loop_range):
#     if not my_qa_human.values[i][1] == qa_human.values[i][0]:
#         print(my_qa_human.values[i][0])
#         print(my_qa_human.values[i][1])

