from .m2m_api_token import get_token
from .config import *
import requests
import time     

access_token = None
expire_time = None

def region_device_count(payload = None):
    global access_token, expire_time

    if expire_time == None or expire_time < time.time():
        tokens = get_token(REGION_DEVICE_COUNT_SCOPE)
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
    return data