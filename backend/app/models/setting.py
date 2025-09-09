# backend/app/models/setting.py
from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

class Worldview(Base):
    __tablename__ = "worldviews"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    genre = Column(String)
    time_period = Column(String)
    technology_level = Column(String)
    magic_system = Column(Text)
    additional_details = Column(JSONB)

class WritingStyle(Base):
    __tablename__ = "writing_styles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    tone = Column(ARRAY(String))
    point_of_view = Column(String)
    reference_works = Column(Text)
    guidelines = Column(JSONB)

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    template_text = Column(Text, nullable=False)
    variables = Column(JSONB)
