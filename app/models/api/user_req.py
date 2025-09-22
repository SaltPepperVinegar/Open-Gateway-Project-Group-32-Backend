from app.models.base.user import UserBase


class UserCreateReq(UserBase):
    password: str
