from datetime import datetime

import pytest

from app.models.api.user import UserRegisterRes
from app.models.embedded.enums import UserRole
from tests.integration.utils import api_post

pytestmark = pytest.mark.asyncio


async def test_user_register_default(init_db, clean_db, init_firebase, firebase_log_in):
    payload = {"display_name": "Test User"}

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
