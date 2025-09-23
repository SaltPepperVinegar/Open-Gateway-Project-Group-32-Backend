from typing import Dict, Any

from firebase_admin import auth

from app.models.api.user import UserRegisterReq, UserRegisterRes
from app.models.base.user import UserCreateBase, Role
from app.repository.users_repo import create_user
from app.core.config import settings


async def register_user_service(req: UserRegisterReq, decoded_token: Dict[str, Any]) -> UserRegisterRes:
    uid = decoded_token["uid"]
    email = decoded_token["email"]
    role = Role.MANAGER if email in settings.MANAGER_EMAILS else Role.WORKER

    # Set role as a field of custom user claims
    auth.set_custom_user_claims(uid, {"role": role.value})

    new_user = UserCreateBase(
        uid=uid,
        email=email,
        role=role,
        display_name=req.display_name
    )

    created_user = await create_user(new_user)

    return UserRegisterRes(**created_user.model_dump())