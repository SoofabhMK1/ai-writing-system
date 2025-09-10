from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .message import Message, MessageCreate

class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    project_id: int
    messages: List[MessageCreate]

class Conversation(ConversationBase):
    id: int
    project_id: int
    created_at: datetime
    messages: List[Message] = []

    class Config:
        orm_mode = True
