from typing import List, Type

from beanie import PydanticObjectId

from src.dal.base_dal import BaseDAL
from src.models.games import (
    GameDocument,
    GameCreate,
    GameUpdate,
    PlayerIndex,
    BoardCell,
    CellIndex,
)


class GamesDAL(BaseDAL):
    def __init__(self, model: Type[GameDocument] = GameDocument):
        super().__init__(model)

    async def get_game_by_id(self, game_id: str) -> GameDocument | None:
        return await self.model.get(game_id)
    
    async def get_last_game_for_matchup(self, matchup_id: PydanticObjectId) -> GameDocument | None:
        return await self.model.find_one(self.model.matchup_id == matchup_id).sort('-created_at').first()

    async def create_game(self, matchup_id: PydanticObjectId, starting_player: PlayerIndex) -> GameDocument:
        data: GameCreate = GameCreate(
            matchup_id=matchup_id,
            board=[0] * 9,
            winner=None,
            is_finished=False,
            current_turn=starting_player,
            winning_triplet=None,
        )

        return await self.create(data)

    async def update_game_state(
        self,
        game_id: PydanticObjectId,
        board: List[BoardCell],
        current_turn: PlayerIndex,
        is_finished: bool,
        winner: PlayerIndex | None = None,
        winning_triplet: List[CellIndex] | None = None
    ) -> GameDocument | None:
        game: GameDocument | None = await self.model.get(game_id)
        if game is None:
            return None

        data: GameUpdate = GameUpdate(
            board=board,
            current_turn=current_turn,
            is_finished=is_finished,
            winner=winner,
            winning_triplet=winning_triplet,
        )

        return await self.update(game, data.model_dump(exclude_none=True))
