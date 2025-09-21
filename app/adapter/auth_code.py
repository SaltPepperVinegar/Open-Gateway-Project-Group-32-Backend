# app/adapter/auth_code.py
from __future__ import annotations

import urllib.parse
import warnings
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib3.exceptions import InsecureRequestWarning

from .config import CLIENT_ID, PASSWORD, REALM_BASE, REDIRECT_URI, USERNAME


def _as_tag(node: Tag | NavigableString | None) -> Optional[Tag]:
    return node if isinstance(node, Tag) else None


def get_auth_code(scope: str) -> str:
    session = requests.Session()

    # Only suppress TLS warnings for this scripted flow
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    # Build OIDC auth URL
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": scope,
    }
    auth_url = (
        f"{REALM_BASE}/protocol/openid-connect/auth?{urllib.parse.urlencode(params)}"
    )

    # 1) Land on Keycloak login form
    r = session.get(auth_url, allow_redirects=True, verify=False)

    soup = BeautifulSoup(r.text, "html.parser")
    form = _as_tag(soup.find("form"))
    if form is None:
        raise RuntimeError("Login form not found (are you already logged in?)")

    # Resolve action against the current response URL
    action_attr: Optional[str] = form.get("action")
    action: str = urllib.parse.urljoin(r.url, action_attr or "")

    # Collect inputs safely (Tag-only, guard names/values)
    inputs: Dict[str, str] = {}
    for el in form.find_all("input"):
        if not isinstance(el, Tag):
            continue
        name = el.get("name")
        if not name:
            continue
        inputs[name] = el.get("value") or ""

    # Fill username/password
    if "username" in inputs or "login" not in inputs:
        inputs["username"] = USERNAME
    else:
        # Some Keycloak themes use 'login' instead of 'username'
        inputs["login"] = USERNAME
    inputs["password"] = PASSWORD

    # 2) Submit credentials without following redirects
    resp = session.post(action, data=inputs, allow_redirects=False, verify=False)

    # Safely read Location
    location_header: Optional[str] = resp.headers.get("Location")
    if not location_header:
        session.close()
        raise RuntimeError("No redirect Location returned after login submit.")

    # Absolute redirect URL
    loc: str = urllib.parse.urljoin(resp.request.url, location_header)

    auth_code: Optional[str] = None
    if loc.startswith(REDIRECT_URI):
        q = urllib.parse.urlparse(loc).query
        qs: Dict[str, List[str]] = urllib.parse.parse_qs(q)
        code_list = qs.get("code")
        if code_list:
            auth_code = code_list[0]

    session.close()

    if auth_code is None:
        raise RuntimeError(
            "Could not capture authorization code before redirecting to localhost."
        )

    return auth_code
