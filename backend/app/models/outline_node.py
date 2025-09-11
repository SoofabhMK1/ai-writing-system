import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class NodeStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class OutlineNode(Base):
    __tablename__ = "outline_nodes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, default="新节点")

    content_brief = Column(Text, nullable=True, comment="内容蓝图/写作指令")
    generated_content = Column(
        Text, nullable=True, comment="AI生成或用户最终编辑的内容"
    )
    word_count_target = Column(Integer, default=0, comment="目标字数")
    status = Column(
        Enum(NodeStatus), default=NodeStatus.TODO, nullable=False, comment="节点状态"
    )

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    parent_id = Column(
        Integer, ForeignKey("outline_nodes.id"), nullable=True, index=True
    )

    node_order = Column(Integer, default=0, nullable=False, comment="排序字段")

    children = relationship(
        "OutlineNode", back_populates="parent", cascade="all, delete-orphan"
    )
    parent = relationship("OutlineNode", back_populates="children", remote_side=[id])
