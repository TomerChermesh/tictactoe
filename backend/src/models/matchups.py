from enum import Enum

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from datetime import datetime


class MatchMode(str, Enum):
    friend = 'friend'
    ai = 'ai'


class MatchupBase(BaseModel):
    user_id: PydanticObjectId
    player1_name: str
    player1_score: int = 0
    player2_name: str
    player2_score: int = 0
    mode: MatchMode


class MatchupCreate(MatchupBase):
    pass


class MatchupUpdateName(BaseModel):
    player1_name: str | None = None
    player2_name: str | None = None


class MatchupUpdateScore(BaseModel):
    player1_score: int | None = None
    player2_score: int | None = None


class MatchupDocument(MatchupBase, Document):
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = 'matchups'
