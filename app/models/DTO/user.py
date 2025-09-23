from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field

from app.models.embedded.enums import UserRole


class UserCreateDTO(BaseModel):
    uid: str
    display_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: UserRole
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
