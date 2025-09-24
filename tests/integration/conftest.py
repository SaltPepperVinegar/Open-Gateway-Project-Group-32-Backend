import os
import httpx
from datetime import datetime
import json

import pytest
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from firebase_admin import credentials, get_app
import firebase_admin

from app.main import app
from app.models.db.user import UserDocument
from app.core.config import settings


DB_DOCUMENT_MODELS = [UserDocument]


@pytest.fixture(scope="session")
def test_app():
    # Set a special lifespan function for test app.
    async def lifespan_test(app: FastAPI):
        # Setup test db
        db_client = AsyncIOMotorClient(settings.MONGO_DSN)
        db = db_client.get_database(settings.DB_NAME_TEST)
        await init_beanie(database=db, document_models=DB_DOCUMENT_MODELS)
        app.state.mongo_client = db_client
        app.state.db = db

        # Authorize firebase services
        try:
            fb_app = get_app()  # Reuse Firebase instance if exists
        except ValueError:
            cred = credentials.Certificate(settings.FIREBASE_CRED_PATH)
            fb_app = firebase_admin.initialize_app(cred)

        app.state.firebase_app = fb_app

        try:
            yield
        finally:
            db_client.close()
    
    app.router.lifespan_context = lifespan_test
    app.title = settings.APP_NAME_TEST

    return app


@pytest.fixture(scope="function")
async def async_client(test_app):
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture(scope="function")
async def clean_db(test_app):
    yield

    for model in DB_DOCUMENT_MODELS:
        await model.get_motor_collection().delete_many({})


@pytest.fixture(scope="function")
def firebase_new_user(test_app):
    """
    Create a temporary user in firebase for test.
    The associated email is a timestamp.
    The user will be deleted in teardown of the fixture.
    """
    
    user = firebase_admin.auth.create_user(
        email=f"test_{datetime.now().timestamp()}@example.com",
        password="password"
    )

    yield {
        "uid": user.uid,
        "email": user.email,
        "password": "password"
    }

    firebase_admin.auth.delete_user(user.uid)


@pytest.fixture(scope="function")
def firebase_log_in(firebase_new_user):
    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:signInWithPassword?key={
            json.loads(settings.FIREBASE_FRONTEND_CERTIFICATE_JSON)['apiKey']
        }"
    )

    payload = {
        "email": firebase_new_user["email"],
        "password": firebase_new_user["password"],
        "returnSecureToken": True,
    }

    with httpx.Client() as client:
        r = client.post(url, json=payload)

    if r.status_code != 200:
        raise Exception(r.status_code, r.json().get("error", {}))

    data = r.json()

    yield {
        "uid": data["localId"],
        "token": data["idToken"]
    }