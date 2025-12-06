import pytest
from typing import List
from src.utils.ai_fallback import get_fallback_move
from src.exceptions import InvalidMoveError
from src.models.games import BoardCell
from src.constants.game import WINNING_LINES


class TestGetFallbackMove:
    @pytest.mark.parametrize('board, ai_player_id, opponent_player_id, expected_move', [
        ([1, 1, 0, 2, 0, 2, 0, 0, 0], 1, 2, 2),
        ([0, 0, 0, 1, 1, 0, 2, 0, 2], 1, 2, 5),
        ([0, 0, 0, 2, 0, 2, 1, 1, 0], 1, 2, 8),
        ([1, 0, 2, 1, 0, 2, 0, 0, 0], 1, 2, 6),
        ([0, 1, 2, 0, 1, 2, 0, 0, 0], 1, 2, 7),
        ([0, 0, 1, 0, 0, 1, 2, 0, 0], 1, 2, 8),
        ([1, 0, 2, 0, 1, 0, 0, 0, 0], 1, 2, 8),
        ([0, 0, 1, 0, 1, 0, 0, 0, 0], 1, 2, 6),
        ([2, 2, 0, 1, 0, 1, 0, 0, 0], 2, 1, 2),
    ], ids=[
        'ai_win_horizontal_top',
        'ai_win_horizontal_middle',
        'ai_win_horizontal_bottom',
        'ai_win_vertical_left',
        'ai_win_vertical_middle',
        'ai_win_vertical_right',
        'ai_win_diagonal_tl_br',
        'ai_win_diagonal_tr_bl',
        'ai_win_player_2'
    ])
    def test_ai_can_win(
        self,
        board: List[BoardCell],
        ai_player_id: int,
        opponent_player_id: int,
        expected_move: int
    ) -> None:
        result: int = get_fallback_move(board, ai_player_id, opponent_player_id)
        assert result == expected_move
        assert board[result] == 0  # Ensure chosen cell is empty

    @pytest.mark.parametrize('board, ai_player_id, opponent_player_id, expected_move', [
        ([2, 2, 0, 0, 0, 0, 1, 0, 0], 1, 2, 2),
        ([0, 0, 0, 2, 2, 0, 0, 1, 0], 1, 2, 5),
        ([0, 0, 0, 0, 0, 0, 2, 2, 0], 1, 2, 8),
        ([2, 0, 0, 2, 0, 0, 0, 1, 0], 1, 2, 6),
        ([0, 2, 0, 0, 2, 0, 0, 0, 1], 1, 2, 7),
        ([0, 0, 2, 0, 0, 2, 1, 0, 0], 1, 2, 8),
        ([2, 0, 0, 0, 2, 0, 0, 0, 0], 1, 2, 8),
        ([0, 0, 2, 0, 2, 0, 0, 0, 0], 1, 2, 6),
        ([1, 1, 0, 0, 0, 0, 0, 2, 0], 2, 1, 2),
    ], ids=[
        'block_horizontal_top',
        'block_horizontal_middle',
        'block_horizontal_bottom',
        'block_vertical_left',
        'block_vertical_middle',
        'block_vertical_right',
        'block_diagonal_tl_br',
        'block_diagonal_tr_bl',
        'block_player_2'
    ])
    def test_block_opponent_win(
        self,
        board: List[BoardCell],
        ai_player_id: int,
        opponent_player_id: int,
        expected_move: int
    ) -> None:
        result: int = get_fallback_move(board, ai_player_id, opponent_player_id)
        assert result == expected_move
        assert board[result] == 0

    @pytest.mark.parametrize('board, ai_player_id, opponent_player_id, expected_move', [
        ([0] * 9, 1, 2, 4),
        ([0, 0, 0, 0, 1, 0, 0, 0, 0], 1, 2, 0),
        ([1, 0, 0, 0, 2, 0, 0, 0, 0], 1, 2, 2),
        ([1, 0, 2, 0, 1, 0, 6, 0, 8], 1, 2, 1),
        ([1, 0, 0, 0, 2, 0, 0, 0, 0], 2, 1, 2),
    ], ids=[
        'empty_board_center',
        'center_taken_corner',
        'center_corner_taken_next_corner',
        'center_corners_taken_edge',
        'priority_order'
    ])
    def test_priority_based_move(
        self,
        board: List[BoardCell],
        ai_player_id: int,
        opponent_player_id: int,
        expected_move: int
    ) -> None:
        result: int = get_fallback_move(board, ai_player_id, opponent_player_id)
        assert result == expected_move
        assert board[result] == 0

    @pytest.mark.parametrize('board, ai_player_id, opponent_player_id', [
        ([1, 2, 1, 2, 1, 2, 2, 1, 2], 1, 2),
        ([2, 1, 2, 1, 2, 1, 1, 2, 1], 1, 2),
    ], ids=['full_board_1', 'full_board_2'])
    def test_no_empty_cells_raises_error(
        self,
        board: List[BoardCell],
        ai_player_id: int,
        opponent_player_id: int
    ) -> None:
        with pytest.raises(InvalidMoveError, match='No empty cells available for fallback move'):
            get_fallback_move(board, ai_player_id, opponent_player_id)

    @pytest.mark.parametrize('board, ai_player_id, opponent_player_id, expected_winning_move', [
        ([1, 1, 0, 2, 2, 0, 0, 0, 0], 1, 2, 2),
        ([1, 1, 0, 0, 0, 0, 2, 2, 0], 1, 2, 2),
    ], ids=['ai_win_vs_block_1', 'ai_win_vs_block_2'])
    def test_ai_prioritizes_win_over_block(
        self,
        board: List[BoardCell],
        ai_player_id: int,
        opponent_player_id: int,
        expected_winning_move: int
    ) -> None:
        result: int = get_fallback_move(board, ai_player_id, opponent_player_id)
        assert result == expected_winning_move
        assert board[result] == 0
        
        test_board = board.copy()
        test_board[result] = ai_player_id
        is_winning: bool = any(
            all(test_board[i] == ai_player_id for i in line)
            for line in WINNING_LINES
        )
        assert is_winning, f'Move {result} should be a winning move for AI player {ai_player_id}'
