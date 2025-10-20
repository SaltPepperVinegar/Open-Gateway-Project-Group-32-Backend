from datetime import datetime

import pytest

from app.models.api.survivor_report import (
    SurvivorReportCreateRes,
    SurvivorReportRetrieveRes,
)
from tests.integration.utils import api_get, api_post, firebase_log_in_manually

pytestmark = pytest.mark.asyncio


async def test_submit_survivor_report(init_db, clean_db):
    # Test fully specified payload

    payload_1 = {
        "title": "Injured person found",
        "description": "One injured adult found near the collapsed building.",
        "level": "high",
        "location": {
            "gid": "abc-123",
            "type": "Point",
            "coordinates": [144.9631, -37.8136],
        },
        "address": "123 Main St, Melbourne",
    }

    resp = await api_post("/api/v1/survivor_reports", payload_1)
    assert resp.status_code == 201, resp.text

    resp_model = SurvivorReportCreateRes(**resp.json())

    assert len(resp_model.id) > 0
    assert resp_model.title == payload_1["title"]
    assert resp_model.description == payload_1["description"]
    assert resp_model.level.value == payload_1["level"]
    assert resp_model.location.gid == payload_1["location"]["gid"]
    assert resp_model.location.type == payload_1["location"]["type"]
    assert resp_model.location.coordinates == payload_1["location"]["coordinates"]
    assert resp_model.address == payload_1["address"]
    assert isinstance(resp_model.created_at, datetime)

    # Test payload with necessary field specified

    payload_2 = {"location": {"type": "Point", "coordinates": [151.2093, -33.8688]}}

    resp = await api_post("/api/v1/survivor_reports", payload_2)
    assert resp.status_code == 201, resp.text

    resp_model = SurvivorReportCreateRes(**resp.json())

    assert len(resp_model.id) > 0
    assert resp_model.title is None
    assert resp_model.description is None
    assert resp_model.level is None
    assert resp_model.location.gid is None
    assert resp_model.location.type == payload_2["location"]["type"]
    assert resp_model.location.coordinates == payload_2["location"]["coordinates"]
    assert resp_model.address is None
    assert isinstance(resp_model.created_at, datetime)

    # Test payload with incorrect location triggering 422 error

    payload_3 = {
        "title": "Invalid point format",
        "location": {"type": "Point", "coordinates": [120.99]},
    }

    resp = await api_post("/api/v1/survivor_reports", payload_3)
    assert resp.status_code == 422, resp.text


@pytest.mark.parametrize(
    "firebase_new_user",
    [{"email": "some_worker@email.com", "password": "yeegeewowleegiao"}],
    indirect=True,
)
async def test_retrieve_all_survivor_report(
    init_db, clean_db, init_firebase, firebase_log_in
):
    payload = {"display_name": "Test Worker"}
    resp = await api_post("/api/v1/users", payload, firebase_log_in["token"])
    assert resp.status_code == 201, resp.text

    new_token = firebase_log_in_manually("some_worker@email.com", "yeegeewowleegiao")[
        "token"
    ]

    # Submit one payload and check if retrieved record count is 1

    payload_1 = {
        "title": "Injured person found",
        "description": "One injured adult found near the collapsed building.",
        "level": "high",
        "location": {
            "gid": "abc-123",
            "type": "Point",
            "coordinates": [144.9631, -37.8136],
        },
        "address": "123 Main St, Melbourne",
    }

    resp = await api_post("/api/v1/survivor_reports", payload_1)
    assert resp.status_code == 201, resp.text

    resp = await api_get("/api/v1/survivor_reports", new_token)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 1

    # Submit another payload and check if retrieve 2 records

    payload_2 = {
        "title": "Survivor spotted on rooftop",
        "description": None,
        "level": "medium",
        "location": {"gid": None, "type": "Point", "coordinates": [138.6007, -34.9285]},
        "address": None,
    }

    resp = await api_post("/api/v1/survivor_reports", payload_2)
    assert resp.status_code == 201, resp.text

    resp = await api_get("/api/v1/survivor_reports", new_token)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 2

    # Submit one more payload and check if retrieve 3 records

    payload_3 = {
        "title": "Group of survivors",
        "description": "Three people waving for help on balcony.",
        "location": {"type": "Point", "coordinates": [153.0260, -27.4705]},
        "address": "",
    }

    resp = await api_post("/api/v1/survivor_reports", payload_3)
    assert resp.status_code == 201, resp.text

    resp = await api_get("/api/v1/survivor_reports", new_token)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 3

    resp_model_list = [SurvivorReportRetrieveRes(**resp) for resp in resp.json()]

    for resp_model in resp_model_list:
        if resp_model.title == payload_1["title"]:
            resp_model_1 = resp_model
        elif resp_model.title == payload_2["title"]:
            resp_model_2 = resp_model
        elif resp_model.title == payload_3["title"]:
            resp_model_3 = resp_model

    # Ensure correctness of retrieved models

    # Check response of payload 1
    assert len(resp_model_1.id) > 0
    assert resp_model_1.title == payload_1["title"]
    assert resp_model_1.description == payload_1["description"]
    assert resp_model_1.level.value == payload_1["level"]
    assert resp_model_1.location.gid == payload_1["location"]["gid"]
    assert resp_model_1.location.type == payload_1["location"]["type"]
    assert resp_model_1.location.coordinates == payload_1["location"]["coordinates"]
    assert resp_model_1.address == payload_1["address"]
    assert isinstance(resp_model_1.created_at, datetime)

    # Check response of payloads 2
    assert len(resp_model_2.id) > 0
    assert resp_model_2.title == payload_2["title"]
    assert resp_model_2.description is None
    assert resp_model_2.level.value == payload_2["level"]
    assert resp_model_2.location.gid is None
    assert resp_model_2.location.type == payload_2["location"]["type"]
    assert resp_model_2.location.coordinates == payload_2["location"]["coordinates"]
    assert resp_model_2.address is None
    assert isinstance(resp_model_2.created_at, datetime)

    # Check response of payload 3
    assert len(resp_model_3.id) > 0
    assert resp_model_3.title == payload_3["title"]
    assert resp_model_3.description == payload_3["description"]
    assert resp_model_3.level is None
    assert resp_model_3.location.gid is None
    assert resp_model_3.location.type == payload_3["location"]["type"]
    assert resp_model_3.location.coordinates == payload_3["location"]["coordinates"]
    assert resp_model_3.address == payload_3["address"]
    assert isinstance(resp_model_3.created_at, datetime)
