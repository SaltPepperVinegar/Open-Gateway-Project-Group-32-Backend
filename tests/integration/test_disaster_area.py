import pytest

from app.core.config import settings
from app.models.api.disaster_area import DisasterAreaCreateRes, DisasterAreaSearchRes
from app.models.embedded.enums import DisasterAreaStatus
from app.models.embedded.geo_json import GeoJSONPolygon
from tests.integration.utils import (
    api_get,
    api_patch,
    api_post,
    firebase_log_in_manually,
)

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


@pytest.mark.parametrize(
    "firebase_new_user",
    [{"email": settings.MANAGER_EMAILS[0], "password": "MyStrongPass123"}],
    indirect=True,
)
async def test_disaster_area_search(init_db, clean_db, init_firebase, firebase_log_in):
    payload = {"display_name": "Test Manager"}
    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    new_token = firebase_log_in_manually(settings.MANAGER_EMAILS[0], "MyStrongPass123")[
        "token"
    ]

    # Create 3 different disaster areas

    area_payload_1 = {
        "title": "Flooding in Downtown",
        "description": "Severe flash flooding reported in central business district.",
        "boundary": {
            "gid": "b6f4a892-19cd-4a32-901e-f45acb4dbe3f",
            "type": "Polygon",
            "coordinates": [[[10.1, 20.2], [11.3, 21.4], [12.5, 22.6], [10.1, 20.2]]],
        },
    }

    area_payload_2 = {
        "title": "Wildfire near National Park",
        "description": "Rapidly spreading wildfire detected at the park boundary.",
        "boundary": {
            "gid": "3a1b9c45-8a2f-48f8-9324-642c7912a1f9",
            "type": "Polygon",
            "coordinates": [[[30.5, 40.7], [31.8, 41.9], [32.0, 42.5], [30.5, 40.7]]],
        },
    }

    area_payload_3 = {
        "title": "Chemical Spill on Highway",
        "description": "Tanker truck overturned, releasing hazardous material across both lanes.",
        "boundary": {
            "gid": "e02f598a-84ef-4de0-9b4b-97830c9e77f6",
            "type": "Polygon",
            "coordinates": [[[50.2, 60.1], [51.3, 61.4], [52.5, 62.7], [50.2, 60.1]]],
        },
    }

    # Call disaster area create API endpoint for them to put them in database

    resp = await api_post("/api/v1/disaster_areas", area_payload_1, new_token)
    assert resp.status_code == 201, resp.text

    resp = await api_post("/api/v1/disaster_areas", area_payload_2, new_token)
    assert resp.status_code == 201, resp.text

    resp = await api_post("/api/v1/disaster_areas", area_payload_3, new_token)
    assert resp.status_code == 201, resp.text

    # Search with no status specified
    # Except three areas are found

    resp = await api_get("/api/v1/disaster_areas", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]

    assert len(disaster_areas) == 3

    # Search with status = ACTIVE
    # Also expect three areas are found (new created areas have active status as default)

    resp = await api_get("/api/v1/disaster_areas?status=active", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]

    assert len(disaster_areas) == 3

    searched_titles = [area.title for area in disaster_areas]
    assert area_payload_1["title"] in searched_titles
    assert area_payload_2["title"] in searched_titles
    assert area_payload_3["title"] in searched_titles

    # Search with status = RESOLVED
    # Expect no areas are found

    resp = await api_get("/api/v1/disaster_areas?status=resolved", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]

    assert len(disaster_areas) == 0

    # Search with status = DELETED
    # Also expect no areas are found

    resp = await api_get("/api/v1/disaster_areas?status=deleted", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]

    assert len(disaster_areas) == 0

    # Search with invalud status literal
    # Expect HTTP 422 unprocessable entity

    resp = await api_get("/api/v1/disaster_areas?status=invalid_state", new_token)
    assert resp.status_code == 422, resp.text


