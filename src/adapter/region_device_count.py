from .m2m_api_token import get_token
from .auth_code import get_auth_code
from .config import *
import requests


def region_device_count(payload = None):
    auth_code = get_auth_code(REGION_DEVICE_COUNT_SCOPE)
    print(auth_code)
    access_token = get_token(auth_code, REGION_DEVICE_COUNT_SCOPE)
    print("access_token:", access_token)


    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    if payload == None:
        payload = {
                    "area": {
                        "areaType": "CIRCLE",
                        "center": { "latitude": -37.8136, "longitude": 144.9631 },
                        "radius": 0.0000000000000000000000000000000000000000000001
                    },
                    "filter": { "deviceType": ["human device"] }
                  }       


    resp = requests.post(REGION_DEVICE_COUNT_URL, headers=headers, json=payload, verify=False)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    data = resp.json()
    print(data)

    return data