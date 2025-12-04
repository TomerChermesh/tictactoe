from typing import Type
from datetime import datetime, timezone

from src.models.users import UserDocument


class UsersDAL:
    def __init__(self, model: Type[UserDocument] = UserDocument) -> None:
        self.model: Type[UserDocument] = model

    async def get_user_by_id(self, user_id: str) -> UserDocument | None:
        return await self.model.get(user_id)

    async def get_user_by_email(self, email: str) -> UserDocument | None:
        return await self.model.find_one(self.model.email == email)

    async def create_user(self, email: str, password_hash: str) -> UserDocument:
        now: datetime = datetime.now(timezone.utc)
        user: UserDocument = self.model(
            email=email,
            password=password_hash,
            created_at=now,
            updated_at=now
        )
        await user.insert()
        return user
