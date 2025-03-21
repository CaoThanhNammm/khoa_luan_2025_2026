import json
import py_vncorenlp
from dotenv import load_dotenv
load_dotenv()
import re

class PreProcessing:
    # r'C:\Users\Nam\Desktop\vncorenlp'
    def load_vncorenlp(self, save_dir):
        return py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=save_dir)

    def string_to_json(self, text):
        removed_special = text.replace("```", "").replace("json", "")
        removed_special = removed_special.strip()
        return json.loads(removed_special)

    def text_preprocessing_vietnamese(self, text, vncorenlp):
        # 1. Chuyển thành chữ thường
        text = text.lower()

        # 2. Loại bỏ dấu câu
        text = re.sub(r'[^\w\s]', '', text)

        # 4. Xóa khoảng trắng thừa
        text = text.strip()

        # 5. Tách từ (Tokenization)
        output = vncorenlp.word_segment(text)
        result_string = ' '.join(output)
        return result_string
