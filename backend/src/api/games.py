from fastapi import APIRouter, Depends, HTTPException
from src.security.auth import get_current_user
from src.models.users import UserDocument
from src.dependencies import get_game_service
from src.services.game import GameService
from src.models.responses import UpdateResponse
from src.models.games import GameDocument
from src.exceptions import (
    GameNotFoundError,
    MatchupNotFoundError,
    InvalidMoveError,
    GameFinishedError
)
from beanie import PydanticObjectId
from src.utils.rate_limit import rate_limiter
from src.utils.logger import logger

router: APIRouter = APIRouter(prefix='/games', dependencies=[Depends(rate_limiter)])


@router.post('/new', response_model=UpdateResponse)
async def create_new_game(
    matchup_id: str,
    starting_player: int,
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user)
):
    logger.info(f'Create new game: matchup_id={matchup_id}, starting_player={starting_player}')
    return await game_service.create_independent_new_game(matchup_id, starting_player)


@router.post('/{game_id}/move', response_model=UpdateResponse)
async def player_move(
    game_id: str,
    player_id: int,
    cell_index: int | None = None,
    is_ai_move: bool = False,
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user)
):
    logger.info(f'Player move request: game_id={game_id}, player_id={player_id}, cell_index={cell_index}, is_ai_move={is_ai_move}')
    try:
        if is_ai_move:
            return await game_service.ai_move(game_id, player_id)
        elif cell_index is not None:
            return await game_service.player_move(game_id, player_id, cell_index)
        else:
            raise InvalidMoveError('Cell index is required')
    except (GameNotFoundError, MatchupNotFoundError) as e:
        logger.warning(f'Game/Matchup not found: {str(e)}')
        raise HTTPException(status_code=404, detail=str(e))
    except (InvalidMoveError, GameFinishedError) as e:
        logger.warning(f'Invalid move or game finished: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f'Unexpected error in player_move: {str(e)}', exception=e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/last_game', response_model=GameDocument)
async def get_last_game_for_matchup(
    matchup_id: PydanticObjectId,
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user)
):
    logger.info(f'Get last game for matchup: matchup_id={matchup_id}')
    try:
        game: GameDocument | None = await game_service.get_last_game_for_matchup(matchup_id)
        if not game:
            raise HTTPException(status_code=404, detail='Game not found for this matchup')
        return game
    except HTTPException:
        raise
    except (GameNotFoundError, MatchupNotFoundError) as e:
        logger.warning(f'Game/Matchup not found: {str(e)}')
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f'Unexpected error in get_last_game_for_matchup: {str(e)}', exception=e)
        raise HTTPException(status_code=500, detail=str(e))

