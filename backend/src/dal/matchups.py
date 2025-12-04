from typing import List, Type

from beanie import PydanticObjectId

from src.dal.base_dal import BaseDAL
from src.models.matchups import MatchMode, MatchupCreate, MatchupUpdateName, MatchupUpdateScore, MatchupDocument
from src.models.games import PlayerIndex
from src.exceptions import MatchupNotFoundError

class MatchupsDAL(BaseDAL):
    def __init__(self, model: Type[MatchupDocument] = MatchupDocument) -> None:
        self.model: Type[MatchupDocument] = model

    async def create_matchup(
        self,
        user_id: PydanticObjectId,
        player1_name: str,
        player2_name: str,
        mode: MatchMode
    ) -> MatchupDocument:
        data: MatchupCreate = MatchupCreate(
            user_id=user_id,
            player1_name=player1_name,
            player1_score=0,
            player2_name=player2_name,
            player2_score=0,
            mode=mode
        )
        return await self.create(data)

    async def get_matchup_by_id(self, matchup_id: str) -> MatchupDocument | None:
        return await self.model.get(matchup_id)

    async def list_matchups_for_user(
        self,
        user_id: PydanticObjectId
    ) -> List[MatchupDocument]:
        return await self.model.find(self.model.user_id == user_id).sort('-updated_at').to_list()

    async def update_player_name(
        self,
        matchup_id: str,
        player_id: PlayerIndex,
        name: str
    ) -> MatchupDocument | None:
        matchup: MatchupDocument | None = await self.model.get(matchup_id)
        if not matchup:
            raise MatchupNotFoundError(f'Matchup with id {matchup_id} not found')

        data: MatchupUpdateName = MatchupUpdateName(
            player1_name=name if player_id == 1 else None,
            player2_name=name if player_id == 2 else None
        )

        return await self.update(matchup, data.model_dump(exclude_none=True))

    async def increase_player_score_by_one(
        self,
        matchup_id: str,
        player_id: PlayerIndex
    ) -> MatchupDocument | None:
        matchup: MatchupDocument | None = await self.model.get(matchup_id)
        if not matchup:
            raise MatchupNotFoundError(f'Matchup with id {matchup_id} not found')

        data: MatchupUpdateScore = MatchupUpdateScore(
            player1_score=matchup.player1_score + 1 if player_id == 1 else None,
            player2_score=matchup.player2_score + 1 if player_id == 2 else None
        )

        return await self.update(matchup, data.model_dump(exclude_none=True))
