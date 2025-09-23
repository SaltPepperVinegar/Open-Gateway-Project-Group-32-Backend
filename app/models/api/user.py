from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from app.models.base.user import UserBase

from app.models.base.user import Role


class UserRegisterReq(BaseModel):
    display_name: str


class UserRegisterRes(UserBase):
    pass
