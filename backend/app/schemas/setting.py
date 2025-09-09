# backend/app/schemas/setting.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- Worldview Schemas ---
class WorldviewBase(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    time_period: Optional[str] = None
    technology_level: Optional[str] = None
    magic_system: Optional[str] = None
    additional_details: Optional[Dict[str, Any]] = None

class WorldviewCreate(WorldviewBase):
    pass

class WorldviewUpdate(WorldviewBase):
    pass

class WorldviewInDB(WorldviewBase):
    id: int

    class Config:
        orm_mode = True

# --- WritingStyle Schemas ---
class WritingStyleBase(BaseModel):
    name: str
    description: Optional[str] = None
    tone: Optional[List[str]] = None
    point_of_view: Optional[str] = None
    reference_works: Optional[str] = None
    guidelines: Optional[Dict[str, Any]] = None

class WritingStyleCreate(WritingStyleBase):
    pass

class WritingStyleUpdate(WritingStyleBase):
    pass

class WritingStyleInDB(WritingStyleBase):
    id: int

    class Config:
        orm_mode = True

# --- PromptTemplate Schemas ---
class PromptTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    template_text: str
    variables: Optional[Dict[str, Any]] = None

class PromptTemplateCreate(PromptTemplateBase):
    pass

class PromptTemplateUpdate(PromptTemplateBase):
    pass

class PromptTemplateInDB(PromptTemplateBase):
    id: int

    class Config:
        orm_mode = True
