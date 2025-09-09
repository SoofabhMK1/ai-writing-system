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

class WorldviewInDB(WorldviewBase):
    id: int

    class Config:
        from_attributes = True

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

class WritingStyleInDB(WritingStyleBase):
    id: int

    class Config:
        from_attributes = True

# --- PromptTemplate Schemas ---
class PromptTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    template_text: str
    variables: Optional[Dict[str, Any]] = None

class PromptTemplateCreate(PromptTemplateBase):
    pass

class PromptTemplateInDB(PromptTemplateBase):
    id: int

    class Config:
        from_attributes = True

# --- GeneratedOutline Schemas ---
class GeneratedOutlineBase(BaseModel):
    project_id: int
    version_name: Optional[str] = None
    target_word_count: Optional[int] = None
    worldview_id: Optional[int] = None
    writing_style_id: Optional[int] = None
    settings_snapshot: Optional[Dict[str, Any]] = None
    outline_data: Dict[str, Any]

class GeneratedOutlineCreate(GeneratedOutlineBase):
    pass

class GeneratedOutlineInDB(GeneratedOutlineBase):
    id: int
    created_at: Any # Using Any for datetime for simplicity, can be stricter

    class Config:
        from_attributes = True

# --- AIModel Schemas ---
class AIModelBase(BaseModel):
    name: str
    api_url: str
    api_key: str
    model_name: str

class AIModelCreate(AIModelBase):
    pass

class AIModelInDB(AIModelBase):
    id: int
    api_key: str = "********" # Never send the real key to the client

    class Config:
        from_attributes = True
