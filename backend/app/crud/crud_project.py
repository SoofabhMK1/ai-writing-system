from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectBase

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectBase]):
    pass

project = CRUDProject(Project)
