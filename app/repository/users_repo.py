from app.models.db.user import UserDoc


async def create_user(username: str, email: str) -> UserDoc:
    user = UserDoc(username=username, email=email)
    return await user.insert()


async def get_user_by_username(username: str) -> UserDoc | None:
    return await UserDoc.find_one(UserDoc.username == username)
