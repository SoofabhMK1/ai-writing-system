from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    gender = Column(String)
    age = Column(Integer)
    occupation = Column(String)
    brief_introduction = Column(Text)
    
    # JSONB fields for flexible attributes
    physical_attributes = Column(JSONB)
    personality_traits = Column(JSONB)
    background_story = Column(JSONB)
    custom_fields = Column(JSONB)
