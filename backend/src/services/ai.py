from typing import List
import re

from google import genai
from google.genai.errors import APIError

from src.config import GEMINI_API_KEY
from src.constants.ai import GEMINI_MODEL
from src.constants.game import WINNING_LINES
from src.exceptions import AIServiceError
from src.utils.logger import logger


class AIService:
    def __init__(self):
        self.client: genai.Client | None = None
        self._initialized: bool = False

    def init_client(self):
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
            logger.error('AI service is unavailable due to missing API Key or failed initialization')
            raise AIServiceError('AI service is unavailable due to missing API Key or failed initialization.')

        try:
            response: genai.types.Response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
        except APIError as e:
            logger.error('Failed to get response from AI model due to API error', exception=e)
            raise AIServiceError('Failed to get response from AI model due to API error.') from e
        except Exception as e:
            logger.error('An unexpected error occurred during AI request', exception=e)
            raise AIServiceError('An unexpected error occurred during AI request.') from e

        raw_text: str = (response.text or '').strip()
        logger.debug(f'Response from Gemini: {raw_text}')

        if not raw_text:
            logger.error('AI returned an empty response')
            raise AIServiceError('AI returned an empty response.')

        match = re.search(r'\d+', raw_text)
        if not match:
            logger.error(f'AI returned a non-numeric response: {raw_text!r}')
            raise AIServiceError(f'AI returned a non-numeric response: {raw_text!r}')

        ai_cell_index: int = int(match.group())

        if ai_cell_index < 0 or ai_cell_index > 8:
            logger.error(f'AI returned an out-of-range cell index: {ai_cell_index}')
            raise AIServiceError(f'AI returned an out-of-range cell index: {ai_cell_index}')

        if ai_cell_index >= len(board) or board[ai_cell_index] != 0:
            logger.error(f'AI selected an invalid or occupied cell index: {ai_cell_index}')
            raise AIServiceError(f'AI selected an invalid or occupied cell index: {ai_cell_index}')

        logger.info(f'AI selected cell index: {ai_cell_index}')
        return ai_cell_index
