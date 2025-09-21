from fastapi import APIRouter, HTTPException
from app.models.api.user_req import CreateUserReq
from app.models.api.user_res import UserRes
from app.service.users_service import register_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRes, status_code=201)
async def create_user(req: CreateUserReq):
    try:
        return await register_user(req.username, req.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
