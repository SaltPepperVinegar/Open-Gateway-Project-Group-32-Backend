from pydantic import BaseModel, EmailStr
from typing import Any


class UserRes(BaseModel):
    id: str
    username: str
    email: EmailStr
    meta: dict[str, Any] | None = None
