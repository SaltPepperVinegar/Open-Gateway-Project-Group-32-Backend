# tests/integration/test_users_api.py
import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_user_happy_path(aclient: AsyncClient):
    payload = {
        "username": "alex",
        "email": "alex@example.org",
        "password": "StrongP@ss",
        "role": "worker",
    }
    r = await aclient.post("/api/v1/users", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    body = r.json()
    assert body["username"] == "alex"
    assert "id" in body
