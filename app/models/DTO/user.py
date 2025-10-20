from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field

from app.models.embedded.enums import UserRole


class UserDTO(BaseModel):
    """
    The general data transfer object for user resource.
    It covers all fields of user the app maintains.
    """

    uid: str
    display_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserCreateDTO(BaseModel):
    """
    Encapsulate data for a new user creation.
    """

    uid: str
    display_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: UserRole
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
