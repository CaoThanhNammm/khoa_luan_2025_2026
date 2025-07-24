# Global Instances Configuration

## Tổng quan

Hệ thống đã được cấu hình để khởi tạo tất cả các đối tượng cần thiết (PDF, Llama models, Qdrant, Neo4j) **một lần duy nhất** khi server khởi động, thay vì khởi tạo lại nhiều lần trong các service khác nhau.

## Các đối tượng được khởi tạo global

1. **PDF**: Xử lý file PDF từ S3
2. **Llama Models**: 
   - `llama_chunks`: Tạo chunking
   - `llama_title`: Tạo tiêu đề
   - `llama_content`: Xử lý nội dung
3. **Qdrant**: Vector database với các embedding models
4. **Neo4j**: Knowledge graph database
5. **PreProcessing**: Xử lý văn bản
6. **S3 Client**: AWS S3 client

## Cách hoạt động

### 1. Khởi tạo khi server start

Trong `main.py`:
```python
# Initialize all global instances once when server starts
from app.core.global_instances import initialize_global_instances
initialize_global_instances()
```

**Đảm bảo chỉ khởi tạo một lần**: Hệ thống sử dụng flag `_initialized` để đảm bảo `🚀 Initializing global instances...` chỉ được gọi một lần duy nhất, ngay cả khi có nhiều services cố gắng truy cập global instances.

### 2. Sử dụng trong services

Trong các service files (như `document_service.py`, `chat_service.py`):
```python
from app.core.global_instances import (
    get_pdf, get_llama_chunks, get_llama_title, get_llama_content,
    get_qdrant, get_neo, get_preprocessing, get_s3_client
)

# Lấy global instances
pdf = get_pdf()
llama_chunks = get_llama_chunks()
qdrant = get_qdrant()
# ... etc
```

## Cấu hình Environment Variables

Copy file `.env.example` thành `.env` và điền các giá trị:

```bash
cp .env.example .env
```

Các biến môi trường cần thiết:
- AWS credentials và S3 config
- Embedding model names
- Qdrant host và API key
- Llama model names và NVIDIA API keys
- Neo4j connection details

## Lợi ích

1. **Performance**: Khởi tạo một lần thay vì nhiều lần
2. **Memory**: Tiết kiệm bộ nhớ bằng cách chia sẻ instances
3. **Consistency**: Đảm bảo tất cả services sử dụng cùng configuration
4. **Maintainability**: Dễ dàng thay đổi cấu hình ở một nơi

## Lưu ý

- Tất cả global instances được khởi tạo khi server start
- Nếu có lỗi trong quá trình khởi tạo, server sẽ log lỗi nhưng vẫn tiếp tục chạy
- Các getter functions sẽ throw RuntimeError nếu instance chưa được khởi tạo
- Đảm bảo tất cả environment variables được set đúng trước khi start server

## Kiểm tra trạng thái

Bạn có thể kiểm tra trạng thái khởi tạo bằng cách gọi endpoint:
```
GET /status/global-instances
```

Response sẽ cho biết trạng thái của từng component:
```json
{
  "initialized": true,
  "pdf": true,
  "llama_chunks": true,
  "llama_title": true,
  "llama_content": true,
  "qdrant": true,
  "neo": true,
  "pre_processing": true,
  "s3_client": true
}
```

## Troubleshooting

Nếu gặp lỗi "instance not initialized":
1. Kiểm tra logs khi server start để xem lỗi khởi tạo
2. Đảm bảo tất cả environment variables được set
3. Kiểm tra network connectivity đến các external services (Qdrant, Neo4j, etc.)
4. Gọi endpoint `/status/global-instances` để xem component nào failed
5. Kiểm tra logs để tìm thông báo `🚀 Initializing global instances...` - chỉ nên xuất hiện một lần