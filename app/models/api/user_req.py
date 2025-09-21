from pydantic import BaseModel, EmailStr

class CreateUserReq(BaseModel):
    username: str
    email: EmailStr
