from typing import List, Literal

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from datetime import datetime


PlayerIndex = Literal[1, 2]
BoardCell = Literal[0, 1, 2]
CellIndex = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]


class GameBase(BaseModel):
    matchup_id: PydanticObjectId
    board: List[BoardCell]
    current_turn: PlayerIndex
    is_finished: bool
    winner: PlayerIndex | None
    winning_triplet: List[CellIndex] | None


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    matchup_id: PydanticObjectId | None = None


class GameDocument(GameBase, Document):
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = 'games'
