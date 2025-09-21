from .api_token import get_token
from .config import POPULATION_DENSITY_DATA_SCOPE, POPULATION_DENSITY_DATA_URL
import requests
import time

access_token = None
expire_time = None


def population_density_data(payload=None):
    global access_token, expire_time

    if expire_time == None or expire_time < time.time():
        tokens = get_token(POPULATION_DENSITY_DATA_SCOPE)
        access_token = tokens["access_token"]
        expire_time = time.time() + tokens["expires_in"]

        print("access_token:", access_token[0:32])
        print("expire_time", expire_time)
    else:
        print(f"token still valid for {expire_time - time.time()}")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    if payload == None:
        payload = {
            "area": {
                "areaType": "POLYGON",
                "boundary": [
                    {"latitude": -37.8150, "longitude": 144.9630},
                    {"latitude": -37.8165, "longitude": 144.9690},
                    {"latitude": -37.8125, "longitude": 144.9710},
                ],
            },
            "precision": 10,
            "startTime": "2025-08-31T10:00:00Z",
            "endTime": "2025-08-31T10:01:00Z",
        }

    resp = requests.post(POPULATION_DENSITY_DATA_URL, headers=headers, json=payload, verify=False)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    data = resp.json()
    return data
