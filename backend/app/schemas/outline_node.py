from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.outline_node import NodeStatus

class OutlineNodeBase(BaseModel):
    title: Optional[str] = None
    content_brief: Optional[str] = None
    generated_content: Optional[str] = None
    word_count_target: Optional[int] = None
    status: Optional[NodeStatus] = None
    node_order: Optional[int] = None

class OutlineNodeCreate(BaseModel):
    title: str = Field(..., min_length=1)
    project_id: int
    parent_id: Optional[int] = None

class OutlineNode(OutlineNodeBase):
    id: int
    project_id: int
    parent_id: Optional[int] = None
    children: List['OutlineNode'] = []

    class Config:
        from_attributes = True
