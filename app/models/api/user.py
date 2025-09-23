from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.models.embedded.enums import UserRole


class UserRegisterReq(BaseModel):
    display_name: str = Field(min_length=1, max_length=100)


class UserRegisterRes(BaseModel):
    uid: str
    display_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime
