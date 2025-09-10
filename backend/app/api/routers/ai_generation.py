import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app import crud, schemas
from app.database import get_db
from app.crud import crud_setting
from app.services import ai_service

# --- Helper Function and Models ---

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

class GenerationRequest(BaseModel):
    project_id: int
    ai_model_id: int
    worldview_id: int | None = None
    writing_style_id: int | None = None
    target_word_count: int

class GenerationRequestWithPrompt(GenerationRequest):
    prompt: str

class ChatRequest(BaseModel):
    ai_model_id: int
    messages: List[schemas.MessageCreate]

# --- AI Generation Router ---

router = APIRouter(
    prefix="/ai",
    tags=["AI Generation"],
)

@router.post("/get-initial-prompt", response_model=str)
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

@router.post("/generate-outline-stream")
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

@router.post("/chat-stream")
async def chat_stream(req: ChatRequest, db: Session = Depends(get_db)):
    ai_model = crud_setting.ai_model.get(db, id=req.ai_model_id)
    if not ai_model:
        raise HTTPException(status_code=404, detail="AI Model not found")

    return StreamingResponse(
        ai_service.generate_chat_completion(
            model_config=ai_model,
            messages=[message.dict() for message in req.messages],
        ),
        media_type="text/event-stream"
    )

@router.post("/generate-outline")
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
    
    stream = ai_service.generate_outline_from_config(
        model_config=ai_model,
        prompt=prompt,
    )

    full_content = ""
    async for sse_event in stream:
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
        
        if event_type == "content" and data_str:
            data = json.loads(data_str)
            full_content += data.get("chunk", "")

    return {"status": "success", "outline": full_content}
