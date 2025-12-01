from typing import Optional
from pydantic import BaseModel

from src.models.matchups import MatchupDocument
from src.models.games import GameDocument


class UpdateResponse(BaseModel):
    matchup: Optional[MatchupDocument] = None
    game: Optional[GameDocument] = None

    class Config:
        from_attributes = True
