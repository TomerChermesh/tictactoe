from datetime import datetime, timezone

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserDocument(Document):
    email: Indexed(EmailStr, unique=True)
    password: str

    created_at: datetime
    updated_at: datetime

    class Settings:
        name = 'users'

    async def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
        await self.save()
