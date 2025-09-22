from typing import Any

from app.models.base.user import UserBase


class UserCreateRes(UserBase):
    id: str
    meta: dict[str, Any] | None = None
