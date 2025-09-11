import os, re, base64, hashlib, urllib.parse, warnings, requests
from urllib3.exceptions import InsecureRequestWarning
from .config import *

def get_token(scope = None):
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": "Yqp2jao1Ruc8UBwk7jwAIJ6Y1jsVT4qJHvQVpduK",  # add if client is confidential
    }

    if (scope != None):
        data["scope"] = scope

    # Only disable verification for this stub host (dev only)
    resp = requests.post(TOKEN_URL, data=data, verify=False)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    tokens = resp.json()
    return tokens["access_token"]
