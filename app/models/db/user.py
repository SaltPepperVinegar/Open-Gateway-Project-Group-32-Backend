from beanie import Document, Indexed
from pydantic import EmailStr, Field
from typing import Annotated
from datetime import datetime
from app.models.embedded.enums import UserRole

class UserDocument(Document):
    uid: Annotated[str, Indexed(unique=True)]
    display_name: str = Field(min_length=1, max_length=100)
    email: Annotated[EmailStr, Indexed(unique=True)]
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "users"
