from pymongo.errors import DuplicateKeyError

from app.exceptions.user import UserAlreadyRegisteredError, UserDoesNotExistError
from app.models.db.user import UserDocument
from app.models.DTO.user import UserCreateDTO, UserDTO


async def create_user(user: UserCreateDTO) -> UserCreateDTO:
    """
    Insert a new user document into user collection.
    Raise UserAlreadyRegisteredError when inserting duplicated UID or email.
    """

    user_doc = UserDocument(**user.model_dump())

    try:
        await user_doc.insert()
    except DuplicateKeyError as err:
        raise UserAlreadyRegisteredError() from err

    return user


async def retrieve_user_profile(uid: str) -> UserDTO:
    """
    Find associated data (profile) of a user according to Firebase UID.
    Raise UserDoesNotExistError when there is no user with provided UID.
    """

    user_document = await UserDocument.find_one(UserDocument.uid == uid)

    if user_document is None:
        raise UserDoesNotExistError()

    return UserDTO(**user_document.model_dump())
