from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# 1. 使用 create_async_engine 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 2. 创建异步会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


# 3. 使用新的声明式基类 (SQLAlchemy 2.0 推荐)
class Base(DeclarativeBase):
    pass


# 4. 创建异步的数据库会话依赖项
async def get_db():
    """
    FastAPI dependency that provides an async database session.
    """
    async with SessionLocal() as session:
        yield session
