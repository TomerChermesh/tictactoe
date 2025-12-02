from fastapi import Depends
from src.dal.users import UsersDAL
from src.dal.matchups import MatchupsDAL
from src.dal.games import GamesDAL
from src.services.game import GameService
from src.services.ai import AIService


_ai_service_instance: AIService | None = None


def get_ai_service() -> AIService:
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
        _ai_service_instance.init_client()
    return _ai_service_instance


def get_users_dal() -> UsersDAL:
    return UsersDAL()


def get_matchups_dal() -> MatchupsDAL:
    return MatchupsDAL()


def get_games_dal() -> GamesDAL:
    return GamesDAL()


def get_game_service(
    matchups_dal: MatchupsDAL = Depends(get_matchups_dal),
    games_dal: GamesDAL = Depends(get_games_dal),
    ai_service: AIService = Depends(get_ai_service)
) -> GameService:
    return GameService(matchups_dal=matchups_dal, games_dal=games_dal, ai_service=ai_service)
