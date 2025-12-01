from typing import Optional, List
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
)
from src.utils.game import (
    validate_player_move,
    check_game_winner_triplet,
    get_next_turn,
    is_board_full,
    ensure_valid_player_index,
    ensure_valid_cell_index,
)


class GameService:
    def __init__(self, matchups_dal: MatchupsDAL, games_dal: GamesDAL):
        self.matchups_dal = matchups_dal
        self.games_dal = games_dal

    async def _get_matchup_by_id(self, matchup_id: str) -> MatchupDocument:
        matchup: Optional[MatchupDocument] = await self.matchups_dal.get_matchup_by_id(matchup_id)
        if not matchup:
            raise MatchupNotFoundError(f'Matchup with id {matchup_id} not found')
        return matchup

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

    async def create_independent_new_game(self, starting_player_raw: int) -> GameDocument:
        game: GameDocument = await self.create_new_game(
            matchup_id=matchup.id,
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

        return UpdateResponse(matchup=matchup, game=game)

    async def get_matchups_list_for_user(self, user_id: str) -> List[MatchupDocument]:
        return await self.matchups_dal.list_matchups_for_user(user_id)

    async def get_matchup_active_game(self, matchup_id: str) -> UpdateResponse:
        matchup: MatchupDocument = await self._get_matchup_by_id(matchup_id)
        game: Optional[GameDocument] = await self.games_dal.get_active_game_for_matchup(matchup_id)
        return UpdateResponse(matchup=matchup, game=game)

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

        matchup: MatchupDocument = await self._get_matchup_by_id(matchup_id)
        updated_matchup: MatchupDocument = await self.matchups_dal.update_player_name(
            matchup_id,
            player_id,
            player_name,
        )
        return UpdateResponse(matchup=updated_matchup, game=None)

    async def player_move(
        self,
        game_id: str,
        player_id_raw: int,
        cell_index_raw: int,
    ) -> UpdateResponse:
        try:
            player_id: PlayerIndex = ensure_valid_player_index(player_id_raw)
            cell_index: CellIndex = ensure_valid_cell_index(cell_index_raw)
        except ValueError as e:
            raise InvalidMoveError(str(e))

        game: Optional[GameDocument] = await self.games_dal.get_game_by_id(game_id)
        if not game:
            raise GameNotFoundError(f'Game with id {game_id} not found')

        if game.is_finished:
            raise GameFinishedError('Game is already finished')

        if not validate_player_move(game.board, game.current_turn, player_id, cell_index):
            raise InvalidMoveError('Invalid move: either not your turn or cell is already occupied')

        new_board: List[BoardCell] = game.board.copy()
        new_board[cell_index] = player_id

        winner_triplet: Optional[List[CellIndex]] = check_game_winner_triplet(
            new_board,
            cell_index,
            player_id,
        )
        updated_matchup: Optional[MatchupDocument] = None

        if winner_triplet:
            game.winner = player_id
            game.winning_triplet = winner_triplet
            game.is_finished = True
            updated_matchup = await self.matchups_dal.increase_player_score_by_one(
                game.matchup_id,
                player_id,
            )
        elif is_board_full(new_board):
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
