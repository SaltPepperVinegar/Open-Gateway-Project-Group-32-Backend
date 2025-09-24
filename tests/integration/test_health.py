import pytest
from httpx import AsyncClient
from tests.integration.utils import *

pytestmark = pytest.mark.asyncio

async def test_health():
    r = await api_get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
