from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.users_depends import get_decoded_token
from app.exceptions.user import UserAlreadyRegisteredError
from app.models.api.user import UserRegisterReq, UserRegisterRes, VerifyTokenRes
from app.service.user_service import register_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRegisterRes, status_code=201)
async def register_user(
    req: UserRegisterReq,
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)],
) -> UserRegisterRes:
    try:
        return await register_user_service(req, decoded_token)
    except UserAlreadyRegisteredError as err:
        raise HTTPException(status_code=400, detail=err.message) from err


@router.get("/verify-token", response_model=VerifyTokenRes)
async def verify_token(
    _: Annotated[Dict[str, Any], Depends(get_decoded_token)],
) -> VerifyTokenRes:

    return VerifyTokenRes(is_valid=True)