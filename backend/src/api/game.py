from fastapi import APIRouter, Depends, HTTPException
from src.security.auth import get_current_user
from src.models.users import UserDocument
from src.dependencies import get_game_service
from src.services.game import GameService
from src.models.responses import UpdateResponse
from src.exceptions import (
    GameNotFoundError,
    MatchupNotFoundError,
    InvalidMoveError,
    GameFinishedError
)

router: APIRouter = APIRouter(prefix='/game')


@router.post('/new', response_model=UpdateResponse)
async def create_new_game(
    matchup_id: str,
    starting_player: int,
    game_service: GameService = Depends(get_game_service),
    current_user: UserDocument = Depends(get_current_user)
):
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
    print(f'player_move: game_id={game_id}, player_id={player_id}, cell_index={cell_index}, is_ai_move={is_ai_move}')
    try:
        if is_ai_move:
            return await game_service.ai_move(game_id, player_id)
        elif cell_index is not None:
            return await game_service.player_move(game_id, player_id, cell_index)
        else:
            raise InvalidMoveError('Cell index is required')
    except (GameNotFoundError, MatchupNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (InvalidMoveError, GameFinishedError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
