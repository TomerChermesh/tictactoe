from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


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
        self.updated_at = datetime.utcnow()
        await self.save()
