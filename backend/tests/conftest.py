import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch


@pytest.fixture
def temp_dir():
    """Create a temporary directory for file operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_board_empty():
    """Empty board for testing."""
    return [0] * 9


@pytest.fixture
def sample_board_partial():
    """Partially filled board."""
    return [1, 0, 2, 0, 1, 0, 0, 0, 2]


@pytest.fixture
def sample_board_full():
    """Full board (draw scenario)."""
    return [1, 2, 1, 2, 1, 2, 2, 1, 2]


@pytest.fixture
def sample_board_winner_horizontal():
    """Board with horizontal win for player 1."""
    return [1, 1, 1, 2, 0, 2, 0, 0, 0]


@pytest.fixture
def sample_board_winner_vertical():
    """Board with vertical win for player 2."""
    return [2, 1, 0, 2, 1, 0, 2, 0, 0]


@pytest.fixture
def sample_board_winner_diagonal():
    """Board with diagonal win for player 1."""
    return [1, 2, 0, 2, 1, 0, 0, 0, 1]

