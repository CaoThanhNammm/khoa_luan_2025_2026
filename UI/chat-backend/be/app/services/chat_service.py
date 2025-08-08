from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import requests
import json
import os
import sys
from dotenv import load_dotenv
import uuid
from typing import List, Optional

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from Chat import Chat
from app.models.conversation import Conversation, Message
from app.models.document import UserDocument
from app.services.user_service import get_user_by_id
from app.core.global_instances import get_qdrant, get_neo, get_preprocessing
load_dotenv()

# Message types
USER_MESSAGE = "USER"
BOT_MESSAGE = "BOT"

# Cache for chat objects by conversation_id
_chat_cache = {}

def get_or_create_chat_for_conversation(conversation_id: str):
    """Get existing chat object from cache or create new one"""
    if conversation_id not in _chat_cache:
        _chat_cache[conversation_id] = init_chat_bot()
    return _chat_cache[conversation_id]

def remove_chat_from_cache(conversation_id: str):
    """Remove chat object from cache when conversation is deleted"""
    if conversation_id in _chat_cache:
        del _chat_cache[conversation_id]

def get_cache_info():
    """Get information about current cache state (for debugging)"""
    return {
        "cached_conversations": list(_chat_cache.keys()),
        "cache_size": len(_chat_cache)
    }

