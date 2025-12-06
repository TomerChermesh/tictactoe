from typing import List
import re

from google import genai
from google.genai.errors import APIError

from src.config import GEMINI_API_KEY
from src.constants.ai import GEMINI_MODEL, AI_RESPONSE_REGEX
from src.constants.game import WINNING_LINES
from src.exceptions import AIServiceError
from src.utils.logger import logger


class AIService:
    def __init__(self) -> None:
        self.client: genai.Client | None = None
        self._initialized: bool = False
        self._rules_cache_name: str | None = None

    def init_client(self) -> None:
        if self._initialized and self.client is not None:
            return

        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
            self._initialized = True
            logger.info('Gemini Client initialized successfully')
        except Exception as e:
            logger.error('Error initializing Gemini Client', exception=e)
            self.client = None
            self._initialized = False

    def get_next_move(self, board: List[int], ai_player_id: int, opponent_player_id: int) -> int:
        error_message: str

        logger.debug(
            f'Sending prompt to Gemini: Current board: {board}, '
            f'AI player: {ai_player_id}, Opponent player: {opponent_player_id}'
        )

        if not self._initialized:
            self.init_client()

        if not self.client:
            error_message = 'AI service is unavailable due to missing API Key or failed initialization'
            logger.error(error_message)
            raise AIServiceError(error_message)

        prompt: str = f"""
        You are a fast Tic-Tac-Toe engine.

        OUTPUT (CRITICAL):
        - Respond with EXACTLY ONE digit between 0 and 8.
        - No text, no explanation, no spaces, no punctuation.

        GAME STATE:
        - Board (0=empty, 1=X, 2=O): {board}
        - You are player {ai_player_id}.
        - Opponent: {opponent_player_id}.
        - It is your turn.
        - Winning lines: {WINNING_LINES}

        RULES:
        1. Choose a legal empty cell (value 0).
        2. If you can win now, choose that cell.
        3. Else if opponent can win next turn, block them.
        4. Else choose the best move for you.
        5. If only one empty cell remains, choose it.

        RETURN:
        Only the chosen cell index (0–8). ONE digit. Nothing else.
        """

        try:
            result = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            response: str = getattr(result, 'text', '')
            logger.debug(f'Raw Gemini result: {response!r}')

        except APIError as e:
            error_message = 'Failed to get response from AI model due to API error'
            logger.error(error_message, exception=e)
            raise AIServiceError(error_message)
        except Exception as e:
            error_message = 'An unexpected error occurred during AI request'
            logger.error(error_message, exception=e)
            raise AIServiceError(error_message)

        ai_cell_index: int = self.validate_response(response, board)
        logger.info(f'AI selected cell index: {ai_cell_index}')
        return ai_cell_index



    def validate_response(self, response: str, board: List[int]) -> int:
        raw_text: str = response.strip()
        logger.debug(f'Response from Gemini: {raw_text}')

        if not raw_text:
            error_message = 'AI returned an empty response'
            logger.error(error_message)
            raise AIServiceError(error_message)

        if not re.match(AI_RESPONSE_REGEX, raw_text):
            error_message = f'AI returned a bad structured response: {raw_text!r}. Expected a single digit between 0-8.'
            logger.error(error_message)
            raise AIServiceError(error_message)

        ai_cell_index: int = int(raw_text)

        if ai_cell_index >= len(board) or board[ai_cell_index] != 0:
            error_message = f'AI returned an invalid or occupied cell index: {ai_cell_index}'
            logger.error(error_message)
            raise AIServiceError(error_message)
        
        return ai_cell_index
        