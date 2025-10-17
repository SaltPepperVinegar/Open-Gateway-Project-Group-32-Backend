from datetime import datetime
from typing import Optional, Self

from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator

from app.models.embedded.enums import UserRole


class UserRegisterReq(BaseModel):
    display_name: str = Field(min_length=1, max_length=100)


class UserRegisterRes(BaseModel):
    uid: str
    display_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserProfileRes(BaseModel):
    uid: str
    display_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserSearchQueryParam(BaseModel):
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(
        default=None,
        description= \
            "If email is specified, "
            "no other fields should be specified because email uniquely identifies a user."
    )
    role: Optional[UserRole] = None
    page_size: int = Field(description="Page size must be greater than 0.")
    page_number: int = Field(description="Page number starts from 0.")


    @model_validator(mode="after")
    def check_page_size_and_number_range(self) -> Self:
        if self.page_size <= 0:
            raise ValueError("Page size must be a positive non-zero number.")
        
        if self.page_number < 0:
            raise ValueError("Page number must be non-negative number.")

        return self
    

    @model_validator(mode="after")
    def check_not_all_none(self) -> Self:
        model_dict = self.model_dump()

        none_field_count = len([v for v in model_dict.values() if v is None])
        field_count = len(model_dict)

        if field_count == none_field_count:
            raise ValueError("At least one field must be provided for search.")

        return self
    

    @model_validator(mode="after")
    def check_if_only_email(self) -> Self:
        if self.email is not None and (self.display_name is not None or self.role is not None):
            raise ValueError("If email is provided for search, no other fields can be provided.")
        
        return self
    
