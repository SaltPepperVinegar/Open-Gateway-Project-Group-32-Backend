from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException

from app.models.base.user import UserCreateBase, UserSearchBase, UserBase
from app.models.db.user import UserDocument

async def create_user(user: UserCreateBase) -> UserCreateBase:
    user_doc = UserDocument(**user.model_dump())

    try:
        await user_doc.insert()
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="uid already exists")

    return user


async def search_user(user: UserSearchBase) -> UserBase | None:
    pass
