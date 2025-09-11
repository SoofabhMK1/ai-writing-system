from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    book_title: Optional[str] = None
    core_concept: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True
