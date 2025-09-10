from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from database import get_db
import pytest
import pytest_asyncio
from httpx import AsyncClient
from models.user import Base
from unittest.mock import patch


# Test database setup - use in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.fixture(autouse=True)
def mock_redis():
    with patch("database.redis_client.get") as mock_get, \
         patch("database.redis_client.set") as mock_set, \
         patch("database.redis_client.delete") as mock_delete:

        mock_get.return_value = None
        mock_set.return_value = True

        yield {
            "get": mock_get,
            "set": mock_set,
            "delete": mock_delete,
        }



