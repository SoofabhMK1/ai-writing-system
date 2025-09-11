from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Character])
def read_characters(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve characters.
    """
    characters = crud.character.get_multi(db, skip=skip, limit=limit)
    return characters


@router.post("/", response_model=schemas.Character)
def create_character(
    *,
    db: Session = Depends(get_db),
    character_in: schemas.CharacterCreate,
) -> Any:
    """
    Create new character.
    """
    character = crud.character.create(db=db, obj_in=character_in)
    return character
