from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from beanie import init_beanie

from src.config import MONGO_URI, MONGO_DB_NAME
from src.models.users import UserDocument
from src.models.games import GameDocument
from src.models.matchups import MatchupDocument
from src.utils.logger import logger


async def init_db() -> None:
    logger.info(f'Initializing database connection: database={MONGO_DB_NAME}')
    try:
        client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=30000)
        database: AsyncIOMotorDatabase = client[MONGO_DB_NAME]

        await init_beanie(
            database=database,
            document_models=[
                UserDocument,
                GameDocument,
                MatchupDocument
            ]
        )
        logger.info('Database connection established and Beanie initialized successfully')
    except Exception as e:
        logger.error(f'Failed to initialize database: {str(e)}', exception=e)
        raise
