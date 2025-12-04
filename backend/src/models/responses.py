from pydantic import BaseModel

from src.models.matchups import MatchupDocument
from src.models.games import GameDocument


class UpdateResponse(BaseModel):
    matchup: MatchupDocument | None = None
    game: GameDocument | None = None

    class Config:
        from_attributes = True
