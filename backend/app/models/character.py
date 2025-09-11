from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from app.database import Base
from app.database_types import JsonEncodedDict

# Use JSONB for PostgreSQL, and a JSON-like type for other databases (like SQLite in tests)
JSON_TYPE = JSONB().with_variant(JsonEncodedDict, "sqlite")

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    gender = Column(String)
    age = Column(Integer)
    occupation = Column(String)
    brief_introduction = Column(Text)
    
    # JSONB fields for flexible attributes
    physical_attributes = Column(JSON_TYPE)
    personality_traits = Column(JSON_TYPE)
    background_story = Column(JSON_TYPE)
    custom_fields = Column(JSON_TYPE)
