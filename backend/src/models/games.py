from typing import List, Optional, Literal

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from datetime import datetime


PlayerIndex = Literal[1, 2]
BoardCell = Literal[0, 1, 2]
CellIndex = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]


class GameBase(BaseModel):
    matchup_id: PydanticObjectId
    board: List[BoardCell]
    winner: Optional[PlayerIndex]
    is_finished: bool
    current_turn: PlayerIndex
    winning_triplet: Optional[List[CellIndex]]


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    matchup_id: Optional[PydanticObjectId] = None


class GameDocument(GameBase, Document):
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = 'games'
