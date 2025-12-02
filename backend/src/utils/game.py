from typing import List
import random
from src.models.games import BoardCell, PlayerIndex, CellIndex

from src.constants.game import WINNING_LINES


def ensure_valid_player_index(value: int) -> PlayerIndex:
    if value not in (1, 2):
        raise ValueError('Player index must be 1 or 2')
    return value


def ensure_valid_cell_index(value: int) -> CellIndex:
    if value < 0 or value > 8:
        raise ValueError('Cell index must be between 0 and 8')
    return value


def validate_player_move(
    board: List[BoardCell],
    current_turn: PlayerIndex,
    player_id: PlayerIndex,
    cell_index: CellIndex
) -> bool:
    if current_turn != player_id:
        return False

    if board[cell_index] != 0:
        return False

    return True


def get_next_turn(current_turn: PlayerIndex) -> PlayerIndex:
    return 1 if current_turn == 2 else 2


def check_game_winner_triplet(
    board: List[BoardCell],
    cell_index: CellIndex,
    player_id: PlayerIndex
) -> List[CellIndex] | None:
    for line in WINNING_LINES:
        if cell_index in line and all(board[i] == player_id for i in line):
            return line
    return None


def is_board_full(board: List[BoardCell]) -> bool:
    return all(cell != 0 for cell in board)


def get_random_empty_cell(board: List[BoardCell]) -> CellIndex:
    empty_cells: List[CellIndex] = [i for i in range(len(board)) if board[i] == 0]
    if not empty_cells:
        raise ValueError('No empty cells available on the board')
    return random.choice(empty_cells)
