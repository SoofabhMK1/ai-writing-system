# backend/app/crud/crud_setting.py
from sqlalchemy.orm import Session
from app.models import setting as models
from app.schemas import setting as schemas
from app.crud.base import CRUDBase
from app.core.security import encrypt_data
from typing import Dict, Any

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

# CRUD for GeneratedOutline
class CRUDGeneratedOutline(CRUDBase[models.GeneratedOutline, schemas.GeneratedOutlineCreate, schemas.GeneratedOutlineUpdate]):
    def get_all_by_project(self, db: Session, *, project_id: int) -> list[models.GeneratedOutline]:
        return db.query(self.model).filter(self.model.project_id == project_id).order_by(self.model.created_at.desc()).all()

generated_outline = CRUDGeneratedOutline(models.GeneratedOutline)

# CRUD for AIModel
class CRUDAIModel(CRUDBase[models.AIModel, schemas.AIModelCreate, schemas.AIModelUpdate]):
    def create(self, db: Session, *, obj_in: schemas.AIModelCreate) -> models.AIModel:
        db_obj = models.AIModel(
            name=obj_in.name,
            api_url=obj_in.api_url,
            api_key=encrypt_data(obj_in.api_key),
            model_name=obj_in.model_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: models.AIModel, obj_in: schemas.AIModelUpdate | Dict[str, Any]
    ) -> models.AIModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if "api_key" in update_data and update_data["api_key"]:
            update_data["api_key"] = encrypt_data(update_data["api_key"])
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)

ai_model = CRUDAIModel(models.AIModel)
