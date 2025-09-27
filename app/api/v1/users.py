from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends

from app.api.v1.users_depends import get_decoded_token
from app.models.api.user import UserRegisterReq, UserRegisterRes
from app.service.user_service import register_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRegisterRes, status_code=201)
async def register_user(
    req: UserRegisterReq,
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)],
) -> UserRegisterRes:
    return await register_user_service(req, decoded_token)
