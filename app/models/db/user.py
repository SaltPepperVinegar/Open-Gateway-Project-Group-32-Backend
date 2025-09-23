from beanie import Document, Indexed
from pydantic import EmailStr

from app.models.base.user import UserBase


class UserDocument(UserBase, Document):
    uid: str = Indexed(unique=True)
    email: EmailStr = Indexed(unique=True)

    class Settings:
        name = "users"
