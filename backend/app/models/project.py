from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True,nullable=False)
    description = Column(Text,nullable=False)