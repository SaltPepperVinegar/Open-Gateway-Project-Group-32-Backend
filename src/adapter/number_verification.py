from .m2m_api_token import get_token
from .auth_code import get_auth_code
from .config import *
import requests
import json

def number_verification(number = "+61412345678"):
    access_token = get_token(NUMBER_VERFICATION_SCOPE)
    print("access_token:", access_token)


    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "phoneNumber": number,
    }

    resp = requests.post(NUMBER_VERFICATION_URL, headers=headers, json=payload, verify=False)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    data = resp.json()
    print(data)

    return data



