from typing import Final, List


FASTAPI_TITLE: Final[str] = 'Tic Tac Toe API'
FASTAPI_VERSION: Final[str] = '0.1.0'
VALID_ORIGINS: Final[List[str]] = ['http://localhost:5173', 'http://127.0.0.1:5173']

RATE_LIMIT_MAX_REQUESTS: int = 100
RATE_LIMIT_WINDOW_SECONDS: float = 60.0