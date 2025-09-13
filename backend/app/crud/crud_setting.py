from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import encrypt_data
from app.crud.base import CRUDBase
from app.models import setting as models
from app.schemas import setting as schemas


# CRUD for Worldview
class CRUDWorldview(
    CRUDBase[models.Worldview, schemas.WorldviewCreate, schemas.WorldviewBase]
):
    pass


worldview = CRUDWorldview(models.Worldview)


# CRUD for WritingStyle
class CRUDWritingStyle(
    CRUDBase[models.WritingStyle, schemas.WritingStyleCreate, schemas.WritingStyleBase]
):
    pass


writing_style = CRUDWritingStyle(models.WritingStyle)


# CRUD for PromptTemplate
class CRUDPromptTemplate(
    CRUDBase[
        models.PromptTemplate, schemas.PromptTemplateCreate, schemas.PromptTemplateBase
    ]
):
    pass


prompt_template = CRUDPromptTemplate(models.PromptTemplate)


# CRUD for GeneratedOutline
class CRUDGeneratedOutline(
    CRUDBase[
        models.GeneratedOutline,
        schemas.GeneratedOutlineCreate,
        schemas.GeneratedOutlineBase,
    ]
):
    async def get_all_by_project(
        self, db: AsyncSession, *, project_id: int
    ) -> List[models.GeneratedOutline]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.project_id == project_id)
            .order_by(self.model.created_at.desc())
        )
        return result.scalars().all()


generated_outline = CRUDGeneratedOutline(models.GeneratedOutline)


# CRUD for AIModel
class CRUDAIModel(CRUDBase[models.AIModel, schemas.AIModelCreate, schemas.AIModelBase]):
    async def create(
        self, db: AsyncSession, *, obj_in: schemas.AIModelCreate
    ) -> models.AIModel:
        db_obj = models.AIModel(
            name=obj_in.name,
            api_url=obj_in.api_url,
            api_key=encrypt_data(obj_in.api_key),
            model_name=obj_in.model_name,
            model_type=obj_in.model_type,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: models.AIModel,
        obj_in: schemas.AIModelBase | Dict[str, Any],
    ) -> models.AIModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "api_key" in update_data and update_data["api_key"]:
            update_data["api_key"] = encrypt_data(update_data["api_key"])

        return await super().update(db, db_obj=db_obj, obj_in=update_data)


ai_model = CRUDAIModel(models.AIModel)
