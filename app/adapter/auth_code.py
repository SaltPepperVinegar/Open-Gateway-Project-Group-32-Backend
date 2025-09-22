import urllib.parse
import warnings

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

from .config import CLIENT_ID, PASSWORD, REALM_BASE, REDIRECT_URI, USERNAME


def get_auth_code(scope: str) -> str:
    session = requests.Session()

    # --- safety: only suppress TLS warnings for stub host we explicitly bypass ---
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    # --- Build a REAL auth_url (fixes MissingSchema) ---
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": scope,
    }

    auth_url = f"{REALM_BASE}/protocol/openid-connect/auth?{urllib.parse.urlencode(params)}"
    print(auth_url)
    # 1) Start flow: land on Keycloak login form
    r = session.get(auth_url, allow_redirects=True, verify=False)

    soup = BeautifulSoup(r.text, "html.parser")
    form = soup.find("form")
    if form is None:
        raise RuntimeError("Login form not found (are you already logged in?)")

    action = urllib.parse.urljoin(r.url, form.get("action"))  # type: ignore

    inputs = {i.get("name"): i.get("value", "") for i in form.find_all("input") if i.get("name")}  # type: ignore

    # Fill username/password (Keycloak uses 'username' + 'password' normally)
    inputs["username"] = (
        USERNAME if "username" in inputs or "login" not in inputs else inputs["login"]
    )
    inputs["password"] = PASSWORD

    # 2) Submit credentials BUT do NOT follow redirects (prevents hitting localhost)
    resp = session.post(action, data=inputs, allow_redirects=False, verify=False)
    print(resp.headers)

    loc = urllib.parse.urljoin(resp.request.url, resp.headers["Location"])  # type: ignore

    if loc.startswith(REDIRECT_URI):  # type: ignore
        q = urllib.parse.urlparse(loc).query  # type: ignore

        auth_code = urllib.parse.parse_qs(q).get("code", [None])[0]  # type: ignore

    if not auth_code:
        raise RuntimeError("Could not capture authorization code before redirecting to localhost.")
    session.close()
    return auth_code  # type: ignore
