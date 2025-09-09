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
    project_in: schemas.ProjectUpdate,
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

outline_router = APIRouter(
    prefix="/outline-nodes",
    tags=["Outline Nodes"],
)

@outline_router.get("/project/{project_id}", response_model=List[schemas.OutlineNode])
def read_outline_nodes_for_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    获取指定项目的所有大纲节点（以树状结构返回）。
    """
    return crud.outline_node.get_all_by_project(db=db, project_id=project_id)


@outline_router.post("/", response_model=schemas.OutlineNode)
def create_outline_node(
    node_in: schemas.OutlineNodeCreate,
    db: Session = Depends(get_db)
):
    """
    创建一个新的大纲节点。
    """
    return crud.outline_node.create(db=db, obj_in=node_in)


@outline_router.put("/{node_id}", response_model=schemas.OutlineNode)
def update_outline_node(
    node_id: int,
    node_in: schemas.OutlineNodeUpdate,
    db: Session = Depends(get_db)
):
    """
    更新一个大纲节点的信息（如标题、内容、顺序等）。
    """
    db_node = crud.outline_node.get(db=db, id=node_id)
    if not db_node:
        raise HTTPException(status_code=404, detail="Outline node not found")
    return crud.outline_node.update(db=db, db_obj=db_node, obj_in=node_in)


@outline_router.delete("/{node_id}", response_model=schemas.OutlineNode)
def delete_outline_node(
    node_id: int,
    db: Session = Depends(get_db)
):
    """
    删除一个大纲节点（及其所有子节点）。
    """
    db_node = crud.outline_node.remove(db=db, id=node_id)
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    return db_node