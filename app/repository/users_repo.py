from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from app.models.db.user import UserDocument
from app.models.DTO.user import UserCreateDTO


async def create_user(user: UserCreateDTO) -> UserCreateDTO:
    user_doc = UserDocument(**user.model_dump())

    try:
        await user_doc.insert()
    except DuplicateKeyError as err:
        raise HTTPException(status_code=400, detail="uid already exists") from err

    return user
