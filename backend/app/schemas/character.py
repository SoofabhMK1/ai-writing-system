from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class CharacterBase(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None
    brief_introduction: Optional[str] = None
    physical_attributes: Optional[Dict[str, Any]] = None
    body_details: Optional[Dict[str, Any]] = None
    clothing_style_and_habits: Optional[Dict[str, Any]] = None
    personality_traits: Optional[Dict[str, Any]] = None
    background_story: Optional[Dict[str, Any]] = None
    sexual_preferences_and_behaviors: Optional[Dict[str, Any]] = None
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

    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Character(CharacterInDBBase):
    pass


# Properties stored in DB
class CharacterInDB(CharacterInDBBase):
    pass
