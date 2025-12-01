from typing import List, Optional, Final
from src.models.games import BoardCell, PlayerIndex, CellIndex

WINNING_LINES: Final[List[List[CellIndex]]] = [
    [0, 1, 2],  # Top row
    [3, 4, 5],  # Middle row
    [6, 7, 8],  # Bottom row
    [0, 3, 6],  # Left column
    [1, 4, 7],  # Middle column
    [2, 5, 8],  # Right column
    [0, 4, 8],  # Diagonal TL-BR
    [2, 4, 6],  # Diagonal TR-BL
]


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
) -> Optional[List[CellIndex]]:
    for line in WINNING_LINES:
        if cell_index in line and all(board[i] == player_id for i in line):
            return line
    return None


def is_board_full(board: List[BoardCell]) -> bool:
    return all(cell != 0 for cell in board)
