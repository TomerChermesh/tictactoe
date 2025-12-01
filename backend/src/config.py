from dotenv import load_dotenv
import os
from typing import Final

load_dotenv()

MONGO_URI: Final[str] = os.getenv('MONGO_URI')
MONGO_DB_NAME: Final[str] = os.getenv('MONGO_DB_NAME', 'tic_tac_toe')

JWT_SECRET_KEY: Final[str] = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM: Final[str] = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRES_MINUTES: Final[int] = int(os.getenv('JWT_EXPIRES_MINUTES', '60'))

GEMINI_API_KEY: Final[str] = os.getenv('GEMINI_API_KEY')