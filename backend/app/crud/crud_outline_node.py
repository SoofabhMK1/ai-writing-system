# backend/app/crud/crud_outline_node.py
from sqlalchemy.orm import Session
from typing import List

from app.crud.base import CRUDBase
from app.models.outline_node import OutlineNode
from app.schemas.outline_node import OutlineNodeCreate, OutlineNodeBase

class CRUDOutlineNode(CRUDBase[OutlineNode, OutlineNodeCreate, OutlineNodeBase]):
    # 这里我们将添加专门为 OutlineNode 写的、非通用的数据库操作方法
    
    def get_all_by_project(self, db: Session, *, project_id: int) -> List[OutlineNode]:
        """
        获取一个项目下的所有大纲节点。
        为了构建树状结构，我们只获取根节点（parent_id is None），
        SQLAlchemy 的 relationship 会自动加载它们的 children。
        """
        return (
            db.query(self.model)
            .filter(OutlineNode.project_id == project_id, OutlineNode.parent_id.is_(None))
            .order_by(OutlineNode.node_order)
            .all()
        )

outline_node = CRUDOutlineNode(OutlineNode)
