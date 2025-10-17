from datetime import datetime, timezone
from typing import Optional, Self

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.models.embedded.enums import UserRole


class UserDTO(BaseModel):
    """
    The general data transfer object for user resource.
    It covers all fields of user the app maintains.
    One typical scenario using this model is encapsulation
    of user data retrieved from database.
    """

    uid: str
    display_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


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


class UserSearchFilterDTO(BaseModel):
    """
    Encapsulates the fields used to specify search filter
    when searching user documents in database.
    At least one of these fields must be provided.
    A typical use case is retrieving information of
    multiple users which meet all filter requirements.
    e.g. Get associated information of all "worker" users.
    """

    uid: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    

    @model_validator(mode="after")
    def check_not_all_none(self) -> Self:
        model_dict = self.model_dump()

        none_field_count = len([v for v in model_dict.values() if v is None])
        field_count = len(model_dict)

        if field_count == none_field_count:
            raise ValueError("At least one identifying field must be provided.")

        return self
