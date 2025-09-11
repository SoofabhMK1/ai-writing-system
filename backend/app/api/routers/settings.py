from typing import Annotated, List, Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decrypt_data
from app.crud import crud_setting
from app.crud.base import CRUDBase
from app.database import get_db
from app.schemas import setting as setting_schemas

# Pydantic models
ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaInDBType = TypeVar("SchemaInDBType", bound=BaseModel)


def create_settings_router(
    *,
    crud_instance: CRUDBase,
    tag: str,
    prefix: str,
    response_model: Type[SchemaInDBType],
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
) -> APIRouter:
    """
    Generic factory to create an async CRUD router for a setting model.
    """
    router = APIRouter(prefix=prefix, tags=[tag])
    entity_name = tag.rstrip("s")

    @router.post("/", response_model=response_model)
    async def create_item(item_in: create_schema, db: Annotated[AsyncSession, Depends(get_db)]):
        return await crud_instance.create(db=db, obj_in=item_in)

    @router.get("/", response_model=List[response_model])
    async def read_items(
        db: Annotated[AsyncSession, Depends(get_db)], skip: int = 0, limit: int = 100
    ):
        return await crud_instance.get_multi(db, skip=skip, limit=limit)

    @router.put("/{item_id}", response_model=response_model)
    async def update_item(
        item_id: int, item_in: update_schema, db: Annotated[AsyncSession, Depends(get_db)]
    ):
        db_item = await crud_instance.get(db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{entity_name} not found")
        return await crud_instance.update(db=db, db_obj=db_item, obj_in=item_in)

    @router.delete("/{item_id}", response_model=response_model)
    async def delete_item(item_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
        db_item = await crud_instance.remove(db=db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{entity_name} not found")
        return db_item

    return router


# --- Create individual CRUD routers using the factory ---
worldview_router = create_settings_router(
    crud_instance=crud_setting.worldview,
    tag="Worldviews",
    prefix="/worldviews",
    response_model=setting_schemas.WorldviewInDB,
    create_schema=setting_schemas.WorldviewCreate,
    update_schema=setting_schemas.WorldviewBase,
)

writing_style_router = create_settings_router(
    crud_instance=crud_setting.writing_style,
    tag="Writing Styles",
    prefix="/writing-styles",
    response_model=setting_schemas.WritingStyleInDB,
    create_schema=setting_schemas.WritingStyleCreate,
    update_schema=setting_schemas.WritingStyleBase,
)

prompt_template_router = create_settings_router(
    crud_instance=crud_setting.prompt_template,
    tag="Prompt Templates",
    prefix="/prompt-templates",
    response_model=setting_schemas.PromptTemplateInDB,
    create_schema=setting_schemas.PromptTemplateCreate,
    update_schema=setting_schemas.PromptTemplateBase,
)

# --- AI Model has custom endpoints, so we create it separately ---
ai_model_router = create_settings_router(
    crud_instance=crud_setting.ai_model,
    tag="AI Models",
    prefix="/ai-models",
    response_model=setting_schemas.AIModelInDB,
    create_schema=setting_schemas.AIModelCreate,
    update_schema=setting_schemas.AIModelBase,
)


@ai_model_router.post("/{model_id}/test-connection")
async def test_ai_connection(model_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    from openai import AsyncOpenAI

    db_model = await crud_setting.ai_model.get(db, id=model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="AI Model not found")

    try:
        api_key_to_test = decrypt_data(db_model.api_key)
        client = AsyncOpenAI(
            base_url=db_model.api_url,
            api_key=api_key_to_test,
        )
        await client.models.list()
        return {"status": "success", "message": "连接成功"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"连接失败: {str(e)}"
        ) from e


# --- Generated Outline has a custom 'get_all_by_project' endpoint ---
generated_outline_router = APIRouter(
    prefix="/generated-outlines", tags=["Generated Outlines"]
)


@generated_outline_router.post("/", response_model=setting_schemas.GeneratedOutlineInDB)
async def create_generated_outline(
    outline_in: setting_schemas.GeneratedOutlineCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await crud_setting.generated_outline.create(db=db, obj_in=outline_in)


@generated_outline_router.get(
    "/project/{project_id}", response_model=List[setting_schemas.GeneratedOutlineInDB]
)
async def read_generated_outlines_for_project(
    project_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud_setting.generated_outline.get_all_by_project(
        db=db, project_id=project_id
    )


@generated_outline_router.delete(
    "/{outline_id}", response_model=setting_schemas.GeneratedOutlineInDB
)
async def delete_generated_outline(outline_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    db_outline = await crud_setting.generated_outline.remove(db=db, id=outline_id)
    if not db_outline:
        raise HTTPException(status_code=404, detail="Generated outline not found")
    return db_outline


# --- Combine all settings routers into a single main router ---
router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)
router.include_router(worldview_router)
router.include_router(writing_style_router)
router.include_router(prompt_template_router)
router.include_router(ai_model_router)
router.include_router(generated_outline_router)
