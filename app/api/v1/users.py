from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends

from app.models.api.user import UserRegisterReq, UserRegisterRes
from app.service.users_service import register_user_service
from app.api.v1.users_depends import get_decoded_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRegisterRes, status_code=201)
async def register_user(req: UserRegisterReq, decoded_token: Dict[str, Any] = Depends(get_decoded_token)) -> UserRegisterRes:
    try:
        return await register_user_service(req, decoded_token)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
