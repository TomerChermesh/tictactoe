from typing import List
from beanie import PydanticObjectId
from src.dal.matchups import MatchupsDAL
from src.dal.games import GamesDAL
from src.models.matchups import MatchupDocument
from src.models.responses import UpdateResponse
from src.models.games import GameDocument, PlayerIndex, CellIndex, BoardCell
from src.exceptions import (
    GameNotFoundError,
    MatchupNotFoundError,
    InvalidMoveError,
    GameFinishedError,
    AIServiceError,
)
from src.utils.game import (
    validate_player_move,
    check_game_winner_triplet,
    get_next_turn,
    is_board_full,
    ensure_valid_player_index,
    ensure_valid_cell_index,
    get_random_empty_cell
)
from src.services.ai import AIService
from src.utils.logger import logger


class GameService:
    def __init__(self, matchups_dal: MatchupsDAL, games_dal: GamesDAL, ai_service: AIService) -> None:
        self.matchups_dal: MatchupsDAL = matchups_dal
        self.games_dal: GamesDAL = games_dal
        self.ai_service: AIService = ai_service

    async def create_new_game(self, matchup_id: PydanticObjectId, starting_player_raw: int) -> GameDocument:
        try:
            starting_player: PlayerIndex = ensure_valid_player_index(starting_player_raw)
        except ValueError as e:
            raise InvalidMoveError(str(e))

        game: GameDocument = await self.games_dal.create_game(
            matchup_id=matchup_id,
            starting_player=starting_player
        )

        return game

    async def create_independent_new_game(self, matchup_id: PydanticObjectId, starting_player_raw: int) -> UpdateResponse:
        game: GameDocument = await self.create_new_game(
            matchup_id=matchup_id,
            starting_player_raw=starting_player_raw
        )

        return UpdateResponse(matchup=None, game=game)

    async def create_new_matchup(
        self,
        user_id: PydanticObjectId,
        player1_name: str,
        player2_name: str,
        mode: str,
        starting_player_raw: int,
    ) -> UpdateResponse:
        logger.info(f'Creating new matchup: user_id={user_id}, player1={player1_name}, player2={player2_name}, mode={mode}')
        matchup: MatchupDocument = await self.matchups_dal.create_matchup(
            user_id=user_id,
            player1_name=player1_name,
            player2_name=player2_name,
            mode=mode,
        )

        game: GameDocument = await self.create_new_game(
            matchup_id=matchup.id,
            starting_player_raw=starting_player_raw
        )

        logger.info(f'Matchup and game created: matchup_id={matchup.id}, game_id={game.id}')
        return UpdateResponse(matchup=matchup, game=game)

    async def get_matchups_list_for_user(self, user_id: PydanticObjectId) -> List[MatchupDocument]:
        return await self.matchups_dal.list_matchups_for_user(user_id)

    async def get_last_game_for_matchup(self, matchup_id: PydanticObjectId) -> GameDocument | None:
        return await self.games_dal.get_last_game_for_matchup(matchup_id)

    async def update_player_name(
        self,
        matchup_id: str,
        player_id_raw: int,
        player_name: str,
    ) -> UpdateResponse:
        try:
            player_id: PlayerIndex = ensure_valid_player_index(player_id_raw)
        except ValueError as e:
            raise InvalidMoveError(str(e))

        updated_matchup: MatchupDocument | None = await self.matchups_dal.update_player_name(
            matchup_id,
            player_id,
            player_name,
        )

        if not updated_matchup:
            warning_message: str = f'Matchup not found: matchup_id={matchup_id}'
            logger.warning(warning_message)
            raise MatchupNotFoundError(warning_message)

        return UpdateResponse(matchup=updated_matchup, game=None)

    async def player_move(
        self,
        game_id: str,
        player_id_raw: int,
        cell_index_raw: int
    ) -> UpdateResponse:
        try:
            player_id: PlayerIndex = ensure_valid_player_index(player_id_raw)
            cell_index: CellIndex = ensure_valid_cell_index(cell_index_raw)
        except ValueError as e:
            raise InvalidMoveError(str(e))

        game: GameDocument | None = await self.games_dal.get_game_by_id(game_id)
        
        self.validate_move(game, player_id, cell_index)
        
        new_board: List[BoardCell] = game.board.copy()
        new_board[cell_index] = player_id

        winner_triplet: List[CellIndex] | None = check_game_winner_triplet(
            new_board,
            cell_index,
            player_id,
        )
        updated_matchup: MatchupDocument | None = None

        if winner_triplet:
            logger.info(f'Game finished with winner: game_id={game_id}, winner={player_id}')
            game.winner = player_id
            game.winning_triplet = winner_triplet
            game.is_finished = True
            updated_matchup = await self.matchups_dal.increase_player_score_by_one(
                game.matchup_id,
                player_id,
            )
        elif is_board_full(new_board):
            logger.info(f'Game finished with draw: game_id={game_id}')
            game.is_finished = True
        else:
            game.current_turn = get_next_turn(player_id)

        updated_game: GameDocument = await self.games_dal.update_game_state(
            game_id=game_id,
            board=new_board,
            current_turn=game.current_turn,
            is_finished=game.is_finished,
            winner=game.winner,
            winning_triplet=game.winning_triplet,
        )

        return UpdateResponse(matchup=updated_matchup, game=updated_game)
    

    async def validate_move(self, game: GameDocument, player_id: PlayerIndex, cell_index: CellIndex) -> None:
        warning_message: str
        if not game:
            warning_message = f'Game not found: game_id={game.id}'
            logger.warning(warning_message)
            raise GameNotFoundError(warning_message)

        if game.is_finished:
            warning_message = f'Attempted move on finished game: game_id={game.id}'
            logger.warning(warning_message)
            raise GameFinishedError(warning_message)

        if not validate_player_move(game.board, game.current_turn, player_id, cell_index):
            warning_message = f'Invalid move: game_id={game.id}, player_id={player_id}, cell_index={cell_index}'
            logger.warning(warning_message)
            raise InvalidMoveError(warning_message)

    async def ai_move(
        self,
        game_id: str,
        ai_player_id: int
    ) -> UpdateResponse:
        logger.info(f'AI move requested: game_id={game_id}, ai_player_id={ai_player_id}')
        game: GameDocument | None = await self.games_dal.get_game_by_id(game_id)
        if not game:
            warning_message: str = f'Game not found for AI move: game_id={game_id}'
            logger.warning(warning_message)
            raise GameNotFoundError(warning_message)

        ai_move: int
        opponent_player_id: PlayerIndex = 2 if ai_player_id == 1 else 1
        try:
            ai_move = self.ai_service.get_next_move(game.board, ai_player_id, opponent_player_id)
        except AIServiceError as e:
            logger.warning(f'AI move failed, using random empty cell: {str(e)}')
            ai_move = get_random_empty_cell(game.board)

        return await self.player_move(game_id, ai_player_id, ai_move)

