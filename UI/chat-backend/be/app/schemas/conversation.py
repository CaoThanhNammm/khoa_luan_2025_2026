from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    type: str  # USER or BOT

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    conversation_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str

class ConversationCreate(BaseModel):
    message: str

class ConversationWithDocumentCreate(BaseModel):
    message: str
    document_id: str

class EmptyConversationWithDocumentCreate(BaseModel):
    document_id: str
    filename: str
    title: Optional[str] = None
    file_size: Optional[int] = None
    status: Optional[str] = None
    s3_key: Optional[str] = None
    s3_url: Optional[str] = None

class ConversationResponse(ConversationBase):
    id: str
    user_id: int
    created_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

class MessageRequest(BaseModel):
    message: str
    document_id: Optional[str] = None

class StudentHandbookConversationCreate(BaseModel):
    """Schema for creating empty conversation for student handbook"""
    pass

class StudentHandbookMessageRequest(BaseModel):
    """Schema for sending message to student handbook (creates conversation if needed)"""
    message: str