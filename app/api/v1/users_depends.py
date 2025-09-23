from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from firebase_admin import auth



def get_decoded_token(token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=True))) -> Dict[str, Any]:
    try:
        decoded = auth.verify_id_token(token.credentials)
        return decoded
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )