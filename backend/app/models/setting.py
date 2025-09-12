import enum
from sqlalchemy import Column, Integer, String, Text, ARRAY, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base
from app.database_types import JsonEncodedDict, StringArray

# Use JSONB for PostgreSQL, and a JSON-like type for other databases (like SQLite in tests)
JSON_TYPE = JSONB().with_variant(JsonEncodedDict, "sqlite")
ARRAY_TYPE = ARRAY(String).with_variant(StringArray, "sqlite")

class Worldview(Base):
    __tablename__ = "worldviews"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    genre = Column(String)
    time_period = Column(String)
    technology_level = Column(String)
    magic_system = Column(Text)
    additional_details = Column(JSON_TYPE)

class WritingStyle(Base):
    __tablename__ = "writing_styles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    tone = Column(ARRAY_TYPE)
    point_of_view = Column(String)
    reference_works = Column(Text)
    guidelines = Column(JSON_TYPE)

class PromptCategory(str, enum.Enum):
    SYSTEM_PROMPT = "SYSTEM_PROMPT"
    CHARACTER_PROMPT = "CHARACTER_PROMPT"
    PROJECT_PROMPT = "PROJECT_PROMPT"

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(Enum(PromptCategory))
    template_text = Column(Text, nullable=False)
    variables = Column(JSON_TYPE)

class GeneratedOutline(Base):
    __tablename__ = "generated_outlines"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    version_name = Column(String, nullable=True)
    
    # Generation Config Snapshot
    target_word_count = Column(Integer)
    worldview_id = Column(Integer, ForeignKey("worldviews.id"), nullable=True)
    writing_style_id = Column(Integer, ForeignKey("writing_styles.id"), nullable=True)
    settings_snapshot = Column(JSON_TYPE) # "Time capsule" of the settings used

    # Result
    outline_data = Column(JSON_TYPE, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    api_url = Column(String, nullable=False)
    api_key = Column(String, nullable=False) # In a real app, this should be encrypted
    model_name = Column(String, nullable=False)
