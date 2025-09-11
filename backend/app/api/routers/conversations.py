from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Conversation)
async def create_conversation(
    *,
    db: Annotated[AsyncSession, Depends(get_db)],
    conversation_in: schemas.ConversationCreate,
):
    conversation = await crud.conversation.create(db=db, obj_in=conversation_in)
    return conversation

@router.get("/", response_model=List[schemas.Conversation])
async def read_conversations(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(crud.conversation.model)
        .options(selectinload(crud.conversation.model.messages))
    )
    conversations = result.scalars().unique().all()
    return conversations

@router.get("/{conversation_id}", response_model=schemas.Conversation)
async def read_conversation(
    conversation_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_conversation = await crud.conversation.get_with_messages(db, id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.put("/{conversation_id}", response_model=schemas.Conversation)
async def update_conversation(
    *,
    db: Annotated[AsyncSession, Depends(get_db)],
    conversation_id: int,
    conversation_in: schemas.ConversationCreate,
):
    db_conversation = await crud.conversation.get_with_messages(db, id=conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation = await crud.conversation.update(db=db, db_obj=db_conversation, obj_in=conversation_in)
    return conversation

@router.delete("/{conversation_id}", response_model=schemas.Conversation)
async def delete_conversation(
    conversation_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_conversation = await crud.conversation.remove(db, id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation
