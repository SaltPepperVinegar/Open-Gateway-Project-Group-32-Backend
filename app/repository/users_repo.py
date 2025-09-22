from app.models.base.user import UserCreate
from app.models.db.user import UserDoc


async def create_user(user_create: UserCreate) -> UserCreate:
    userdoc = UserDoc(
        username=user_create.username,
        email=user_create.email,
        role=user_create.role,
        password_hash=user_create.hashed,
    )
    user_create.userID = str(userdoc.id)
    await userdoc.insert()
    return user_create


async def get_user_by_username(username: str) -> UserDoc | None:
    return await UserDoc.find_one(UserDoc.username == username)
