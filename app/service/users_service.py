from passlib.hash import bcrypt

from app.models.api.user_req import UserCreateReq
from app.models.api.user_res import UserCreateRes
from app.models.db.user import UserDoc
from app.repository.users_repo import create_user, get_user_by_username


async def register_user(req: UserCreateReq) -> UserCreateRes:
    existing = await get_user_by_username(req.username)
    if existing:
        raise ValueError("Username already exists")
    hashed = bcrypt.hash(req.password)
    user_doc = UserDoc(username=req.username, email=req.email, password_hash=hashed)
    saved = await create_user(user_doc)
    return UserCreateRes(id=str(saved.id), username=saved.username, email=saved.email)
