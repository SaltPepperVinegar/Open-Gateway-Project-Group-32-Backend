import os

import pytest
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app as real_app
from app.models.db.user import UserDocument


# Make anyio backend session-scoped so it matches your session-scoped fixtures
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    os.environ.setdefault("MONGO_DSN", "mongodb://localhost:27017/fastapi_db")
    client = AsyncIOMotorClient(os.environ["MONGO_DSN"])
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[UserDocument])
    yield
    await client.drop_database(db.name)


@pytest.fixture
async def aclient():
    transport = ASGITransport(app=real_app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