def get_conversation(db: Session, conversation_id: str):
    """Get a conversation by ID"""
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def get_user_conversations(db: Session, user_id: int):
    """Get all conversations for a user"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(Conversation.created_at.desc()).all()

def generate_title(message: str) -> str:
    """Generate a title for a conversation based on the first message"""
    # Truncate message if it's too long
    if len(message) > 50:
        return message[:47] + "..."
    return message

def get_chatbot_response_with_document(question: str, document_id: str) -> str:
    """Get a response from the chatbot API for a question about a specific document"""
    try:
        # Call the local API endpoint
        response = requests.post(
            "http://localhost:8000/api/chat",
            json={"question": question, "document_id": document_id},
            timeout=1200  # 20 minutes = 1200 seconds
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("data", "Sorry, I couldn't process your request.")
        else:
            print(f"Error from chatbot API: {response.status_code} - {response.text}")
            return "Sorry, there was an error processing your request."
    except Exception as e:
        print(f"Exception calling chatbot API: {str(e)}")
        return "Sorry, I'm having trouble connecting to my knowledge base right now."

def init_chat_bot():
    # Sử dụng các global instances đã được khởi tạo
    qdrant = get_qdrant()
    neo = get_neo()
    pre_processing = get_preprocessing()
        
    # Khởi tạo chat với các global instances
    t = 5
    return Chat(t, qdrant, neo, pre_processing, '')

def start_new_conversation(db: Session, user_id: int, message: str):
    """Start a new conversation"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create new conversation
    conversation = Conversation(
        id=str(uuid.uuid4()),
        title=generate_title(message),
        user_id=user_id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    # Get or create chat object for this conversation
    chat = get_or_create_chat_for_conversation(conversation.id)
    
    # Add user message
    user_message = Message(
        conversation_id=conversation.id,
        content=message,
        type=USER_MESSAGE
    )
    db.add(user_message)
    db.commit()
    
    # Get bot response
    chat.set_question(message)
    bot_response = chat.answer_s2s_stsv()

    # Add bot message
    bot_message = Message(
        conversation_id=conversation.id,
        content=bot_response,
        type=BOT_MESSAGE
    )
    db.add(bot_message)
    db.commit()
    
    # Refresh conversation to include messages
    db.refresh(conversation)
    
    return conversation

def start_new_conversation_with_document(db: Session, user_id: int, message: str, document_id: str):
    """Start a new conversation with a document context"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create new conversation
    conversation = Conversation(
        id=str(uuid.uuid4()),
        title=generate_title(message),
        user_id=user_id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    # Get or create chat object for this conversation
    chat = get_or_create_chat_for_conversation(conversation.id)
    
    # Create a user document entry if documentId is provided
    if document_id:
        try:
            filename = "Sổ tay sinh viên 2024" if document_id == "so_tay_sinh_vien_2024" else document_id
            user_document = UserDocument(
                user_id=user_id,
                conversation_id=conversation.id,
                document_id=document_id,
                filename=filename
            )
            db.add(user_document)
            db.commit()
        except Exception as e:
            print(f"Error creating user document entry: {str(e)}")
            # Continue without document association if this fails
    
    # Add user message
    user_message = Message(
        conversation_id=conversation.id,
        content=message,
        type=USER_MESSAGE
    )
    db.add(user_message)
    db.commit()

    chat.set_question(message)
    chat.set_document_id(document_id)
    bot_response = chat.answer_s2s()

    # Add bot message
    bot_message = Message(
        conversation_id=conversation.id,
        content=bot_response,
        type=BOT_MESSAGE
    )
    db.add(bot_message)
    db.commit()
    
    # Refresh conversation to include messages
    db.refresh(conversation)
    
    return conversation

def create_empty_conversation_with_document(
    db: Session, 
    user_id: int, 
    document_id: str, 
    filename: str, 
    title: Optional[str] = None,
    file_size: Optional[int] = None,
    status: Optional[str] = None,
    s3_key: Optional[str] = None,
    s3_url: Optional[str] = None
):
    """Create an empty conversation with document info"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create new conversation
    conversation_title = title if title else f"Chat với {filename}"
    conversation = Conversation(
        id=str(uuid.uuid4()),
        title=conversation_title,
        user_id=user_id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    # Create a user document entry
    if document_id:
        try:
            user_document = UserDocument(
                user_id=user_id,
                conversation_id=conversation.id,
                document_id=document_id,
                filename=filename,
                file_size=file_size,
                status=status or "processing",
                s3_key=s3_key,
                s3_url=s3_url
            )
            db.add(user_document)
            db.commit()
        except Exception as e:
            print(f"Error creating user document entry: {str(e)}")
            # Continue without document association if this fails
    
    return conversation

def send_message_stsv(db: Session, conversation_id: str, message: str, user_id: int):
    """Send a message in a conversation"""
    # Get conversation
    conversation = get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )
    
    # Get existing chat object from cache (should already exist)
    chat = get_or_create_chat_for_conversation(conversation_id)
    
    # Add user message
    user_message = Message(
        conversation_id=conversation_id,
        content=message,
        type=USER_MESSAGE
    )
    db.add(user_message)
    db.commit()

    
    # Get bot response
    chat.set_question(message)
    bot_response = chat.answer_s2s_stsv()

    # Add bot message
    bot_message = Message(
        conversation_id=conversation_id,
        content=bot_response,
        type=BOT_MESSAGE
    )
    db.add(bot_message)
    db.commit()
    db.refresh(bot_message)
    
    return bot_message

def send_message(db: Session, conversation_id: str, document_id: str, message: str, user_id: int):
    """Send a message in a conversation"""
    # Get conversation
    conversation = get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Get document_id from user_documents table based on conversation_id
    user_document = db.query(UserDocument).filter(
        UserDocument.conversation_id == conversation_id,
        UserDocument.user_id == user_id
    ).first()
    
    # Use document_id from database if available, otherwise use the provided one
    actual_document_id = user_document.document_id if user_document else document_id
    print(f"Using document_id: {actual_document_id} (from DB: {user_document is not None})")

    # Get existing chat object from cache (should already exist)
    chat = get_or_create_chat_for_conversation(conversation_id)

    # Add user message
    user_message = Message(
        conversation_id=conversation_id,
        content=message,
        type=USER_MESSAGE
    )
    db.add(user_message)
    db.commit()

    # Get bot response using the actual document_id from database
    chat.set_question(message)
    chat.set_document_id(actual_document_id)
    bot_response = chat.answer_s2s()

    # Add bot message
    bot_message = Message(
        conversation_id=conversation_id,
        content=bot_response,
        type=BOT_MESSAGE
    )
    db.add(bot_message)
    db.commit()
    db.refresh(bot_message)

    return bot_message

def create_empty_student_handbook_conversation(db: Session, user_id: int):
    """Create an empty conversation for student handbook"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create new conversation with default title
    conversation = Conversation(
        id=str(uuid.uuid4()),
        title="Chat với Sổ tay sinh viên",
        user_id=user_id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    # Create a user document entry for student handbook
    try:
        user_document = UserDocument(
            user_id=user_id,
            conversation_id=conversation.id,
            document_id="so_tay_sinh_vien_2024",
            filename="Sổ tay sinh viên 2024"
        )
        db.add(user_document)
        db.commit()
    except Exception as e:
        print(f"Error creating user document entry: {str(e)}")
        # Continue without document association if this fails
    
    return conversation

def send_message_to_student_handbook(db: Session, message: str, user_id: int, conversation_id: Optional[str] = None):
    """Send a message to student handbook. Creates new conversation if conversation_id is not provided."""
    
    # If no conversation_id provided, create a new conversation
    if not conversation_id:
        conversation = create_empty_student_handbook_conversation(db, user_id)
        conversation_id = conversation.id
        # Update conversation title based on first message
        conversation.title = generate_title(message)
        db.commit()
        # Get or create chat object for new conversation
        chat = get_or_create_chat_for_conversation(conversation_id)
    else:
        # Get existing conversation
        conversation = get_conversation(db, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )
        # Get existing chat object from cache
        chat = get_or_create_chat_for_conversation(conversation_id)
    
    # Add user message
    user_message = Message(
        conversation_id=conversation_id,
        content=message,
        type=USER_MESSAGE
    )
    db.add(user_message)
    db.commit()
    
    # Get bot response for student handbook
    chat.set_question(message)
    chat.set_document_id("so_tay_sinh_vien_2024")
    bot_response = chat.answer_s2s()
    
    # Add bot message
    bot_message = Message(
        conversation_id=conversation_id,
        content=bot_response,
        type=BOT_MESSAGE
    )
    db.add(bot_message)
    db.commit()
    db.refresh(bot_message)
    
    return bot_message

def delete_conversation(db: Session, conversation_id: str, user_id: int):
    """Delete a conversation"""
    conversation = get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != user_id:
        return False
    
    # Remove chat object from cache
    remove_chat_from_cache(conversation_id)
    
    db.delete(conversation)
    db.commit()
    
    return True