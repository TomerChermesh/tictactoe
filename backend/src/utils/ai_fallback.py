from typing import List
from src.constants.game import WINNING_LINES, BASE_CELLS_PRIORITY
from src.exceptions import InvalidMoveError


def _find_winning_move(board: List[int], player_id: int) -> int | None:
    for line in WINNING_LINES:
        values = [board[i] for i in line]
        if values.count(player_id) == 2 and values.count(0) == 1:
            empty_index_in_line = values.index(0)
            return line[empty_index_in_line]
    return None


def get_fallback_move(board: List[int], ai_player_id: int, opponent_player_id: int) -> int:
    move: int | None = _find_winning_move(board, ai_player_id)
    if move is not None:
        return move

    move: int | None = _find_winning_move(board, opponent_player_id)
    if move is not None:
        return move

    for idx in BASE_CELLS_PRIORITY:
        if board[idx] == 0:
            return idx

    raise InvalidMoveError('No empty cells available for fallback move')
