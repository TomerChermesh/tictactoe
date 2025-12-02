from typing import Type

from src.models.users import UserCreate, UserDocument


class UsersDAL:
    def __init__(self, model: Type[UserDocument] = UserDocument):
        self.model = model

    async def get_user_by_id(self, user_id: str) -> UserDocument | None:
        return await self.model.get(user_id)

    async def get_user_by_email(self, email: str) -> UserDocument | None:
        return await self.model.find_one(self.model.email == email)

    async def create_user(self, email: str, password_hash: str) -> UserDocument:
        payload: UserCreate = UserCreate(
            email=email,
            password=password_hash
        )

        user: UserDocument = self.model(**payload.model_dump(exclude_none=True))
        await user.insert()
        return user
