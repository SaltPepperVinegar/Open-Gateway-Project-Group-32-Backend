from app.repository.users_repo import create_user, get_user_by_username
from app.models.api.user_res import UserRes


async def register_user(username: str, email: str) -> UserRes:
    existing = await get_user_by_username(username)
    if existing:
        raise ValueError("Username already exists")
    saved = await create_user(username, email)
    return UserRes(id=str(saved.id), username=saved.username, email=saved.email)
