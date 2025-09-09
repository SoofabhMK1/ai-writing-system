# backend/app/crud/crud_setting.py
from sqlalchemy.orm import Session
from app.models import setting as models
from app.schemas import setting as schemas
from app.crud.base import CRUDBase

# CRUD for Worldview
class CRUDWorldview(CRUDBase[models.Worldview, schemas.WorldviewCreate, schemas.WorldviewUpdate]):
    pass

worldview = CRUDWorldview(models.Worldview)

# CRUD for WritingStyle
class CRUDWritingStyle(CRUDBase[models.WritingStyle, schemas.WritingStyleCreate, schemas.WritingStyleUpdate]):
    pass

writing_style = CRUDWritingStyle(models.WritingStyle)

# CRUD for PromptTemplate
class CRUDPromptTemplate(CRUDBase[models.PromptTemplate, schemas.PromptTemplateCreate, schemas.PromptTemplateUpdate]):
    pass

prompt_template = CRUDPromptTemplate(models.PromptTemplate)
