from typing import Optional, List, Type

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

    async def get_game_by_id(self, game_id: str) -> Optional[GameDocument]:
        return await self.model.get(game_id)
    
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

    async def list_games_for_matchup(self, matchup_id: PydanticObjectId) -> List[GameDocument]:
        return await self.model.find(
            self.model.matchup_id == matchup_id
        ).sort('-created_at').to_list()

    async def get_active_game_for_matchup(self, matchup_id: PydanticObjectId) -> Optional[GameDocument]:
        return await self.model.find_one(
            self.model.matchup_id == matchup_id,
            self.model.is_finished == False
        )

    async def update_game_state(
        self,
        game_id: PydanticObjectId,
        board: List[BoardCell],
        current_turn: PlayerIndex,
        is_finished: bool,
        winner: Optional[PlayerIndex] = None,
        winning_triplet: Optional[List[CellIndex]] = None
    ) -> Optional[GameDocument]:
        game: Optional[GameDocument] = await self.model.get(game_id)
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
