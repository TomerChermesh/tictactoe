from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from beanie import init_beanie

from src.config import MONGO_URI, MONGO_DB_NAME
from src.models.users import UserDocument
from src.models.games import GameDocument
from src.models.matchups import MatchupDocument


async def init_db() -> None:
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
