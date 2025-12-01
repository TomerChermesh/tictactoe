from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI: str = os.getenv('MONGO_URI')
MONGO_DB_NAME: str = os.getenv('MONGO_DB_NAME', 'tic_tac_toe')

JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'dev-secret-change-me')
JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRES_MINUTES: int = int(os.getenv('JWT_EXPIRES_MINUTES', '60'))