from enum import Enum

from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    WORKER = "worker"
    MANAGER = "manager"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Role


class UserCreate(UserBase):
    password_hash: str | None = None
    userID: str | None = None
