from beanie import Document
from pydantic import EmailStr

class UserDoc(Document):
    username: str
    email: EmailStr

    class Settings:
        name = "users"  # collection name
