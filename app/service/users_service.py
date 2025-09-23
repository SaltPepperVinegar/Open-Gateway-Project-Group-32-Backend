from typing import Any, Dict

from firebase_admin import auth

from app.core.config import settings
from app.models.api.user import UserRegisterReq, UserRegisterRes
from app.models.DTO.user import UserCreateDTO
from app.models.embedded.enums import UserRole
from app.repository.users_repo import create_user


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
