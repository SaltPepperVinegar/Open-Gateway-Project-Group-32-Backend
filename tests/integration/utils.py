from httpx import ASGITransport, AsyncClient

from app.main import app


async def api_post(path, json_data, token=None):
    if token is None:
        headers = {}
    else:
        headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:

        response = await ac.post(path, json=json_data, headers=headers)
    return response


async def api_get(path, token=None):
    if token is None:
        headers = {}
    else:
        headers = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get(path, headers=headers)
    return response


async def api_patch(path, json_data, token=None):
    if token is None:
        headers = {}
    else:
        headers = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.patch(path, json=json_data, headers=headers)
    return response


async def api_delete(path, token=None):
    if token is None:
        headers = {}
    else:
        headers = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.delete(path, headers=headers)
    return response
