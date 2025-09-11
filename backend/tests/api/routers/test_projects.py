import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db, Base
from app.schemas import ProjectCreate

# --- Test Database Setup ---
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# --- Pytest Fixtures ---
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create database tables before tests run, and drop them after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="module")
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


# --- Tests ---
@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    project_data = {"name": "Test Project", "description": "A test project"}
    response = await client.post("/api/v1/projects/", json=project_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["description"] == project_data["description"]
    assert "id" in data

@pytest.mark.asyncio
async def test_read_projects(client: AsyncClient):
    # First, create a project to ensure there's data
    project_data = {"name": "Another Test Project", "description": "Another one"}
    await client.post("/api/v1/projects/", json=project_data)

    response = await client.get("/api/v1/projects/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[-1]["name"] == project_data["name"]
