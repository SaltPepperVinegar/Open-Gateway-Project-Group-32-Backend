from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from app.models.base.user import UserBase, UserCreateBase, UserSearchBase
from app.models.db.user import UserDocument


async def create_user(user: UserCreateBase) -> UserCreateBase:
    user_doc = UserDocument(**user.model_dump())

    try:
        await user_doc.insert()
    except DuplicateKeyError as err:
        raise HTTPException(status_code=400, detail="uid already exists") from err

    return user


async def search_user(user: UserSearchBase) -> UserBase | None:
    pass
