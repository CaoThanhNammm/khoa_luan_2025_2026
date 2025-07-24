import ast
import asyncio
import time

from botocore.exceptions import NoCredentialsError, ClientError
from sqlalchemy.orm import Session
from app.models.document import UserDocument, ContactMessage
from app.schemas.document import DocumentCreate, ContactMessageCreate
from app.services.user_service import get_user_by_id
from fastapi import HTTPException, status, UploadFile
import os
import uuid
from dotenv import load_dotenv
from typing import Optional
from app.core.global_instances import (
    get_pdf, get_llama_chunks, get_llama_title, get_llama_content,
    get_qdrant, get_neo, get_preprocessing, get_s3_client
)
from LLM.prompt import extract_entities_relationship_from_text, chunking, create_title

load_dotenv()

# AWS S3 Configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "khoaluan111")
S3_REGION = os.getenv("S3_REGION", "ap-southeast-1")

# Global instances will be initialized lazily when needed
def _get_global_instances():
    """Get all global instances lazily"""
    return {
        'pdf': get_pdf(),
        'llama_chunks': get_llama_chunks(),
        'llama_title': get_llama_title(),
        'llama_content': get_llama_content(),
        'qdrant': get_qdrant(),
        'neo': get_neo(),
        'pre_processing': get_preprocessing(),
        's3_client': get_s3_client()
    }

def get_user_documents(db: Session, user_id: int):
    """Get all documents for a user"""
    return db.query(UserDocument).filter(UserDocument.user_id == user_id).all()

def get_document(db: Session, document_id: int):
    """Get a document by ID"""
    return db.query(UserDocument).filter(UserDocument.id == document_id).first()

def get_document_by_external_id(db: Session, document_id: str, user_id: int):
    """Get a document by external ID (document_id field)"""
    return db.query(UserDocument).filter(
        UserDocument.document_id == document_id,
        UserDocument.user_id == user_id
    ).first()

def create_document(db: Session, document: DocumentCreate, user_id: int):
    """Create a new document record"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_document = UserDocument(
        user_id=user_id,
        conversation_id=document.conversation_id,
        document_id=document.document_id,
        filename=document.filename,
        file_size=document.file_size,
        status=document.status,
        s3_key=document.s3_key,
        s3_url=document.s3_url
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

def update_document_status(db: Session, document_id: str, status: str, user_id: int):
    """Update a document's status"""
    document = get_document_by_external_id(db, document_id, user_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    document.status = status
    db.commit()
    db.refresh(document)
    
    return document

def upload_to_s3(file_content: bytes, file_name: str, document_id: str) -> dict:
    """Upload a file to S3"""
    instances = _get_global_instances()
    s3_client = instances['s3_client']
    
    if not s3_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="S3 client not initialized"
        )
    
    try:
        # Create S3 key with document_id to avoid duplicates
        s3_key = f"documents/{document_id}/{file_name}"
        
        # Upload file to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType='application/pdf'
        )
        
        s3_url = f"s3://{S3_BUCKET_NAME}/{s3_key}"
        
        return {
            "s3_key": s3_key,
            "s3_url": s3_url
        }
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload to S3: {str(e)}"
        )

async def process_file_upload(file: UploadFile, user_id: int, db: Session):
    """Process a file upload"""
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded"
        )
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted"
        )
    
    # Generate document ID
    document_id = str(uuid.uuid4())
    
    # Read file content
    contents = await file.read()
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty or could not be read"
        )
    
    # Upload to S3
    s3_info = upload_to_s3(contents, file.filename, document_id)
    
    # Create document record
    document = DocumentCreate(
        document_id=document_id,
        filename=file.filename,
        file_size=len(contents),
        status="processing",
        s3_key=s3_info["s3_key"],
        s3_url=s3_info["s3_url"]
    )
    
    db_document = create_document(db, document, user_id)

    # Process PDF after uploading to S3
    try:
        # Add timeout for PDF processing (20 minutes)
        await asyncio.wait_for(
            process_pdf(s3_info["s3_url"], s3_info["s3_key"], document_id),
            timeout=1200  # 20 minutes = 1200 seconds
        )
        # Update document status to completed
        update_document_status(db, document_id, "completed", user_id)
        final_status = "completed"
        print(f"🎉 PDF processing completed for document: {document_id}")
    except asyncio.TimeoutError:
        print(f"⏰ PDF processing timeout for document: {document_id}")
        update_document_status(db, document_id, "failed", user_id)
        final_status = "failed"
    except Exception as e:
        print(f"❌ Error processing PDF for document {document_id}: {str(e)}")
        # Update document status to failed
        update_document_status(db, document_id, "failed", user_id)
        final_status = "failed"

    return {
        "document_id": document_id,
        "filename": file.filename,
        "file_size": len(contents),
        "s3_key": s3_info["s3_key"],
        "s3_url": s3_info["s3_url"],
        "status": final_status
    }



