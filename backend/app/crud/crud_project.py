from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectBase, ProjectCreate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectBase]):
    pass


project = CRUDProject(Project)
