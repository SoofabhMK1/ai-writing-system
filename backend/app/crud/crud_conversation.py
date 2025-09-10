from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate
from app.models.message import Message
from typing import Any, Dict, Union
from pydantic import BaseModel

class CRUDConversation(CRUDBase[Conversation, ConversationCreate, BaseModel]):
    def create(self, db: Session, *, obj_in: ConversationCreate) -> Conversation:
        conversation_data = obj_in.dict(exclude={"messages"})
        db_conversation = Conversation(**conversation_data)
        db.add(db_conversation)
        db.flush()

        for message_in in obj_in.messages:
            db_message = Message(**message_in.dict(), conversation_id=db_conversation.id)
            db.add(db_message)

        db.commit()
        db.refresh(db_conversation)
        return db_conversation

    def update(
        self, db: Session, *, db_obj: Conversation, obj_in: Union[ConversationCreate, Dict[str, Any]]
    ) -> Conversation:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # Update conversation fields
        db_obj.title = update_data.get("title", db_obj.title)

        # Replace messages
        if "messages" in update_data:
            # Delete old messages
            for message in db_obj.messages:
                db.delete(message)
            
            # Create new messages
            for message_in in update_data["messages"]:
                db_message = Message(**message_in, conversation_id=db_obj.id)
                db.add(db_message)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

conversation = CRUDConversation(Conversation)