def upload_to_s3_key(file_content: bytes, file_name: str, document_id: str) -> str:
    """
    Upload file to S3 and return the S3 key
    """
    try:
        instances = _get_global_instances()
        s3_client = instances['s3_client']
        
        if not s3_client:
            raise Exception("S3 client not initialized")

        # Tạo S3 key với document_id để tránh trùng lặp
        s3_key = f"documents/{document_id}/{file_name}"

        # Upload file to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType='application/pdf'
        )

        print(f"File uploaded to S3: s3://{S3_BUCKET_NAME}/{s3_key}")
        return s3_key

    except NoCredentialsError:
        print("AWS credentials not found")
        raise Exception("AWS credentials not configured")
    except ClientError as e:
        print(f"AWS S3 error: {str(e)}")
        raise Exception(f"Failed to upload to S3: {str(e)}")
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        raise


def get_s3_file_url(s3_key: str) -> str:
    """
    Generate S3 file URL
    """
    return f"s3://{S3_BUCKET_NAME}/{s3_key}"


async def process_pdf(s3_file_url: str, s3_key: str, document_id: str):
    try:
        instances = _get_global_instances()
        pdf = instances['pdf']
        
        pdf.set_path(s3_file_url)
        pdf.set_bucket_name(S3_BUCKET_NAME)
        pdf.set_key(s3_key)
        sentences = pdf.read_chunks()

        await _add_data_to_qdrant(sentences, document_id)
        await _add_data_to_neo4j(sentences, document_id)

        print("🎉 PDF processing hoàn tất.")
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error {str(e)}")


# Thêm file mới vào qdrant
async def _add_data_to_qdrant(sentences, document_id):
    try:
        instances = _get_global_instances()
        llama_chunks = instances['llama_chunks']
        qdrant = instances['qdrant']
        
        chunks = []
        all_paragraphs = []

        # sử dụng llama để tự động chia chunk. Output là mảng các json [{}, {}, {}]
        llama_chunks.set_prompt(chunking())
        for s in sentences:
            llama_chunks.set_text(s)
            try:
                chunk_json = llama_chunks.generator()
                chunk_json = chunk_json.replace("'", '"')
                chunk_json = ast.literal_eval(chunk_json)
            except:
                chunk_json = llama_chunks.generator()
                chunk_json = chunk_json.replace("'", '"')
                chunk_json = ast.literal_eval(chunk_json)

            print(chunk_json)
            chunks.append(chunk_json)

        # tạo ra mảng chứa các chunk. Output là mảng String ['', '', '']
        for chunk in chunks:
            for key, content in chunk.items():
                all_paragraphs.append(content)

        print(all_paragraphs)

        # 1. tạo collection trong qdrant
        qdrant.set_collection_name(document_id)
        qdrant.create_collection()

        # 2. Tạo embedding
        embeddings_dict = qdrant.create_embed(all_paragraphs)
        # 3. lưu vào qdrant
        qdrant.add_data(all_paragraphs, embeddings_dict)

        return {"message": "File uploaded and processed successfully for qdrant", "data": document_id}

    except Exception as e:
        print(f"Error processing file in qdrant: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file in qdrant: {str(e)}")


# Thêm file mới vào neo4j
async def _add_data_to_neo4j(sentences, document_id):
    try:
        instances = _get_global_instances()
        llama_title = instances['llama_title']
        llama_content = instances['llama_content']
        neo = instances['neo']
        pre_processing = instances['pre_processing']

        # Tạo ra tiêu đề cho đồ thị
        titles = []
        llama_title.set_prompt(create_title())
        i = 0
        for s in sentences:
            llama_title.set_text(s)
            title = llama_title.generator().lower()
            if i % 2 == 0:
                time.sleep(45)
            print(title)
            i += 1
            titles.append(pre_processing.string_to_json(title))

        print(titles)

        # Tạo ra entities và relationships
        entities_relationship = []
        llama_content.set_prompt(extract_entities_relationship_from_text())

        for s in sentences:
            llama_content.set_text(s)
            entity_relation = llama_content.generator().lower()
            entity_relation = pre_processing.string_to_json(entity_relation)
            print(entity_relation)
            entities_relationship.append(entity_relation)

        print(entities_relationship)

        # B1: Nối "General" với UUID người dùng (Document)
        neo.add_single_relationship("tài liệu", "General", document_id, "Document", "BAO_GỒM")

        # B2: Nối document với tiêu đề
        for title in titles:
            neo.add_single_relationship(document_id, "Document", title["title"], "Part", "BAO_GỒM")

        # B3: Nối tiêu đề với entities_relationship
        for r, title in zip(entities_relationship, titles):
            neo.import_relationships(r, title["title"], "Part")

        return {"message": "File uploaded and processed successfully for neo4j", "data": document_id}

    except Exception as e:
        print(f"Error processing file in neo4j: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file in neo4j: {str(e)}")



def create_contact_message(db: Session, contact: ContactMessageCreate):
    """Create a new contact message"""
    db_contact = ContactMessage(
        name=contact.name,
        email=contact.email,
        subject=contact.subject,
        message=contact.message
    )
    
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    return db_contact