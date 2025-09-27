from typing import Dict, Any
import json

from httpx import ASGITransport, AsyncClient
import httpx

from app.main import app
from app.core.config import settings


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


def firebase_log_in_manually(
        email: str, password: str
) -> Dict[str, Any]:
    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:signInWithPassword?key={
            json.loads(settings.FIREBASE_FRONTEND_CRED)['apiKey']
        }"
    )

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }

    with httpx.Client() as client:
        r = client.post(url, json=payload)

    if r.status_code != 200:
        raise Exception(r.status_code, r.json().get("error", {}))

    data = r.json()

    return {"uid": data["localId"], "token": data["idToken"]}