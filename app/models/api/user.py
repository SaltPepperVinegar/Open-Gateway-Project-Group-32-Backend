from pydantic import BaseModel

from app.models.base.user import UserBase


class UserRegisterReq(BaseModel):
    display_name: str


class UserRegisterRes(UserBase):
    pass
