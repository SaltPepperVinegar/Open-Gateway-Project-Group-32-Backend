from datetime import datetime

import pytest

from app.core.config import settings
from app.models.api.user import UserProfileRes, UserRegisterRes
from app.models.embedded.enums import UserRole
from tests.integration.utils import api_get, api_post

pytestmark = pytest.mark.asyncio


async def test_user_register_worker(init_db, clean_db, init_firebase, firebase_log_in):
    """
    Regist a new user with common email.
    Test if the user can be correctly assigned worker role
    and profile can be correctly created.
    """

    payload = {"display_name": "Test Worker User"}

    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    data = resp.json()

    user_res = UserRegisterRes(**data)

    assert user_res.uid == firebase_log_in["uid"]
    assert user_res.display_name == payload["display_name"]
    assert "@" in user_res.email
    assert user_res.role in UserRole
    assert user_res.role == UserRole.WORKER
    assert isinstance(user_res.created_at, datetime)
    assert isinstance(user_res.updated_at, datetime)


@pytest.mark.parametrize(
    "firebase_new_user",
    [{"email": settings.MANAGER_EMAILS[0], "password": "MyStrongPass123"}],
    indirect=True,
)
async def test_user_register_manager(init_db, clean_db, init_firebase, firebase_log_in):
    """
    Regist a new user with manager email.
    Test if the manager user profile can be correctly created.
    """

    payload = {"display_name": "Test Manager User"}

    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    data = resp.json()

    user_res = UserRegisterRes(**data)

    assert user_res.uid == firebase_log_in["uid"]
    assert user_res.display_name == payload["display_name"]
    assert "@" in user_res.email
    assert user_res.role in UserRole
    assert user_res.role == UserRole.MANAGER
    assert isinstance(user_res.created_at, datetime)
    assert isinstance(user_res.updated_at, datetime)


async def test_retrieve_user_profile(init_db, clean_db, init_firebase, firebase_log_in):
    """
    Test if user data can be correctly retrieved.
    """

    # Regist a new user first

    payload = {"display_name": "Test User"}
    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    # Retrieve user profile through /api/v1/users/profile endpoint

    resp = await api_get("/api/v1/users/profile", firebase_log_in["token"])
    assert resp.status_code == 200, resp.text

    retrieved_user_profile = UserProfileRes(**resp.json())

    assert retrieved_user_profile.uid == firebase_log_in["uid"]
    assert retrieved_user_profile.display_name == payload["display_name"]
    assert "@" in retrieved_user_profile.email
    assert retrieved_user_profile.role in UserRole
    assert retrieved_user_profile.role == UserRole.WORKER
    assert isinstance(retrieved_user_profile.created_at, datetime)
    assert isinstance(retrieved_user_profile.updated_at, datetime)
