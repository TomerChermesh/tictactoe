from fastapi import APIRouter, Depends, HTTPException
from src.security.auth import get_current_user
from src.models.users import UserDocument
from src.dependencies import get_game_service
from src.services.game import GameService
from src.models.responses import UpdateResponse
from src.exceptions import MatchupNotFoundError
from src.models.matchups import MatchupDocument
from typing import List
from src.utils.rate_limit import rate_limiter

router: APIRouter = APIRouter(prefix='/matchup', dependencies=[Depends(rate_limiter)])


@router.post('/new', response_model=UpdateResponse)
async def create_new_matchup(
    player1_name: str,
    player2_name: str,
    mode: str,
    starting_player: int,
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user),
):
    return await game_service.create_new_matchup(
        current_user.id,
        player1_name,
        player2_name,
        mode,
        starting_player,
    )


@router.get('/list', response_model=List[MatchupDocument])
async def get_matchups_list(
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user),
):
    return await game_service.get_matchups_list_for_user(current_user.id)


@router.get('/{matchup_id}', response_model=UpdateResponse)
async def get_matchup(
    matchup_id: str,
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user),
):
    return await game_service.get_matchup_active_game(matchup_id)


@router.put('/{matchup_id}/update_player_name', response_model=UpdateResponse)
async def update_player_name(
    matchup_id: str,
    player_id: int,
    name: str,
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user),
):
    try:
        return await game_service.update_player_name(matchup_id, player_id, name)
    except MatchupNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


