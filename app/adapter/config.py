# --- CONFIG ---
REALM_BASE = "https://poochie.example.com/auth/realms/operator"
CLIENT_ID = "developer-client"
CLIENT_SECRET = "Yqp2jao1Ruc8UBwk7jwAIJ6Y1jsVT4qJHvQVpduK"
REDIRECT_URI = "http://localhost:8080/callback"
USERNAME = "rex@poochie.dog"
PASSWORD = "password"

STUB_HOST = "poochie.example.com"

TOKEN_URL = "https://poochie.example.com/auth/realms/operator/protocol/openid-connect/token"


NUMBER_VERFICATION_URL = "https://poochie.example.com/camara/number-verification/v1/verify"
NUMBER_VERFICATION_SCOPE = "openid number-verification:verify"

REGION_DEVICE_COUNT_URL = "https://poochie.example.com/camara/region-device-count/v2/count"
REGION_DEVICE_COUNT_SCOPE = "region-device-count"

POPULATION_DENSITY_DATA_URL = (
    "https://poochie.example.com/camara/population-density-data/v2/retrieve"
)
POPULATION_DENSITY_DATA_SCOPE = "population-density-data:read"
