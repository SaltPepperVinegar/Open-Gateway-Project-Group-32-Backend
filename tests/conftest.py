import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.users import router as users_router


@pytest.fixture(scope="session")
def app():
    app = FastAPI()
    app.include_router(users_router)
    return app


@pytest.fixture()
def client(app):
    return TestClient(app)
