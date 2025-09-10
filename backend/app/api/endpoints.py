from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.crud import crud_setting
from app.schemas import setting as setting_schemas
from app.core.security import decrypt_data
from app.services import ai_service
from pydantic import BaseModel
from app.models import Project, Worldview, WritingStyle

def get_generation_context(db: Session, project_id: int, worldview_id: int | None, writing_style_id: int | None) -> dict:
    project = crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    worldview = crud_setting.worldview.get(db, id=worldview_id) if worldview_id else None
    writing_style = crud_setting.writing_style.get(db, id=writing_style_id) if writing_style_id else None

    return {
        "project": project,
        "worldview": {c.name: getattr(worldview, c.name) for c in worldview.__table__.columns} if worldview else {},
        "writing_style": {c.name: getattr(writing_style, c.name) for c in writing_style.__table__.columns} if writing_style else {},
    }

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
    node_in: schemas.OutlineNodeBase,
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
def update_worldview(worldview_id: int, worldview_in: setting_schemas.WorldviewBase, db: Session = Depends(get_db)):
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
def update_writing_style(style_id: int, style_in: setting_schemas.WritingStyleBase, db: Session = Depends(get_db)):
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
def update_prompt_template(template_id: int, template_in: setting_schemas.PromptTemplateBase, db: Session = Depends(get_db)):
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

# Generated Outline Endpoints
@settings_router.post("/generated-outlines/", response_model=setting_schemas.GeneratedOutlineInDB)
def create_generated_outline(outline_in: setting_schemas.GeneratedOutlineCreate, db: Session = Depends(get_db)):
    return crud_setting.generated_outline.create(db=db, obj_in=outline_in)

@settings_router.get("/generated-outlines/project/{project_id}", response_model=List[setting_schemas.GeneratedOutlineInDB])
def read_generated_outlines_for_project(project_id: int, db: Session = Depends(get_db)):
    return crud_setting.generated_outline.get_all_by_project(db=db, project_id=project_id)

@settings_router.delete("/generated-outlines/{outline_id}", response_model=setting_schemas.GeneratedOutlineInDB)
def delete_generated_outline(outline_id: int, db: Session = Depends(get_db)):
    db_outline = crud_setting.generated_outline.remove(db=db, id=outline_id)
    if not db_outline:
        raise HTTPException(status_code=404, detail="Generated outline not found")
    return db_outline

# AI Model Endpoints
@settings_router.post("/ai-models/", response_model=setting_schemas.AIModelInDB)
def create_ai_model(model_in: setting_schemas.AIModelCreate, db: Session = Depends(get_db)):
    return crud_setting.ai_model.create(db=db, obj_in=model_in)

@settings_router.get("/ai-models/", response_model=List[setting_schemas.AIModelInDB])
def read_ai_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_setting.ai_model.get_multi(db, skip=skip, limit=limit)

@settings_router.put("/ai-models/{model_id}", response_model=setting_schemas.AIModelInDB)
def update_ai_model(model_id: int, model_in: setting_schemas.AIModelBase, db: Session = Depends(get_db)):
    db_model = crud_setting.ai_model.get(db, id=model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="AI Model not found")
    return crud_setting.ai_model.update(db=db, db_obj=db_model, obj_in=model_in)

@settings_router.delete("/ai-models/{model_id}", response_model=setting_schemas.AIModelInDB)
def delete_ai_model(model_id: int, db: Session = Depends(get_db)):
    db_model = crud_setting.ai_model.remove(db=db, id=model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="AI Model not found")
    return db_model

@settings_router.post("/ai-models/{model_id}/test-connection")
async def test_ai_connection(model_id: int, db: Session = Depends(get_db)):
    from openai import AsyncOpenAI

    db_model = crud_setting.ai_model.get(db, id=model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="AI Model not found")

    try:
        api_key_to_test = decrypt_data(db_model.api_key)
        client = AsyncOpenAI(
            base_url=db_model.api_url,
            api_key=api_key_to_test,
        )
        await client.models.list()
        return {"status": "success", "message": "连接成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"连接失败: {str(e)}")

# --- AI Generation Router ---
ai_router = APIRouter(
    prefix="/ai",
    tags=["AI Generation"],
)

class GenerationRequest(BaseModel):
    project_id: int
    ai_model_id: int
    worldview_id: int | None = None
    writing_style_id: int | None = None
    target_word_count: int

class GenerationRequestWithPrompt(GenerationRequest):
    prompt: str

@ai_router.post("/get-initial-prompt", response_model=str)
def get_initial_prompt(req: GenerationRequest, db: Session = Depends(get_db)):
    """
    Constructs and returns the initial prompt string based on configuration.
    """
    context = get_generation_context(db, req.project_id, req.worldview_id, req.writing_style_id)
    
    return ai_service.create_outline_generation_prompt(
        core_concept=context["project"].core_concept,
        worldview=context["worldview"],
        writing_style=context["writing_style"],
        target_word_count=req.target_word_count
    )

@ai_router.post("/generate-outline-stream")
async def generate_outline_stream(req: GenerationRequestWithPrompt, db: Session = Depends(get_db)):
    ai_model = crud_setting.ai_model.get(db, id=req.ai_model_id)
    if not ai_model:
        raise HTTPException(status_code=404, detail="AI Model not found")

    return StreamingResponse(
        ai_service.generate_outline_from_config(
            model_config=ai_model,
            prompt=req.prompt,
        ),
        media_type="text/event-stream"
    )

import json

@ai_router.post("/generate-outline")
async def generate_outline(req: GenerationRequest, db: Session = Depends(get_db)):
    context = get_generation_context(db, req.project_id, req.worldview_id, req.writing_style_id)
    
    ai_model = crud_setting.ai_model.get(db, id=req.ai_model_id)
    if not ai_model:
        raise HTTPException(status_code=404, detail="AI Model not found")

    prompt = ai_service.create_outline_generation_prompt(
        core_concept=context["project"].core_concept,
        worldview=context["worldview"],
        writing_style=context["writing_style"],
        target_word_count=req.target_word_count
    )
    
    # The service now returns an SSE-formatted stream
    stream = ai_service.generate_outline_from_config(
        model_config=ai_model,
        prompt=prompt,
    )

    # For the non-streaming endpoint, we must parse the SSE stream
    full_content = ""
    async for sse_event in stream:
        # SSE events are separated by double newlines
        lines = sse_event.strip().split('\n')
        event_type = None
        data_str = ""
        for line in lines:
            if line.startswith("event:"):
                event_type = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                data_str = line.split(":", 1)[1].strip()
        
        if event_type == "error":
            error_data = json.loads(data_str)
            raise HTTPException(status_code=500, detail=error_data.get("error", "Unknown AI error"))
        
        # We only care about the final 'content' for this non-streaming endpoint
        if event_type == "content" and data_str:
            data = json.loads(data_str)
            full_content += data.get("chunk", "")

    return {"status": "success", "outline": full_content}
