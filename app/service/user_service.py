from typing import Any, Dict, List

from firebase_admin import auth

from app.core.config import settings
from app.models.api.user import UserRegisterReq, UserRegisterRes, UserProfileRes, UserSearchQueryParam
from app.models.DTO.user import UserCreateDTO, UserSearchFilterDTO
from app.models.embedded.enums import UserRole
from app.repository.user_repo import create_user, find_one_user, find_users
from app.exceptions.user import UserDoesNotExistError


async def register_user_service(
    req: UserRegisterReq, decoded_token: Dict[str, Any]
) -> UserRegisterRes:
    uid = decoded_token["uid"]
    email = decoded_token["email"]
    role = UserRole.MANAGER if email in settings.MANAGER_EMAILS else UserRole.WORKER

    # Set role as a field of custom user claims
    auth.set_custom_user_claims(uid, {"role": role.value})

    new_user = UserCreateDTO(
        uid=uid, display_name=req.display_name, email=email, role=role
    )

    created_user = await create_user(new_user)

    return UserRegisterRes(**created_user.model_dump())


async def retrieve_user_profile_service(
        decoded_token: Dict[str, Any]
) -> UserProfileRes:
    user_search_filter = UserSearchFilterDTO(uid=decoded_token["uid"])

    user = await find_one_user(user_search_filter)

    if user:
        return UserProfileRes(**user.model_dump())
    else:
        raise UserDoesNotExistError()


async def search_users_service(query_params: UserSearchQueryParam) -> List[UserProfileRes]:
    if query_params.email:
        user_search_filter = UserSearchFilterDTO(email=query_params.email)
        user = await find_one_user(user_search_filter)

        if user:
            return [UserProfileRes(**user.model_dump())]
        else:
            return []
    else:
        user_search_filter = UserSearchFilterDTO(
            display_name=query_params.display_name,
            role=query_params.role
        )

        users = await find_users(
            user_search_filter,
            page_size=query_params.page_size,
            page_number=query_params.page_number
        )

        return [UserProfileRes(**user.model_dump) for user in users]
