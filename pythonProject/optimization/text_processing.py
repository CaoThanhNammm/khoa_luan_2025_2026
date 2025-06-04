"""
Module xử lý tiền xử lý văn bản tiếng Việt tối ưu hóa
"""

import re
import os
import unicodedata
import string
from typing import List, Set, Optional

class OptimizedVietnameseProcessor:
    """
    Xử lý tiền xử lý văn bản tiếng Việt tối ưu hóa
    """
    
    def __init__(self):
        """Khởi tạo bộ xử lý văn bản tiếng Việt"""
        self.stopwords = self._load_stopwords()
        
    def _load_stopwords(self) -> Set[str]:
        """Tải danh sách stopwords tiếng Việt"""
        try:
            # Thử tải từ thư mục gốc
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            stopwords_path = os.path.join(root_dir, 'vietnamese_stopwords.txt')
            
            if not os.path.exists(stopwords_path):
                # Thử tải từ thư mục hiện tại
                stopwords_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vietnamese_stopwords.txt')
                
                if not os.path.exists(stopwords_path):
                    # Tạo tập stopwords mặc định nếu không tìm thấy file
                    return self._default_stopwords()
            
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                return set(f.read().splitlines())
                
        except Exception:
            # Sử dụng tập mặc định nếu có lỗi
            return self._default_stopwords()
    
    def _default_stopwords(self) -> Set[str]:
        """Tạo tập stopwords mặc định"""
        return {
            'và', 'của', 'cho', 'là', 'để', 'trong', 'với', 'có', 'được', 'không',
            'những', 'các', 'từ', 'về', 'như', 'trên', 'theo', 'tại', 'bởi', 'lúc',
            'vì', 'do', 'đã', 'sẽ', 'đang', 'nên', 'ra', 'thì', 'nếu', 'còn', 'khi',
            'cũng', 'vẫn', 'rằng', 'tuy', 'nhưng', 'mà', 'vào', 'hay'
        }
    
    def normalize_unicode(self, text: str, form: str = 'NFC') -> str:
        """Chuẩn hóa Unicode"""
        return unicodedata.normalize(form, text)
    
    def remove_punctuation(self, text: str) -> str:
        """Loại bỏ dấu câu"""
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)
    
    def remove_numbers(self, text: str) -> str:
        """Loại bỏ số"""
        return re.sub(r'\d+', '', text)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Loại bỏ stopwords"""
        return [token for token in tokens if token not in self.stopwords]
    
    def tokenize(self, text: str) -> List[str]:
        """Tách từ đơn giản"""
        return text.split()
    
    def text_preprocessing_vietnamese(self, text: str, remove_stop: bool = False) -> str:
        """Tiền xử lý toàn diện cho văn bản tiếng Việt"""
        # Chuẩn hóa unicode
        text = self.normalize_unicode(text)
        
        # Chuyển thành chữ thường
        text = text.lower()
        
        # Loại bỏ số thứ tự ở đầu câu (VD: "1. ", "a) ")
        text = re.sub(r'^\d+[\.\)\-]\s*', '', text)
        text = re.sub(r'^[a-z][\.\)\-]\s*', '', text)
        
        # Loại bỏ ký tự đặc biệt
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Loại bỏ stopwords nếu cần
        if remove_stop:
            tokens = self.tokenize(text)
            tokens = self.remove_stopwords(tokens)
            text = ' '.join(tokens)
        
        return text
        
    def clean_question(self, question: str) -> str:
        """Làm sạch câu hỏi"""
        # Chuẩn hóa unicode
        question = self.normalize_unicode(question)
        
        # Xóa ký tự đặc biệt và khoảng trắng thừa
        question = re.sub(r'[^\w\s\?\.]', ' ', question)
        question = re.sub(r'\s+', ' ', question).strip()
        
        return question

# Tạo instance global để tái sử dụng
vietnamese_processor = OptimizedVietnameseProcessor()
