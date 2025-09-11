from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .message import Message, MessageCreate


class ConversationBase(BaseModel):
    title: Optional[str] = None


class ConversationCreate(ConversationBase):
    project_id: Optional[int] = None
    messages: List[MessageCreate]


class Conversation(ConversationBase):
    id: int
    project_id: Optional[int] = None
    created_at: datetime
    messages: List[Message] = []

    model_config = ConfigDict(from_attributes=True)
