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
        prompt: str = f"""
            You are a Tic-Tac-Toe engine.
            
            Game Goal: 
            Win the game by placing 3 of your marks in a horizontal, vertical, or diagonal row. 
            This is the list of winning lines: {WINNING_LINES} 
            
            Board rules: - 3x3 grid, which is represented as a 1D array of 9 cells.
            - Each cell is "X" which represented by 1, "O" which represented by 2, or 0 for empty.
            - You play as {ai_player_id}.
            - {opponent_player_id} is the opponent.
            - It's {ai_player_id}'s turn.
            - The game is not finished yet.
            - You are only allowed to return index of the cell that is not occupied, e.g. with 0 value.
            - If {opponent_player_id} is close to winning, you should block them unless it's a winning move for {ai_player_id}.
            - Otherwise, you should choose the cell that is the best for {ai_player_id} to win.
            - If there is only one empty cell, you should choose it immediately. 
            
            Your task: - Choose the BEST next move for {ai_player_id}.
            - Return ONLY the cell index: DO NOT add text, explanation, or code blocks.
            - Only integer number between 0 and 8!!! 
            
            DO NOT add any text, explanation, or code blocks.
            
            Current board: {board}
            
            """

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

        try:
            response: genai.types.Response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
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

    def validate_response(self, response: genai.types.Response, board: List[int]) -> int:
        raw_text: str = (response.text or '').strip()
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
        