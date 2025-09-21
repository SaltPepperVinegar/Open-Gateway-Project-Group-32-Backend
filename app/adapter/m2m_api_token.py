import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning

from .config import CLIENT_ID, CLIENT_SECRET, TOKEN_URL


def get_token(scope=None):

    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    data = {
        "grant_type": "client_credentials",
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
