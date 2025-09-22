import pytest
from httpx import AsyncClient


@pytest.mark.anyio  # <-- use anyio here, not asyncio
async def test_health(aclient: AsyncClient):
    r = await aclient.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
