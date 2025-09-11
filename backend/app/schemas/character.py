from pydantic import BaseModel
from typing import Optional, Dict, Any

# Shared properties
class CharacterBase(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None
    brief_introduction: Optional[str] = None
    physical_attributes: Optional[Dict[str, Any]] = None
    personality_traits: Optional[Dict[str, Any]] = None
    background_story: Optional[Dict[str, Any]] = None
    custom_fields: Optional[Dict[str, Any]] = None

# Properties to receive on item creation
class CharacterCreate(CharacterBase):
    name: str

# Properties to receive on item update
class CharacterUpdate(CharacterBase):
    pass

# Properties shared by models stored in DB
class CharacterInDBBase(CharacterBase):
    id: int
    name: str

    class Config:
        orm_mode = True

# Properties to return to client
class Character(CharacterInDBBase):
    pass

# Properties stored in DB
class CharacterInDB(CharacterInDBBase):
    pass
