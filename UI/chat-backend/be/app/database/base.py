from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
load_dotenv()

# Đọc biến môi trường
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_NAME = os.getenv("DB_NAME", "khoa_luan_01")

# Encode password an toàn (phòng ký tự đặc biệt)
DB_PASSWORD = quote_plus(DB_PASSWORD)

# Tạo chuỗi kết nối
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Khởi tạo engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho ORM models
Base = declarative_base()

# Dependency để lấy DB session (dùng trong FastAPI hoặc app khác)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()