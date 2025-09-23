from typing import Annotated, Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

security = HTTPBearer(auto_error=True)


def get_decoded_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> Dict[str, Any]:
    try:
        decoded = auth.verify_id_token(token.credentials)
        return decoded
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from err
