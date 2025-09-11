from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.outline_node import OutlineNode
from app.schemas.outline_node import OutlineNodeBase, OutlineNodeCreate


class CRUDOutlineNode(CRUDBase[OutlineNode, OutlineNodeCreate, OutlineNodeBase]):
    async def get_all_by_project(
        self, db: AsyncSession, *, project_id: int
    ) -> List[OutlineNode]:
        """
        获取一个项目下的所有大纲节点。
        为了构建树状结构，我们只获取根节点（parent_id is None），
        并使用 selectinload 预加载所有的 children，以避免 N+1 查询问题。
        """
        result = await db.execute(
            select(self.model)
            .filter(
                OutlineNode.project_id == project_id, OutlineNode.parent_id.is_(None)
            )
            .order_by(OutlineNode.node_order)
            .options(selectinload(self.model.children))  # Eagerly load children
        )
        return result.scalars().all()


outline_node = CRUDOutlineNode(OutlineNode)
