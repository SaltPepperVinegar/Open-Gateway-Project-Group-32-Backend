from .m2m_api_token import get_token
from .auth_code import get_auth_code
from .config import *
import requests


def population_density_data(payload = None):
    access_token = get_token(POPULATION_DENSITY_DATA_SCOPE)
    print("access_token:", access_token)


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
                        {"latitude": -37.8125, "longitude": 144.9710}
                        ]
                    },
                    "precision": 10,
                    "startTime": "2025-08-31T10:00:00Z",
                    "endTime":   "2025-08-31T10:01:00Z"
                  }     


    resp = requests.post(POPULATION_DENSITY_DATA_URL, headers=headers, json=payload, verify=False)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    data = resp.json()
    print(data)

    return data