from app.crud.base import CRUDBase
from app.models.prompt_preset import PromptPreset
from app.schemas.prompt_preset import PromptPresetCreate, PromptPresetUpdate

class CRUDPromptPreset(CRUDBase[PromptPreset, PromptPresetCreate, PromptPresetUpdate]):
    pass

prompt_preset = CRUDPromptPreset(PromptPreset)