@pytest.mark.parametrize(
    "firebase_new_user",
    [{"email": settings.MANAGER_EMAILS[0], "password": "MyStrongPass123"}],
    indirect=True,
)
async def test_disaster_area_update(init_db, clean_db, init_firebase, firebase_log_in):
    payload = {"display_name": "Test Manager"}
    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    new_token = firebase_log_in_manually(settings.MANAGER_EMAILS[0], "MyStrongPass123")[
        "token"
    ]

    # Create 3 different disaster areas

    area_payload_1 = {
        "title": "Flooding in Downtown",
        "description": "Severe flash flooding reported in central business district.",
        "boundary": {
            "gid": "b6f4a892-19cd-4a32-901e-f45acb4dbe3f",
            "type": "Polygon",
            "coordinates": [[[10.1, 20.2], [11.3, 21.4], [12.5, 22.6], [10.1, 20.2]]],
        },
    }

    area_payload_2 = {
        "title": "Wildfire near National Park",
        "description": "Rapidly spreading wildfire detected at the park boundary.",
        "boundary": {
            "gid": "3a1b9c45-8a2f-48f8-9324-642c7912a1f9",
            "type": "Polygon",
            "coordinates": [[[30.5, 40.7], [31.8, 41.9], [32.0, 42.5], [30.5, 40.7]]],
        },
    }

    area_payload_3 = {
        "title": "Chemical Spill on Highway",
        "description": "Tanker truck overturned, releasing hazardous material across both lanes.",
        "boundary": {
            "gid": "e02f598a-84ef-4de0-9b4b-97830c9e77f6",
            "type": "Polygon",
            "coordinates": [[[50.2, 60.1], [51.3, 61.4], [52.5, 62.7], [50.2, 60.1]]],
        },
    }

    # Call disaster area create API endpoint for them to put them in database

    resp = await api_post("/api/v1/disaster_areas", area_payload_1, new_token)
    assert resp.status_code == 201, resp.text

    resp = await api_post("/api/v1/disaster_areas", area_payload_2, new_token)
    assert resp.status_code == 201, resp.text

    resp = await api_post("/api/v1/disaster_areas", area_payload_3, new_token)
    assert resp.status_code == 201, resp.text

    # Search all disaster areas

    resp = await api_get("/api/v1/disaster_areas", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]

    # Set "Flooding in Downtown" and "Chemical Spill on Highway" as resolved

    for area in disaster_areas:
        assert area.status == DisasterAreaStatus.ACTIVE
        assert area.resolved_at is None

        if (
            area.title == "Flooding in Downtown"
            or area.title == "Chemical Spill on Highway"
        ):
            resp = await api_patch(
                f"/api/v1/disaster_areas/{area.id}", {"status": "resolved"}, new_token
            )
            assert resp.status_code == 200, resp.text

    # Now search resolved areas and check if titles are correct

    resp = await api_get("/api/v1/disaster_areas?status=resolved", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]
    titles = [area.title for area in disaster_areas]

    assert len(disaster_areas) == 2
    assert "Flooding in Downtown" in titles
    assert "Chemical Spill on Highway" in titles
    assert disaster_areas[0].resolved_at is not None
    assert disaster_areas[1].resolved_at is not None

    # Now search areas remaining active and check if the title is correct

    resp = await api_get("/api/v1/disaster_areas?status=active", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]
    assert len(disaster_areas) == 1
    assert disaster_areas[0].title == "Wildfire near National Park"

    # Search all areas and update "Flooding in Downtown" as resolved

    resp = await api_get("/api/v1/disaster_areas", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]

    for area in disaster_areas:
        if area.title == "Flooding in Downtown":
            resp = await api_patch(
                f"/api/v1/disaster_areas/{area.id}", {"status": "active"}, new_token
            )
            assert resp.status_code == 200, resp.text
            break

    # Now search areas remaining active and check if the title and number of areas are correct

    resp = await api_get("/api/v1/disaster_areas?status=active", new_token)
    assert resp.status_code == 200, resp.text

    disaster_areas = [DisasterAreaSearchRes(**resp_dict) for resp_dict in resp.json()]
    titles = [area.title for area in disaster_areas]

    assert len(disaster_areas) == 2
    assert "Flooding in Downtown" in titles
    assert "Wildfire near National Park" in titles
    assert disaster_areas[0].resolved_at is None
    assert disaster_areas[1].resolved_at is None

    # Now try to trigger DisasterAreaDoesNotExistError
    resp = await api_patch(
        "/api/v1/disaster_areas/68ea69fabdff2a50b280809f",
        {"status": "resolved"},
        new_token,
    )
    assert resp.status_code == 404, resp.text

    # Now try to trigger InvalidObjectIDStringError
    resp = await api_patch(
        "/api/v1/disaster_areas/i-am-not-an-object-id-str",
        {"status": "resolved"},
        new_token,
    )
    assert resp.status_code == 400, resp.text
