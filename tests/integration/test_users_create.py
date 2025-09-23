# tests/integration/test_users_api.py
import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_user_happy_path(aclient: AsyncClient):
    assert True