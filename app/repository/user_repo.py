from typing import Optional, List

from pymongo.errors import DuplicateKeyError
from pymongo import DESCENDING

from app.exceptions.user import UserAlreadyRegisteredError
from app.models.db.user import UserDocument
from app.models.DTO.user import UserCreateDTO, UserDTO, UserSearchFilterDTO


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


async def find_one_user(user_search_filter: UserSearchFilterDTO) -> Optional[UserDTO]:
    """
    Find associated data of a user according to specified user identity.
    Identity could be UID, email or other non-duplicated field.
    Return None when no user is found.
    """

    target = await UserDocument.find_one(user_search_filter.model_dump(exclude_none=True))

    return None if target is None else UserDTO(**target.model_dump())


async def find_users(
    user_search_filter: UserSearchFilterDTO,
    page_size: int,
    page_number: int
) -> List[UserDTO]:
    """
    Search and return information of users meeting conditions specified in the filter.
    Page size specifies the maximum number of users returned in one search (i.e., results per page).
    Page number specifies which page of the results to retrieve (starting from 0).
    If no users meet the conditions, an empty list is returned.
    """

    # Initialize search query
    search_query = UserDocument.find()

    # A user is considered a match if the specified display name in filter
    # appears as a substring anywhere in the display name of a user document.
    if user_search_filter.display_name is not None:
        search_query = search_query.find(
            user_search_filter.display_name.lower() in UserDocument.display_name.lower()
        )
    
    if user_search_filter.role is not None:
        search_query = search_query.find(
            user_search_filter.role == UserDocument.role
        )

    # Results are sorted according to update time in descending order
    search_query = search_query \
        .sort([UserDocument.updated_at, DESCENDING]) \
        .skip(page_size * page_number) \
        .limit(page_size)
    
    user_documents = await search_query.to_list()

    return [UserDTO(**user_document.model_dump()) for user_document in user_documents]