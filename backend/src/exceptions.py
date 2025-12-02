class GameNotFoundError(Exception):
    """Raised when a game is not found."""
    pass


class MatchupNotFoundError(Exception):
    """Raised when a matchup is not found."""
    pass


class InvalidMoveError(Exception):
    """Raised when a move is invalid."""
    pass


class GameFinishedError(Exception):
    """Raised when trying to make a move on a finished game."""
    pass


class AIServiceError(Exception):
    """Raised when the AI service returns an invalid response or fails."""
    pass

