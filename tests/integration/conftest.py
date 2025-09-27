import json
from datetime import datetime

import firebase_admin
import httpx
import pytest
from beanie import init_beanie
from firebase_admin import credentials, get_app
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.main import DB_DOCUMENT_MODELS


@pytest.fixture(scope="function")
async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_DSN)

    await init_beanie(
        database=client[settings.DB_NAME_TEST], document_models=DB_DOCUMENT_MODELS
    )

    yield

    client.close()


@pytest.fixture(scope="function")
async def clean_db(init_db):
    pass


@pytest.fixture(scope="function")
def init_firebase():
    try:
        fb_app = get_app()
    except ValueError:
        cred = credentials.Certificate(json.loads(settings.FIREBASE_CRED))
        fb_app = firebase_admin.initialize_app(cred)

    return fb_app


@pytest.fixture(scope="function")
def firebase_new_user(request, init_firebase):
    """
    Create a temporary user in firebase for test.
    Email/password can be specified via request.param,
    otherwise generate default ones.
    """

    email = None
    password = None
    if hasattr(request, "param"):
        email = request.param.get("email")
        password = request.param.get("password")

    if not email:
        email = f"test_{datetime.now().timestamp()}@example.com"
    if not password:
        password = "password"

    user = firebase_admin.auth.create_user(email=email, password=password)

    yield {
        "uid": user.uid,
        "email": email,
        "password": password,
    }

    firebase_admin.auth.delete_user(user.uid)


@pytest.fixture(scope="function")
def firebase_log_in(firebase_new_user, init_firebase):
    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:signInWithPassword?key={
            json.loads(settings.FIREBASE_FRONTEND_CRED)['apiKey']
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

    yield {"uid": data["localId"], "token": data["idToken"]}
