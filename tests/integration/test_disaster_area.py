import pytest

from app.core.config import settings
from app.models.api.disaster_area import DisasterAreaCreateRes
from app.models.embedded.enums import DisasterAreaStatus
from app.models.embedded.geo_json import GeoJSONPolygon
from tests.integration.utils import api_post, firebase_log_in_manually

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "firebase_new_user",
    [{"email": settings.MANAGER_EMAILS[0], "password": "MyStrongPass123"}],
    indirect=True,
)
async def test_manager_create_disaster_area(
    init_db, clean_db, init_firebase, firebase_log_in
):
    payload = {"display_name": "Test Manager"}
    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    # After signing up in firebase and accessing the user registration API,
    # a new token needs to be accessed to have the role claim.
    # Now this new token has claim "role: manager"
    new_token = firebase_log_in_manually(settings.MANAGER_EMAILS[0], "MyStrongPass123")[
        "token"
    ]

    # Let's start with a valid payload.
    payload = {
        "title": "Terrorist Attack",
        "description": "Ten terrorists with automatic rifle shown up in the bank",
        "boundary": {
            "gid": "d4ce2e97-6ba6-499d-b846-59329248ae21",
            "type": "Polygon",
            "coordinates": [
                [[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8], [1.1, 2.2]]
            ],
        },
    }

    resp = await api_post("/api/v1/disaster_areas", payload, new_token)
    assert resp.status_code == 201, resp.text

    resp = DisasterAreaCreateRes(**(resp.json()))

    assert isinstance(resp.id, str)
    assert len(resp.id) > 0
    assert resp.title == payload["title"]
    assert resp.description == payload["description"]
    assert resp.boundary == GeoJSONPolygon(**payload["boundary"])
    assert resp.status == DisasterAreaStatus.ACTIVE
    assert resp.resolved_at is None


@pytest.mark.parametrize(
    "firebase_new_user",
    [{"email": settings.MANAGER_EMAILS[0], "password": "MyStrongPass123"}],
    indirect=True,
)
async def test_manager_create_invalid_disaster_area(
    init_db, clean_db, init_firebase, firebase_log_in
):
    payload = {"display_name": "Test Manager"}
    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    # After sign-up in firebase and access the user registration API,
    # a new token needs to be accessed to have the role claim.
    # Now this new token has claim "role: manager"
    new_token = firebase_log_in_manually(settings.MANAGER_EMAILS[0], "MyStrongPass123")[
        "token"
    ]

    # Now try some invalid payloads.
    payload = {
        "title": "Kangaroo in the Road",
        "description": "Fifty kangaroos laying on the road preventing cars to go across.",
        "boundary": {
            "gid": "d4ce2e97-6ba6-499d-b846-59329248ae21",
            "type": "Polygon",
            "coordinates": [
                [
                    [1.1, 2.2],
                    [3.3, 4.4],
                    [5.5, 6.6],
                    [7.7, 8.8],
                    [1.1, 2.3],  # The ring does not enclose
                ]
            ],
        },
    }

    resp = await api_post("/api/v1/disaster_areas", payload, new_token)
    assert resp.status_code == 422, resp.text

    # One more
    payload = {
        "title": "Kangaroo in the Road",
        "description": "Fifty kangaroos laying on the road preventing cars to go across.",
        "boundary": {
            "gid": "d4ce2e97-6ba6-499d-b846-59329248ae21",
            "type": "Poopgon",  # Type literal doesnot match
            "coordinates": [
                [[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8], [1.1, 2.2]]
            ],
        },
    }

    resp = await api_post("/api/v1/disaster_areas", payload, new_token)
    assert resp.status_code == 422, resp.text

    # Last one
    payload = {
        "title": "Kangaroo in the Road",
        "description": "Fifty kangaroos laying on the road preventing cars to go across.",
        "boundary": {
            "gid": "d4ce2e97-6ba6-499d-b846-59329248ae21",
            "type": "Polygon",  # Type literal doesnot match
            "coordinates": [
                [[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8], [1.1, 2.2]],
                [
                    [0.1, 2.2],
                    [0.3, 4.4],
                    [0.5, 6.6],
                    [0.7, 8.8],
                    [0.1, 2.2],  # Two rings which is not allowed in this APP
                ],
            ],
        },
    }

    resp = await api_post("/api/v1/disaster_areas", payload, new_token)
    assert resp.status_code == 422, resp.text


@pytest.mark.parametrize(
    "firebase_new_user",
    [{"email": "worker_3@email.com", "password": "MyStrongPass123"}],
    indirect=True,
)
async def test_worker_tries_create_disaster_area(
    init_db, clean_db, init_firebase, firebase_log_in
):
    payload = {"display_name": "Test Worker"}
    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    # After sign-up in firebase and access the user registration API,
    # a new token needs to be accessed to have the role claim.
    # Now this new token has claim "role: manager"
    new_token = firebase_log_in_manually("worker_3@email.com", "MyStrongPass123")[
        "token"
    ]

    # The payload is valid.
    payload = {
        "title": "A Manager Attacked Me",
        "description": "He attacked me just now.",
        "boundary": {
            "gid": "d4ce2e97-6ba6-499d-b846-59329248ae21",
            "type": "Polygon",
            "coordinates": [
                [[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8], [1.1, 2.2]]
            ],
        },
    }

    resp = await api_post("/api/v1/disaster_areas", payload, new_token)
    assert resp.status_code == 403
    assert "Only managers can create a new disaster area." in resp.text
