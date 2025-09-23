from enum import Enum
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    WORKER = "worker"
    MANAGER = "manager"


class UserBase(BaseModel):
    uid: str
    email: EmailStr
    role: Role
    display_name: str
    created_at: datetime
    updated_at: datetime


class UserCreateBase(UserBase):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserSearchBase(UserBase):
    uid: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
    display_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None