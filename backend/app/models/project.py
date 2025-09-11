from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    book_title = Column(String, nullable=True)
    core_concept = Column(Text, nullable=True)
