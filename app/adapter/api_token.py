import requests

from .auth_code import get_auth_code
from .config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_URL


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

    if scope is not None:
        data["scope"] = scope

    # Only disable verification for this stub host (dev only)
    resp = requests.post(TOKEN_URL, data=data, verify=False)
    # print(resp.status_code, resp.text)
    resp.raise_for_status()
    tokens = resp.json()
    return tokens
