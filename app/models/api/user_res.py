from typing import Any

from pydantic import BaseModel, EmailStr


class UserRes(BaseModel):
    id: str
    username: str
    email: EmailStr
    meta: dict[str, Any] | None = None
