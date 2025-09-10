from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Conversation)
def create_conversation(
    *,
    db: Session = Depends(get_db),
    conversation_in: schemas.ConversationCreate,
):
    conversation = crud.conversation.create(db=db, obj_in=conversation_in)
    return conversation

@router.get("/project/{project_id}", response_model=List[schemas.Conversation])
def read_conversations_by_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    conversations = db.query(crud.conversation.model).filter(crud.conversation.model.project_id == project_id).all()
    return conversations

@router.get("/{conversation_id}", response_model=schemas.Conversation)
def read_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    db_conversation = crud.conversation.get(db, id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.put("/{conversation_id}", response_model=schemas.Conversation)
def update_conversation(
    *,
    db: Session = Depends(get_db),
    conversation_id: int,
    conversation_in: schemas.ConversationCreate,
):
    db_conversation = crud.conversation.get(db, id=conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation = crud.conversation.update(db=db, db_obj=db_conversation, obj_in=conversation_in)
    return conversation

@router.delete("/{conversation_id}", response_model=schemas.Conversation)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    db_conversation = crud.conversation.remove(db, id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation
