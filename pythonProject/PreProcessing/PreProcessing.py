import json
import py_vncorenlp
from dotenv import load_dotenv
load_dotenv()
import re
import os

class PreProcessing:
    def __init__(self):
        save_dir = r'C:\Users\Nam\Desktop\vncorenlp'
        self.vncorenlp = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=save_dir)


    def string_to_json(self, text):
        removed_special = text.replace("```", "").replace("json", "")
        removed_special = removed_special.strip()
        return json.loads(removed_special)

    def text_preprocessing_vietnamese(self, text):
        root_dir = os.path.dirname(os.path.abspath(__file__))  # Thư mục chứa file Python hiện tại
        root_dir = os.path.dirname(root_dir)  # Lên thư mục cha
        stopwords_path = os.path.join(root_dir, 'vietnamese_stopwords.txt')

        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stop_words = set(f.read().splitlines())

        # 1. Chuyển thành chữ thường
        text = text.lower()

        # 2. Loại bỏ ký tự đánh số/thứ tự ở đầu dòng (ví dụ: "1. ", "a) ")
        #    (?m) bật chế độ multiline, ^ khớp đầu dòng, \s* để bỏ khoảng trắng đầu dòng nếu có
        text = re.sub(r'(?m)^\s*(?:\d+\.|[a-z]\))\s*', '', text)

        # 3. Loại bỏ dấu câu
        text = re.sub(r'[^\w\s\n]', '', text)

        # 4. Xóa khoảng trắng thừa
        text = text.strip()

        # 5. Tách từ (Tokenization)
        output = self.vncorenlp.word_segment(text)  # output là một list
        output = output[0].split(' ')

        # 6. Loại bỏ stop words trực tiếp từ list
        filtered_words = [word for word in output if word not in stop_words]
        result_string = ' '.join(filtered_words)
        return result_string


