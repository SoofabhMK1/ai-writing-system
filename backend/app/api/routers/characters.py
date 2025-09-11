from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.database import get_db

router = APIRouter()


async def get_character_or_404(
    character_id: int, db: Annotated[AsyncSession, Depends(get_db)]
) -> models.Character:
    character = await crud.character.get(db=db, id=character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.get("/", response_model=List[schemas.Character])
async def read_characters(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve characters.
    """
    characters = await crud.character.get_multi(db, skip=skip, limit=limit)
    return characters


@router.post("/", response_model=schemas.Character)
async def create_character(
    *,
    db: Annotated[AsyncSession, Depends(get_db)],
    character_in: schemas.CharacterCreate,
) -> Any:
    """
    Create new character.
    """
    character = await crud.character.create(db=db, obj_in=character_in)
    return character


@router.get("/{character_id}", response_model=schemas.Character)
async def read_character(
    *,
    character: Annotated[models.Character, Depends(get_character_or_404)],
) -> Any:
    """
    Get character by ID.
    """
    return character


@router.put("/{character_id}", response_model=schemas.Character)
async def update_character(
    *,
    db: Annotated[AsyncSession, Depends(get_db)],
    character: Annotated[models.Character, Depends(get_character_or_404)],
    character_in: schemas.CharacterUpdate,
) -> Any:
    """
    Update a character.
    """
    character = await crud.character.update(
        db=db, db_obj=character, obj_in=character_in
    )
    return character


@router.delete("/{character_id}", response_model=schemas.Character)
async def delete_character(
    *,
    db: Annotated[AsyncSession, Depends(get_db)],
    character: Annotated[models.Character, Depends(get_character_or_404)],
) -> Any:
    """
    Delete a character.
    """
    character = await crud.character.remove(db=db, id=character.id)
    return character
