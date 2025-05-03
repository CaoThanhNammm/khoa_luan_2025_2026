import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging
from logging.handlers import RotatingFileHandler
import google.generativeai as genai
from werkzeug.exceptions import HTTPException

from Chat import Chat
from LLM.Gemini import Gemini
from PreProcessing.PreProcessing import PreProcessing

app = Flask(__name__)

# Cấu hình CORS (cho phép frontend từ các domain cụ thể)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Cập nhật origins trong production

# Cấu hình logging
log_handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=5)
log_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# Cấu hình rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Cấu hình Gemini API
try:
    model_name = os.getenv('MODEL')
    api_key = os.getenv('API_KEY')
    pre_processing = PreProcessing()
    my_qa = pd.DataFrame(columns=['question', 'answer'])
    t = 2
    gemini = Gemini(model_name, api_key)
    chat = Chat(t, gemini, pre_processing)
except Exception as e:
    app.logger.error(f"Failed to configure Gemini API: {str(e)}")
    raise Exception("Gemini API configuration failed")


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Xử lý lỗi HTTP"""
    response = e.get_response()
    response.data = jsonify({
        "error": e.description,
        "status": "failed",
        "code": e.code
    }).get_data()
    response.content_type = "application/json"
    app.logger.error(f"HTTP Error {e.code}: {e.description}")
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    """Xử lý lỗi chung"""
    app.logger.error(f"Unexpected error: {str(e)}")
    return jsonify({
        "error": "Internal server error",
        "status": "failed"
    }), 500


@app.route('/api/gemini', methods=['POST'])
@limiter.limit("10 per minute")  # Giới hạn 10 request/phút mỗi IP
def gemini_endpoint():
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        if not data or 'question' not in data:
            app.logger.warning("Invalid request: Missing prompt or question")
            return jsonify({'error': 'Missing prompt or question in request'}), 400

        question = data['question']

        # Kiểm tra độ dài đầu vào
        if len(question) > 500:
            app.logger.warning("Input too long")
            return jsonify({'error': 'Prompt or question too long'}), 400

        # Kết hợp prompt và question
        question = f"Câu hỏi: {question}"

        # Gọi Gemini API
        answer = chat.answer(question)

        # Trả về kết quả
        app.logger.info("Request processed successfully")
        return jsonify({
            'response': answer,
            'status': 'success'
        })
    except Exception as e:
        app.logger.error(f"Error processing Gemini request: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500


@app.route('/', methods=['GET'])
def home():
    app.logger.info("Home endpoint accessed")
    return jsonify({
        'message': 'Welcome to Flask-Gemini API',
        'status': 'running'
    })


if __name__ == '__main__':
    # Chỉ dùng cho môi trường phát triển
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5001)))