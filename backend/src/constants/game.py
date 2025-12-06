from typing import List, Final
from src.models.games import CellIndex

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

BASE_CELLS_PRIORITY: Final[List[CellIndex]] = [4, 0, 2, 6, 8, 1, 3, 5, 7]
