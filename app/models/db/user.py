from beanie import Document

from app.models.base.user import UserBase


class UserDoc(UserBase, Document):
    password_hash: str

    class Settings:
        name = "users"  # collection name
