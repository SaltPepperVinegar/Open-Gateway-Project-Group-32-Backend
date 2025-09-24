import pytest

from tests.integration.utils import api_get

pytestmark = pytest.mark.asyncio


async def test_health():
    r = await api_get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
