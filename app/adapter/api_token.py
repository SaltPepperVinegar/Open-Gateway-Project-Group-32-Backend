import os, re, base64, hashlib, urllib.parse, warnings, requests
from urllib3.exceptions import InsecureRequestWarning
from .config import *
from .auth_code import get_auth_code


def get_token(scope=None):
    auth_code = get_auth_code(scope)

    print(auth_code)

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    if scope != None:
        data["scope"] = scope

    # Only disable verification for this stub host (dev only)
    resp = requests.post(TOKEN_URL, data=data, verify=False)
    # print(resp.status_code, resp.text)
    resp.raise_for_status()
    tokens = resp.json()
    return tokens
