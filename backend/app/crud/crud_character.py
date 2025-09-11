from typing import Any, Dict, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate

class CRUDCharacter(CRUDBase[Character, CharacterCreate, CharacterUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: Character,
        obj_in: Union[CharacterUpdate, Dict[str, Any]]
    ) -> Character:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                current_value = getattr(db_obj, field)
                # If the field is a dict (our JSONB fields), merge them
                if isinstance(current_value, dict) and isinstance(value, dict):
                    # Create a copy to ensure SQLAlchemy detects the change
                    merged_value = current_value.copy()
                    merged_value.update(value)
                    setattr(db_obj, field, merged_value)
                else:
                    setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

character = CRUDCharacter(Character)
