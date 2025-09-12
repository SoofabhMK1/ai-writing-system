from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.PromptPreset)
async def create_prompt_preset(
    *,
    db: AsyncSession = Depends(get_db),
    prompt_preset_in: schemas.PromptPresetCreate,
):
    """
    Create new prompt preset.
    """
    prompt_preset = await crud.prompt_preset.create(db=db, obj_in=prompt_preset_in)
    return prompt_preset

@router.get("/", response_model=List[schemas.PromptPreset])
async def read_prompt_presets(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve prompt presets.
    """
    prompt_presets = await crud.prompt_preset.get_multi(db=db, skip=skip, limit=limit)
    return prompt_presets

@router.put("/{id}", response_model=schemas.PromptPreset)
async def update_prompt_preset(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    prompt_preset_in: schemas.PromptPresetUpdate,
):
    """
    Update a prompt preset.
    """
    prompt_preset = await crud.prompt_preset.get(db=db, id=id)
    if not prompt_preset:
        raise HTTPException(status_code=404, detail="Prompt preset not found")
    prompt_preset = await crud.prompt_preset.update(db=db, db_obj=prompt_preset, obj_in=prompt_preset_in)
    return prompt_preset

@router.get("/{id}", response_model=schemas.PromptPreset)
async def read_prompt_preset(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
):
    """
    Get prompt preset by ID.
    """
    prompt_preset = await crud.prompt_preset.get(db=db, id=id)
    if not prompt_preset:
        raise HTTPException(status_code=404, detail="Prompt preset not found")
    return prompt_preset

@router.delete("/{id}", response_model=schemas.PromptPreset)
async def delete_prompt_preset(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
):
    """
    Delete a prompt preset.
    """
    prompt_preset = await crud.prompt_preset.get(db=db, id=id)
    if not prompt_preset:
        raise HTTPException(status_code=404, detail="Prompt preset not found")
    prompt_preset = await crud.prompt_preset.remove(db=db, id=id)
    return prompt_preset
