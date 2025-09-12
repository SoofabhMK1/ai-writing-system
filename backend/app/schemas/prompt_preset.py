from pydantic import BaseModel
from typing import Optional

class PromptPresetBase(BaseModel):
    name: str
    system_prompt: Optional[str] = None
    cot_guidance: Optional[str] = None
    other_instructions: Optional[str] = None

class PromptPresetCreate(PromptPresetBase):
    pass

class PromptPresetUpdate(PromptPresetBase):
    pass

class PromptPresetInDBBase(PromptPresetBase):
    id: int

    class Config:
        from_attributes = True

class PromptPreset(PromptPresetInDBBase):
    pass
