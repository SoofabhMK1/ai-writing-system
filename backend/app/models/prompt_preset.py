from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class PromptPreset(Base):
    __tablename__ = "prompt_presets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    system_prompt = Column(Text, nullable=True)
    cot_guidance = Column(Text, nullable=True)
    other_instructions = Column(Text, nullable=True)
