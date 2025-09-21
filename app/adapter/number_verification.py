import time

import requests

from .config import NUMBER_VERFICATION_SCOPE, NUMBER_VERFICATION_URL
from .m2m_api_token import get_token

access_token = None
expire_time = None


def number_verification(payload=None):
    global access_token, expire_time

    if expire_time is None or expire_time < time.time():
        tokens = get_token(NUMBER_VERFICATION_SCOPE)
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

    if payload is None:
        payload = {
            "phoneNumber": "+61412345678",
        }

    resp = requests.post(NUMBER_VERFICATION_URL, headers=headers, json=payload, verify=False)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    data = resp.json()
    return data
