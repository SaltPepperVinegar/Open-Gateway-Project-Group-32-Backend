from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.users_depends import get_decoded_token
from app.exceptions.user import UserAlreadyRegisteredError, UserDoesNotExistError
from app.models.api.user import UserRegisterReq, UserRegisterRes, UserProfileRes, UserSearchQueryParam
from app.service.user_service import register_user_service, retrieve_user_profile_service, search_users_service

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


@router.get("", response_model=List[UserProfileRes], status_code=200)
async def search_users(
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)],
    query_params: UserSearchQueryParam = Depends()
) -> List[UserProfileRes]:
    return await search_users_service(query_params)


@router.get("profile", response_model=UserProfileRes, status_code=200)
async def retrieve_user_profile(
    decoded_token: Annotated[Dict[str, Any], Depends(get_decoded_token)]
) -> UserProfileRes:
    try:
        return await retrieve_user_profile_service(decoded_token)
    except UserDoesNotExistError as err:
        raise HTTPException(status_code=404, detail=err.message) from err