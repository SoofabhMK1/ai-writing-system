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


@router.get("/{character_id}", response_model=schemas.Character)
def read_character(
    *,
    db: Session = Depends(get_db),
    character_id: int,
) -> Any:
    """
    Get character by ID.
    """
    character = crud.character.get(db=db, id=character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.put("/{character_id}", response_model=schemas.Character)
def update_character(
    *,
    db: Session = Depends(get_db),
    character_id: int,
    character_in: schemas.CharacterUpdate,
) -> Any:
    """
    Update a character.
    """
    character = crud.character.get(db=db, id=character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    character = crud.character.update(db=db, db_obj=character, obj_in=character_in)
    return character


@router.delete("/{character_id}", response_model=schemas.Character)
def delete_character(
    *,
    db: Session = Depends(get_db),
    character_id: int,
) -> Any:
    """
    Delete a character.
    """
    character = crud.character.get(db=db, id=character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    character = crud.character.remove(db=db, id=character_id)
    return character
