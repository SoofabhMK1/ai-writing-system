from typing import Any, Dict, Union

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, BaseModel]):
    async def create(self, db: AsyncSession, *, obj_in: ConversationCreate) -> Conversation:
        # Create the Conversation object without messages first
        conversation_data = obj_in.dict(exclude={"messages"})
        db_conversation = Conversation(**conversation_data)
        db.add(db_conversation)
        await db.flush()
        await db.refresh(db_conversation)  # Refresh to get the ID

        # Now create the Message objects with the new conversation_id
        for message_in in obj_in.messages:
            db_message = Message(
                **message_in.dict(), conversation_id=db_conversation.id
            )
            db.add(db_message)

        await db.commit()
        await db.refresh(db_conversation) # Refresh again to establish relationships in the session

        # Finally, re-fetch the object with the relationship explicitly loaded for the response
        stmt = (
            select(self.model)
            .options(selectinload(self.model.messages))
            .where(self.model.id == db_conversation.id)
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def get_with_messages(self, db: AsyncSession, *, id: int) -> Conversation | None:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.messages))
            .where(self.model.id == id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Conversation,
        obj_in: Union[ConversationCreate, Dict[str, Any]],
    ) -> Conversation:
        conversation_id = db_obj.id  # Store ID before the session expires the object
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
                await db.delete(message)

            # Create new messages
            for message_in in update_data["messages"]:
                db_message = Message(**message_in, conversation_id=db_obj.id)
                db.add(db_message)

        db.add(db_obj)
        await db.commit()

        # Re-fetch to ensure relationships are loaded for the response
        stmt = (
            select(self.model)
            .options(selectinload(self.model.messages))
            .where(self.model.id == conversation_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one()


conversation = CRUDConversation(Conversation)
