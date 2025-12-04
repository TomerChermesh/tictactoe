import pytest
from typing import List
from src.utils.game import (
    ensure_valid_player_index,
    ensure_valid_cell_index,
    validate_player_move,
    get_next_turn,
    check_game_winner_triplet,
    is_board_full,
    get_random_empty_cell
)
from src.models.games import PlayerIndex, CellIndex, BoardCell


class TestEnsureValidPlayerIndex:   
    @pytest.mark.parametrize('value, expected_result', [
        (1, 1),
        (2, 2),
    ], ids=['valid_1', 'valid_2'])
    def test_happy_ensure_valid_player_index(self, value: int, expected_result: PlayerIndex) -> None:
        result: PlayerIndex = ensure_valid_player_index(value)
        assert result == expected_result

    @pytest.mark.parametrize('value', [
        0,
        3,
        -1,
        100,
    ], ids=['invalid_0', 'invalid_3', 'invalid_negative', 'invalid_large'])
    def test_sad_ensure_valid_player_index(self, value: int) -> None:
        with pytest.raises(ValueError, match='Player index must be 1 or 2'):
            ensure_valid_player_index(value)

class TestEnsureValidCellIndex:   
    @pytest.mark.parametrize('value, expected_result', [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
    ], ids=['valid_0', 'valid_1', 'valid_2', 'valid_3', 'valid_4', 'valid_5', 'valid_6', 'valid_7', 'valid_8'])
    def test_happy_ensure_valid_cell_index(self, value: int, expected_result: CellIndex) -> None:
        result: CellIndex = ensure_valid_cell_index(value)
        assert result == expected_result

    @pytest.mark.parametrize('value', [
        9,
        -1,
        100,
    ], ids=['invalid_9', 'invalid_negative', 'invalid_large'])
    def test_sad_ensure_valid_player_index(self, value: int) -> None:
        with pytest.raises(ValueError, match='Cell index must be between 0 and 8'):
            ensure_valid_cell_index(value)



class TestValidatePlayerMove:    
    @pytest.mark.parametrize('board, current_turn, player_id, cell_index, expected_result', [
        ([0] * 9, 1, 1, 0, True),
        ([0] * 9, 1, 2, 0, False),
        ([1, 0, 2, 0, 1, 0, 0, 0, 2], 1, 1, 0, False),
        ([1, 0, 2, 0, 1, 0, 0, 0, 2], 1, 1, 1, True),
        ([1, 0, 2, 0, 1, 0, 0, 0, 2], 1, 2, 0, False),
    ], ids=['valid_empty', 'wrong_turn', 'cell_occupied', 'valid_partial', 'wrong_turn_and_occupied'])
    def test_validate_player_move(self, board: List[BoardCell], current_turn: PlayerIndex, player_id: PlayerIndex, cell_index: CellIndex, expected_result: bool) -> None:
        result: bool = validate_player_move(board, current_turn, player_id, cell_index)
        assert result == expected_result


class TestGetNextTurn:   
    @pytest.mark.parametrize('current_turn, expected_result', [
        (1, 2),
        (2, 1),
    ], ids=['from_1', 'from_2'])
    def test_get_next_turn(self, current_turn: PlayerIndex, expected_result: PlayerIndex) -> None:
        result: PlayerIndex = get_next_turn(current_turn)
        assert result == expected_result


class TestCheckGameWinnerTriplet:   
    @pytest.mark.parametrize('board, cell_index, player_id, expected_result', [
        ([1, 1, 1, 2, 0, 2, 0, 0, 0], 0, 1, [0, 1, 2]),
        ([2, 1, 0, 2, 1, 0, 2, 0, 0], 0, 2, [0, 3, 6]),
        ([1, 2, 0, 2, 1, 0, 0, 0, 1], 0, 1, [0, 4, 8]),
        ([1, 0, 2, 0, 1, 0, 0, 0, 2], 1, 1, None),
        ([1, 1, 1, 2, 0, 2, 0, 0, 0], 3, 1, None),
        ([0, 0, 0, 1, 1, 1, 2, 0, 0], 3, 1, [3, 4, 5]),
        ([0, 2, 0, 0, 2, 0, 0, 2, 0], 1, 2, [1, 4, 7]),
        ([0, 0, 1, 0, 1, 0, 1, 0, 0], 2, 1, [2, 4, 6]),
    ], ids=['horizontal_top', 'vertical_left', 'diagonal_tl_br', 'no_win', 'win_not_in_line', 'horizontal_middle', 'vertical_middle', 'diagonal_tr_bl'])
    def test_check_game_winner_triplet(self, board: List[BoardCell], cell_index: CellIndex, player_id: PlayerIndex, expected_result: List[CellIndex] | None) -> None:
        result: List[CellIndex] | None = check_game_winner_triplet(board, cell_index, player_id)
        assert result == expected_result


class TestIsBoardFull:   
    @pytest.mark.parametrize('board, expected_result', [
        ([0] * 9, False),
        ([1, 0, 2, 0, 1, 0, 0, 0, 2], False),
        ([1, 2, 1, 2, 1, 2, 2, 1, 2], True),
        ([1, 2, 1, 2, 1, 2, 2, 1, 0], False),
    ], ids=['empty', 'partial', 'full', 'almost_full'])
    def test_is_board_full(self, board: List[BoardCell], expected_result: bool) -> None:
        result: bool = is_board_full(board)
        assert result == expected_result


class TestGetRandomEmptyCell:
    @pytest.mark.parametrize('board, expected_empty_indices', [
        ([0] * 9, {0, 1, 2, 3, 4, 5, 6, 7, 8}),
        ([1, 0, 2, 0, 1, 0, 0, 0, 2], {1, 3, 5, 6, 7}),
    ], ids=['empty_board', 'partial_board'])
    def test_happy_get_random_empty_cell(self, board: List[BoardCell], expected_empty_indices: set[int]) -> None:
        result: CellIndex = get_random_empty_cell(board)
        assert result in range(9)
        assert board[result] == 0
        assert result in expected_empty_indices

    @pytest.mark.parametrize('board', [
        [1, 2, 1, 2, 1, 2, 2, 1, 2],
    ], ids=['full_board'])
    def test_sad_get_random_empty_cell(self, board: List[BoardCell]) -> None:
        with pytest.raises(ValueError, match='No empty cells available on the board'):
            get_random_empty_cell(board)
