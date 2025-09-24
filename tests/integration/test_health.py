import pytest
from httpx import AsyncClient
from utils import api_get

@pytest.mark.anyio  # <-- use anyio here, not asyncio
async def test_health():
    r = await api_get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
