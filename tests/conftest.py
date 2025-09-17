import os
import tempfile
from unittest.mock import patch
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import get_async_db, get_db
from main import app
from models.user import Base


# Create temporary database file for testing
temp_db = tempfile.NamedTemporaryFile(delete=False)
temp_db.close()
TEST_DB_PATH = temp_db.name

SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
ASYNC_SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncTestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

def override_get_db():
    """Override synchronous database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

async def override_get_async_db():
    """Override asynchronous database dependency for testing."""
    async with AsyncTestingSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_async_db] = override_get_async_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Set up test database tables at the start of test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # Clean up temporary database file
    if os.path.exists(TEST_DB_PATH):
        os.unlink(TEST_DB_PATH)


@pytest.fixture(autouse=True)
def clean_database():
    yield
    db = TestingSessionLocal()
    try:
        # Delete all data from all tables in reverse order to handle foreign keys
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
    finally:
        db.close()


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
