from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.crud import crud_setting
from app.schemas import setting as setting_schemas

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

# --- Settings Router ---
settings_router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)

# Worldview Endpoints
@settings_router.post("/worldviews/", response_model=setting_schemas.WorldviewInDB)
def create_worldview(worldview_in: setting_schemas.WorldviewCreate, db: Session = Depends(get_db)):
    return crud_setting.worldview.create(db=db, obj_in=worldview_in)

@settings_router.get("/worldviews/", response_model=List[setting_schemas.WorldviewInDB])
def read_worldviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_setting.worldview.get_multi(db, skip=skip, limit=limit)

@settings_router.put("/worldviews/{worldview_id}", response_model=setting_schemas.WorldviewInDB)
def update_worldview(worldview_id: int, worldview_in: setting_schemas.WorldviewUpdate, db: Session = Depends(get_db)):
    db_worldview = crud_setting.worldview.get(db, id=worldview_id)
    if not db_worldview:
        raise HTTPException(status_code=404, detail="Worldview not found")
    return crud_setting.worldview.update(db=db, db_obj=db_worldview, obj_in=worldview_in)

@settings_router.delete("/worldviews/{worldview_id}", response_model=setting_schemas.WorldviewInDB)
def delete_worldview(worldview_id: int, db: Session = Depends(get_db)):
    db_worldview = crud_setting.worldview.remove(db=db, id=worldview_id)
    if not db_worldview:
        raise HTTPException(status_code=404, detail="Worldview not found")
    return db_worldview

# Writing Style Endpoints
@settings_router.post("/writing-styles/", response_model=setting_schemas.WritingStyleInDB)
def create_writing_style(style_in: setting_schemas.WritingStyleCreate, db: Session = Depends(get_db)):
    return crud_setting.writing_style.create(db=db, obj_in=style_in)

@settings_router.get("/writing-styles/", response_model=List[setting_schemas.WritingStyleInDB])
def read_writing_styles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_setting.writing_style.get_multi(db, skip=skip, limit=limit)

@settings_router.put("/writing-styles/{style_id}", response_model=setting_schemas.WritingStyleInDB)
def update_writing_style(style_id: int, style_in: setting_schemas.WritingStyleUpdate, db: Session = Depends(get_db)):
    db_style = crud_setting.writing_style.get(db, id=style_id)
    if not db_style:
        raise HTTPException(status_code=404, detail="Writing style not found")
    return crud_setting.writing_style.update(db=db, db_obj=db_style, obj_in=style_in)

@settings_router.delete("/writing-styles/{style_id}", response_model=setting_schemas.WritingStyleInDB)
def delete_writing_style(style_id: int, db: Session = Depends(get_db)):
    db_style = crud_setting.writing_style.remove(db=db, id=style_id)
    if not db_style:
        raise HTTPException(status_code=404, detail="Writing style not found")
    return db_style

# Prompt Template Endpoints
@settings_router.post("/prompt-templates/", response_model=setting_schemas.PromptTemplateInDB)
def create_prompt_template(template_in: setting_schemas.PromptTemplateCreate, db: Session = Depends(get_db)):
    return crud_setting.prompt_template.create(db=db, obj_in=template_in)

@settings_router.get("/prompt-templates/", response_model=List[setting_schemas.PromptTemplateInDB])
def read_prompt_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_setting.prompt_template.get_multi(db, skip=skip, limit=limit)

@settings_router.put("/prompt-templates/{template_id}", response_model=setting_schemas.PromptTemplateInDB)
def update_prompt_template(template_id: int, template_in: setting_schemas.PromptTemplateUpdate, db: Session = Depends(get_db)):
    db_template = crud_setting.prompt_template.get(db, id=template_id)
    if not db_template:
        raise HTTPException(status_code=404, detail="Prompt template not found")
    return crud_setting.prompt_template.update(db=db, db_obj=db_template, obj_in=template_in)

@settings_router.delete("/prompt-templates/{template_id}", response_model=setting_schemas.PromptTemplateInDB)
def delete_prompt_template(template_id: int, db: Session = Depends(get_db)):
    db_template = crud_setting.prompt_template.remove(db=db, id=template_id)
    if not db_template:
        raise HTTPException(status_code=404, detail="Prompt template not found")
    return db_template
