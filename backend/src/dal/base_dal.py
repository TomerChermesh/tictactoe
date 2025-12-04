from typing import TypeVar, Type
from datetime import datetime, timezone

from beanie import Document
from pydantic import BaseModel


D = TypeVar('D', bound=Document)
P = TypeVar('P', bound=BaseModel)

class BaseDAL:
    def __init__(self, model: Type[D] = Document) -> None:
        self.model: Type[D] = model

    async def create(self, data: P) -> D:
        now: datetime = datetime.now(timezone.utc)
        doc: D = self.model(**data.model_dump(), created_at=now, updated_at=now)
        await doc.insert()
        return doc

    async def update(self, doc: D, data: P) -> D:
        for key, value in data.items():
            setattr(doc, key, value)

        if hasattr(doc, 'updated_at'):
            setattr(doc, 'updated_at', datetime.now(timezone.utc))

        await doc.save()
        return doc
