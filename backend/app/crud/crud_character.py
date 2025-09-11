from app.crud.base import CRUDBase
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate


class CRUDCharacter(CRUDBase[Character, CharacterCreate, CharacterUpdate]):
    pass


character = CRUDCharacter(Character)
