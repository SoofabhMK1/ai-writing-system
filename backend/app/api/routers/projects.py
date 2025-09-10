from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

@router.post("/", response_model=schemas.Project)
def create_project(
    project_in: schemas.ProjectCreate, 
    db: Session = Depends(get_db)
):
    return crud.project.create(db=db, obj_in=project_in)

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud.project.get_multi(db, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: int, 
    db: Session = Depends(get_db)
):
    db_project = crud.project.get(db, id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project_in: schemas.ProjectBase,
    db: Session = Depends(get_db)
):
    db_project = crud.project.get(db, id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return crud.project.update(db=db, db_obj=db_project, obj_in=project_in)

@router.delete("/{project_id}", response_model=schemas.Project)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    db_project = crud.project.get(db, id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    crud.project.remove(db=db, id=project_id)
    return db_project
