from fastapi import APIRouter, HTTPException

from app.models.api.user_req import UserCreateReq
from app.models.api.user_res import UserCreateRes
from app.service.users_service import register_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserCreateRes, status_code=201)
async def create_user(req: UserCreateReq) -> UserCreateRes:
    try:
        return await register_user(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
