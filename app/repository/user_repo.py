from pymongo.errors import DuplicateKeyError

from app.exceptions.user import UserAlreadyRegisteredError
from app.models.db.user import UserDocument
from app.models.DTO.user import UserCreateDTO


async def create_user(user: UserCreateDTO) -> UserCreateDTO:
    user_doc = UserDocument(**user.model_dump())

    try:
        await user_doc.insert()
    except DuplicateKeyError as err:
        raise UserAlreadyRegisteredError() from err

    return user
